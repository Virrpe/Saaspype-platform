"""
Luciq Phase 5: WebSocket Broadcasting Service
Real-time broadcasting of multi-modal fusion results and trending insights
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Set, Dict, Any, List
from fastapi import WebSocket, WebSocketDisconnect
from collections import defaultdict, deque
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DateTimeEncoder(json.JSONEncoder):
    """Custom JSON encoder to handle datetime and set objects"""
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, set):
            return list(obj)
        return super().default(obj)

class WebSocketBroadcaster:
    """
    Real-time WebSocket broadcasting service for Phase 5 multi-modal fusion
    
    Features:
    - Client connection management
    - Multi-modal fusion broadcasting
    - Real-time trend updates
    - Client-specific subscriptions
    - Performance monitoring
    - Automatic reconnection handling
    """
    
    def __init__(self):
        # Connected clients
        self.active_connections: Set[WebSocket] = set()
        self.client_subscriptions: Dict[WebSocket, Set[str]] = defaultdict(set)
        self.client_metadata: Dict[WebSocket, Dict[str, Any]] = {}
        
        # Broadcasting queues
        self.fusion_queue = asyncio.Queue(maxsize=10000)
        self.trend_queue = asyncio.Queue(maxsize=5000)
        self.alert_queue = asyncio.Queue(maxsize=1000)
        
        # Message history for new connections
        self.recent_fusion_results = deque(maxlen=100)
        self.recent_trends = deque(maxlen=50)
        self.recent_alerts = deque(maxlen=20)
        
        # Performance metrics
        self.broadcast_stats = {
            'total_connections': 0,
            'active_connections': 0,
            'messages_sent': 0,
            'messages_failed': 0,
            'fusion_broadcasts': 0,
            'trend_broadcasts': 0,
            'alert_broadcasts': 0,
            'avg_broadcast_time': 0.0
        }
        
        # Broadcasting task
        self.broadcaster_task = None
        
        logger.info("WebSocket Broadcaster initialized")
    
    async def connect(self, websocket: WebSocket, client_id: str = None) -> Dict[str, Any]:
        """Accept new WebSocket connection"""
        
        try:
            await websocket.accept()
            self.active_connections.add(websocket)
            
            # Initialize client metadata
            self.client_metadata[websocket] = {
                'client_id': client_id or f"client_{len(self.active_connections)}",
                'connected_at': datetime.now(),
                'last_ping': datetime.now(),
                'messages_received': 0,
                'subscriptions': set()
            }
            
            # Default subscriptions
            self.client_subscriptions[websocket] = {'fusion', 'trends', 'alerts'}
            
            # Update stats
            self.broadcast_stats['total_connections'] += 1
            self.broadcast_stats['active_connections'] = len(self.active_connections)
            
            # Start broadcaster if not running
            if not self.broadcaster_task:
                self.broadcaster_task = asyncio.create_task(self._start_broadcaster())
            
            # Send welcome message with recent data
            await self._send_welcome_message(websocket)
            
            logger.info(f"WebSocket client connected: {self.client_metadata[websocket]['client_id']}")
            
            return {
                'status': 'connected',
                'client_id': self.client_metadata[websocket]['client_id'],
                'subscriptions': list(self.client_subscriptions[websocket]),
                'recent_data_available': {
                    'fusion_results': len(self.recent_fusion_results),
                    'trends': len(self.recent_trends),
                    'alerts': len(self.recent_alerts)
                }
            }
            
        except Exception as e:
            logger.error(f"WebSocket connection error: {str(e)}")
            await self.disconnect(websocket)
            return {'status': 'error', 'message': str(e)}
    
    async def disconnect(self, websocket: WebSocket):
        """Handle WebSocket disconnection"""
        
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
            
            client_id = self.client_metadata.get(websocket, {}).get('client_id', 'unknown')
            
            # Clean up metadata
            if websocket in self.client_metadata:
                del self.client_metadata[websocket]
            if websocket in self.client_subscriptions:
                del self.client_subscriptions[websocket]
            
            # Update stats
            self.broadcast_stats['active_connections'] = len(self.active_connections)
            
            logger.info(f"WebSocket client disconnected: {client_id}")
    
    async def broadcast_fusion_result(self, fusion_data: Dict[str, Any]):
        """Broadcast multi-modal fusion result to subscribed clients"""
        
        message = {
            'type': 'multimodal_fusion',
            'timestamp': datetime.now().isoformat(),
            'data': fusion_data
        }
        
        # Add to queue and history
        try:
            await self.fusion_queue.put(message)
            self.recent_fusion_results.append(message)
            self.broadcast_stats['fusion_broadcasts'] += 1
        except asyncio.QueueFull:
            logger.warning("Fusion broadcast queue full")
    
    async def broadcast_trend_update(self, trend_data: Dict[str, Any]):
        """Broadcast trend update to subscribed clients"""
        
        message = {
            'type': 'trend_update',
            'timestamp': datetime.now().isoformat(),
            'data': trend_data
        }
        
        # Add to queue and history
        try:
            await self.trend_queue.put(message)
            self.recent_trends.append(message)
            self.broadcast_stats['trend_broadcasts'] += 1
        except asyncio.QueueFull:
            logger.warning("Trend broadcast queue full")
    
    async def broadcast_alert(self, alert_data: Dict[str, Any]):
        """Broadcast alert to subscribed clients"""
        
        message = {
            'type': 'alert',
            'timestamp': datetime.now().isoformat(),
            'data': alert_data,
            'priority': alert_data.get('priority', 'normal')
        }
        
        # Add to queue and history
        try:
            await self.alert_queue.put(message)
            self.recent_alerts.append(message)
            self.broadcast_stats['alert_broadcasts'] += 1
        except asyncio.QueueFull:
            logger.warning("Alert broadcast queue full")
    
    async def handle_client_message(self, websocket: WebSocket, message: str):
        """Handle incoming message from client"""
        
        try:
            data = json.loads(message)
            message_type = data.get('type')
            
            if message_type == 'ping':
                await self._handle_ping(websocket)
            elif message_type == 'subscribe':
                await self._handle_subscription(websocket, data.get('channels', []))
            elif message_type == 'unsubscribe':
                await self._handle_unsubscription(websocket, data.get('channels', []))
            elif message_type == 'request_history':
                await self._send_history(websocket, data.get('data_type'))
            else:
                logger.warning(f"Unknown message type: {message_type}")
            
            # Update client stats
            if websocket in self.client_metadata:
                self.client_metadata[websocket]['messages_received'] += 1
                self.client_metadata[websocket]['last_ping'] = datetime.now()
                
        except json.JSONDecodeError:
            logger.error(f"Invalid JSON received from client")
        except Exception as e:
            logger.error(f"Error handling client message: {str(e)}")
    
    async def _send_welcome_message(self, websocket: WebSocket):
        """Send welcome message with recent data to new client"""
        
        welcome_data = {
            'type': 'welcome',
            'timestamp': datetime.now().isoformat(),
            'client_info': self.client_metadata[websocket],
            'system_status': {
                'active_connections': len(self.active_connections),
                'fusion_engine_active': True,
                'recent_activity': {
                    'fusion_results': len(self.recent_fusion_results),
                    'trends': len(self.recent_trends),
                    'alerts': len(self.recent_alerts)
                }
            },
            'available_subscriptions': ['fusion', 'trends', 'alerts', 'system'],
            'recent_data': {
                'latest_fusion': self.recent_fusion_results[-1] if self.recent_fusion_results else None,
                'latest_trend': self.recent_trends[-1] if self.recent_trends else None,
                'latest_alert': self.recent_alerts[-1] if self.recent_alerts else None
            }
        }
        
        await self._send_to_client(websocket, welcome_data)
    
    async def _handle_ping(self, websocket: WebSocket):
        """Handle ping message from client"""
        
        pong_message = {
            'type': 'pong',
            'timestamp': datetime.now().isoformat(),
            'server_time': time.time()
        }
        
        await self._send_to_client(websocket, pong_message)
    
    async def _handle_subscription(self, websocket: WebSocket, channels: List[str]):
        """Handle subscription request"""
        
        valid_channels = {'fusion', 'trends', 'alerts', 'system'}
        new_subscriptions = set(channels) & valid_channels
        
        self.client_subscriptions[websocket].update(new_subscriptions)
        
        response = {
            'type': 'subscription_updated',
            'timestamp': datetime.now().isoformat(),
            'subscribed_channels': list(self.client_subscriptions[websocket]),
            'newly_added': list(new_subscriptions)
        }
        
        await self._send_to_client(websocket, response)
    
    async def _handle_unsubscription(self, websocket: WebSocket, channels: List[str]):
        """Handle unsubscription request"""
        
        removed_subscriptions = set(channels) & self.client_subscriptions[websocket]
        self.client_subscriptions[websocket] -= removed_subscriptions
        
        response = {
            'type': 'subscription_updated',
            'timestamp': datetime.now().isoformat(),
            'subscribed_channels': list(self.client_subscriptions[websocket]),
            'removed': list(removed_subscriptions)
        }
        
        await self._send_to_client(websocket, response)
    
    async def _send_history(self, websocket: WebSocket, data_type: str):
        """Send historical data to client"""
        
        history_data = {
            'type': 'history',
            'timestamp': datetime.now().isoformat(),
            'data_type': data_type,
            'data': []
        }
        
        if data_type == 'fusion':
            history_data['data'] = list(self.recent_fusion_results)[-20:]
        elif data_type == 'trends':
            history_data['data'] = list(self.recent_trends)[-10:]
        elif data_type == 'alerts':
            history_data['data'] = list(self.recent_alerts)[-10:]
        
        await self._send_to_client(websocket, history_data)
    
    async def _start_broadcaster(self):
        """Start the main broadcasting loop"""
        
        logger.info("WebSocket broadcaster started")
        
        while True:
            try:
                # Process all queues concurrently
                await asyncio.gather(
                    self._process_fusion_queue(),
                    self._process_trend_queue(),
                    self._process_alert_queue(),
                    return_exceptions=True
                )
                
                # Small delay to prevent CPU overload
                await asyncio.sleep(0.01)
                
            except Exception as e:
                logger.error(f"Broadcaster error: {str(e)}")
                await asyncio.sleep(1)
    
    async def _process_fusion_queue(self):
        """Process fusion broadcast queue"""
        
        try:
            message = self.fusion_queue.get_nowait()
            await self._broadcast_to_subscribers(message, 'fusion')
        except asyncio.QueueEmpty:
            pass
    
    async def _process_trend_queue(self):
        """Process trend broadcast queue"""
        
        try:
            message = self.trend_queue.get_nowait()
            await self._broadcast_to_subscribers(message, 'trends')
        except asyncio.QueueEmpty:
            pass
    
    async def _process_alert_queue(self):
        """Process alert broadcast queue"""
        
        try:
            message = self.alert_queue.get_nowait()
            await self._broadcast_to_subscribers(message, 'alerts')
        except asyncio.QueueEmpty:
            pass
    
    async def _broadcast_to_subscribers(self, message: Dict[str, Any], channel: str):
        """Broadcast message to clients subscribed to specific channel"""
        
        start_time = time.time()
        sent_count = 0
        failed_count = 0
        
        # Get subscribed clients
        subscribed_clients = [
            websocket for websocket in self.active_connections
            if channel in self.client_subscriptions.get(websocket, set())
        ]
        
        # Broadcast to all subscribed clients concurrently
        if subscribed_clients:
            results = await asyncio.gather(
                *[self._send_to_client(client, message) for client in subscribed_clients],
                return_exceptions=True
            )
            
            # Count successful/failed sends
            for result in results:
                if isinstance(result, Exception):
                    failed_count += 1
                else:
                    sent_count += 1
        
        # Update statistics
        broadcast_time = time.time() - start_time
        self.broadcast_stats['messages_sent'] += sent_count
        self.broadcast_stats['messages_failed'] += failed_count
        
        # Update average broadcast time
        if self.broadcast_stats['messages_sent'] > 0:
            current_avg = self.broadcast_stats['avg_broadcast_time']
            total_messages = self.broadcast_stats['messages_sent']
            self.broadcast_stats['avg_broadcast_time'] = (
                (current_avg * (total_messages - sent_count) + broadcast_time * sent_count) / total_messages
            )
        
        if sent_count > 0:
            logger.debug(f"Broadcasted {channel} message to {sent_count} clients in {broadcast_time:.3f}s")
    
    async def _send_to_client(self, websocket: WebSocket, message: Dict[str, Any]):
        """Send message to specific client"""
        
        try:
            await websocket.send_text(json.dumps(message, cls=DateTimeEncoder))
        except WebSocketDisconnect:
            await self.disconnect(websocket)
        except Exception as e:
            logger.error(f"Failed to send message to client: {str(e)}")
            await self.disconnect(websocket)
            raise e
    
    def get_broadcaster_stats(self) -> Dict[str, Any]:
        """Get comprehensive broadcaster statistics"""
        
        return {
            'connections': {
                'active': len(self.active_connections),
                'total_ever': self.broadcast_stats['total_connections']
            },
            'message_stats': {
                'sent': self.broadcast_stats['messages_sent'],
                'failed': self.broadcast_stats['messages_failed'],
                'success_rate': (
                    self.broadcast_stats['messages_sent'] / 
                    max(self.broadcast_stats['messages_sent'] + self.broadcast_stats['messages_failed'], 1)
                ) * 100
            },
            'broadcast_stats': {
                'fusion': self.broadcast_stats['fusion_broadcasts'],
                'trends': self.broadcast_stats['trend_broadcasts'], 
                'alerts': self.broadcast_stats['alert_broadcasts']
            },
            'performance': {
                'avg_broadcast_time': self.broadcast_stats['avg_broadcast_time'],
                'queue_sizes': {
                    'fusion': self.fusion_queue.qsize(),
                    'trends': self.trend_queue.qsize(),
                    'alerts': self.alert_queue.qsize()
                }
            },
            'client_details': {
                websocket: {
                    'client_id': metadata['client_id'],
                    'connected_duration': (datetime.now() - metadata['connected_at']).total_seconds(),
                    'messages_received': metadata['messages_received'],
                    'subscriptions': list(self.client_subscriptions.get(websocket, set()))
                }
                for websocket, metadata in self.client_metadata.items()
            }
        }

# Global broadcaster instance
websocket_broadcaster = WebSocketBroadcaster() 