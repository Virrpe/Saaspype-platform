"""
Data Standardization Module for Luciq Intelligence Orchestration

This module ensures consistent data structures across all intelligence engines,
fixing the attribute access issues identified in production readiness testing.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Dict, List, Any, Union, Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class StandardSignal:
    """Standardized signal structure for all intelligence engines"""
    content: str
    source: str
    timestamp: datetime
    engagement_score: float
    keywords: List[str] = None
    sentiment_score: float = 0.5
    url: Optional[str] = None
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.keywords is None:
            self.keywords = []
        if self.metadata is None:
            self.metadata = {}

@dataclass
class StandardPlatformData:
    """Standardized platform data structure"""
    platform: str
    signals: List[StandardSignal]
    metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

class DataStandardizer:
    """
    Standardizes data structures for consistent engine processing
    
    Fixes the following issues:
    - Dict objects missing 'engagement_score' attribute
    - Dict objects missing 'value' attribute  
    - Inconsistent signal structures across engines
    - Missing required attributes for engine processing
    """
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        
    def standardize_platform_signals(self, platform_signals: Dict[str, List]) -> Dict[str, List]:
        """Standardize platform signals to consistent format"""
        standardized = {}
        
        for platform, signals in platform_signals.items():
            standardized_signals = []
            
            for signal in signals:
                try:
                    std_signal = self._standardize_signal(signal, platform)
                    standardized_signals.append(std_signal)
                except Exception as e:
                    self.logger.warning(f"Failed to standardize signal from {platform}: {e}")
                    continue
            
            standardized[platform] = standardized_signals
            
        return standardized
    
    def _standardize_signal(self, signal: Union[Dict, Any], default_platform: str = "unknown"):
        """Convert any signal format to StandardSignal"""
        
        if isinstance(signal, dict):
            content = signal.get('content', signal.get('text', ''))
            source = signal.get('source', signal.get('platform', default_platform))
            
            timestamp_raw = signal.get('timestamp', datetime.now())
            if isinstance(timestamp_raw, str):
                try:
                    timestamp = datetime.fromisoformat(timestamp_raw.replace('Z', '+00:00'))
                except:
                    timestamp = datetime.now()
            else:
                timestamp = timestamp_raw
            
            engagement_score = (
                signal.get('engagement_score') or
                signal.get('score') or 
                signal.get('value') or
                0.0
            )
            
            keywords = signal.get('keywords', [])
            if isinstance(keywords, str):
                keywords = keywords.split(',')
            
            return StandardSignal(
                content=content,
                source=source,
                timestamp=timestamp,
                engagement_score=float(engagement_score),
                keywords=keywords,
                sentiment_score=float(signal.get('sentiment_score', 0.5)),
                url=signal.get('url'),
                metadata={}
            )
        
        return signal
    
    def standardize_temporal_signals(self, signals: List[Union[Dict, Any]]) -> List[StandardSignal]:
        """
        Standardize temporal signals for temporal pattern engine
        
        Ensures 'value' attribute is mapped to engagement_score
        """
        standardized = []
        
        for signal in signals:
            try:
                std_signal = self._standardize_signal(signal)
                standardized.append(std_signal)
            except Exception as e:
                self.logger.warning(f"Failed to standardize temporal signal: {e}")
                continue
                
        return standardized
    
    def standardize_contextual_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Standardize contextual data for contextual source intelligence
        
        Ensures proper structure for dialectical synthesis
        """
        standardized = data.copy()
        
        # Ensure query exists
        if 'query' not in standardized and 'content' in standardized:
            standardized['query'] = standardized['content']
        
        # Ensure context exists
        if 'context' not in standardized:
            standardized['context'] = {}
            
        return standardized
    
    def create_mock_signal(self, content: str, source: str, engagement_score: float = 10.0) -> StandardSignal:
        """Create a properly structured mock signal for testing"""
        return StandardSignal(
            content=content,
            source=source,
            timestamp=datetime.now(),
            engagement_score=engagement_score,
            keywords=content.lower().split()[:3],  # Simple keyword extraction
            sentiment_score=0.5,
            metadata={}
        )

# Global instance for easy access
data_standardizer = DataStandardizer()

def standardize_engine_input(data: Any, engine_type: str = "generic") -> Any:
    """
    Convenience function to standardize input data for any engine
    
    Args:
        data: Raw input data
        engine_type: Type of engine (cross_platform, temporal, contextual, etc.)
        
    Returns:
        Standardized data appropriate for the engine
    """
    
    if engine_type == "cross_platform":
        if isinstance(data, dict) and 'platform_signals' in data:
            return {
                **data,
                'platform_signals': data_standardizer.standardize_platform_signals(data['platform_signals'])
            }
    
    elif engine_type == "temporal":
        if isinstance(data, dict) and 'signals' in data:
            return {
                **data,
                'signals': data_standardizer.standardize_temporal_signals(data['signals'])
            }
    
    elif engine_type == "contextual":
        if isinstance(data, dict):
            return data_standardizer.standardize_contextual_data(data)
    
    return data 