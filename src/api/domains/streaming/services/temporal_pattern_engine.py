#!/usr/bin/env python3
"""
Advanced Temporal Pattern Recognition Engine - Phase 2 Implementation
Complex time-based pattern detection, seasonality analysis, and trend emergence prediction
"""

import asyncio
import logging
import json
import numpy as np
import pandas as pd
from datetime import datetime, timedelta, time
from typing import List, Dict, Optional, Tuple, Set
from dataclasses import dataclass, field
from collections import defaultdict, deque
import statistics

# Time series analysis libraries
from scipy import stats, signal
from scipy.fft import fft, fftfreq
import statsmodels.api as sm
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from statsmodels.tsa.arima.model import ARIMA
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import DBSCAN

# Visualization and analysis
import matplotlib.pyplot as plt
import seaborn as sns

logger = logging.getLogger(__name__)

@dataclass
class TemporalPattern:
    """Detected temporal pattern in trend signals"""
    pattern_type: str  # 'seasonal', 'cyclical', 'trend', 'anomaly', 'emergence'
    pattern_strength: float  # 0.0 - 1.0
    pattern_period: Optional[float] = None  # Period in hours/days
    pattern_confidence: float = 0.0
    pattern_description: str = ""
    
    # Timing characteristics
    peak_times: List[datetime] = field(default_factory=list)
    valley_times: List[datetime] = field(default_factory=list)
    acceleration_points: List[datetime] = field(default_factory=list)
    
    # Prediction metrics
    emergence_velocity: float = 0.0  # Rate of signal increase
    momentum_score: float = 0.0      # Current momentum
    persistence_score: float = 0.0   # Pattern persistence
    
    # Statistical measures
    autocorrelation: float = 0.0
    trend_slope: float = 0.0
    volatility: float = 0.0
    
    # Metadata
    detection_method: str = ""
    detected_at: datetime = field(default_factory=datetime.now)
    data_points: int = 0

@dataclass
class TrendEmergenceSignal:
    """Signal indicating emerging trend based on temporal analysis"""
    trend_id: str
    emergence_score: float  # 0.0 - 1.0
    emergence_stage: str    # 'inception', 'growth', 'acceleration', 'maturity'
    
    # Temporal characteristics
    first_detected: datetime
    acceleration_start: Optional[datetime] = None
    current_velocity: float = 0.0
    predicted_peak: Optional[datetime] = None
    
    # Pattern indicators
    seasonal_component: float = 0.0
    trend_component: float = 0.0
    noise_level: float = 0.0
    
    # Forecasting
    short_term_forecast: List[float] = field(default_factory=list)  # Next 24 hours
    confidence_intervals: Dict = field(default_factory=dict)
    
    # Related patterns
    similar_patterns: List[str] = field(default_factory=list)
    correlation_patterns: Dict = field(default_factory=dict)

class AdvancedTemporalPatternEngine:
    """Revolutionary temporal pattern recognition for trend detection"""
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.logger.info("⏰ Initializing Advanced Temporal Pattern Recognition Engine...")
        
        # Pattern detection configuration
        self._initialize_pattern_config()
        
        # Historical data storage for pattern learning
        self.signal_history = defaultdict(deque)
        self.pattern_history = defaultdict(list)
        
        # Pattern templates and learned behaviors
        self._initialize_pattern_templates()
        
        # Performance tracking
        self.analysis_stats = {
            'patterns_detected': 0,
            'emergence_signals_generated': 0,
            'prediction_accuracy': 0.0,
            'avg_processing_time': 0.0
        }
        
        self.logger.info("✅ Advanced Temporal Pattern Engine initialized successfully")
    
    def _initialize_pattern_config(self):
        """Initialize pattern detection configuration"""
        self.config = {
            # Seasonality detection
            'seasonal_periods': {
                'hourly': 24,      # Daily patterns
                'daily': 7,        # Weekly patterns  
                'weekly': 4,       # Monthly patterns
                'monthly': 12      # Yearly patterns
            },
            
            # Trend detection thresholds
            'trend_thresholds': {
                'weak': 0.3,
                'moderate': 0.6,
                'strong': 0.8
            },
            
            # Emergence detection parameters
            'emergence_config': {
                'min_data_points': 10,
                'velocity_threshold': 0.1,
                'acceleration_threshold': 0.05,
                'momentum_window': 6  # hours
            },
            
            # Pattern matching
            'similarity_threshold': 0.7,
            'pattern_memory_limit': 1000
        }
    
    def _initialize_pattern_templates(self):
        """Initialize known pattern templates"""
        self.pattern_templates = {
            'viral_emergence': {
                'description': 'Rapid exponential growth characteristic of viral trends',
                'signature': 'exponential_growth',
                'velocity_profile': [0.1, 0.3, 0.7, 1.0, 0.8, 0.4],
                'typical_duration': 72,  # hours
                'peak_indicators': ['high_acceleration', 'cross_platform_correlation']
            },
            
            'seasonal_surge': {
                'description': 'Predictable seasonal increases',
                'signature': 'periodic_peaks',
                'velocity_profile': [0.2, 0.5, 0.8, 0.9, 0.7, 0.3],
                'typical_duration': 168,  # 1 week
                'peak_indicators': ['calendar_correlation', 'historical_precedent']
            },
            
            'market_disruption': {
                'description': 'Sudden paradigm shift causing sustained interest',
                'signature': 'step_function_growth',
                'velocity_profile': [0.1, 0.1, 0.9, 0.8, 0.7, 0.6],
                'typical_duration': 720,  # 30 days
                'peak_indicators': ['innovation_markers', 'media_attention']
            },
            
            'bubble_formation': {
                'description': 'Unsustainable growth followed by collapse',
                'signature': 'bubble_pattern',
                'velocity_profile': [0.2, 0.6, 0.9, 1.0, 0.3, 0.1],
                'typical_duration': 240,  # 10 days
                'peak_indicators': ['unsustainable_growth', 'speculation_markers']
            }
        }
    
    async def analyze_temporal_patterns(self, signals: List[Dict], timeframe_hours: int = 168) -> List[TemporalPattern]:
        """
        Analyze temporal patterns in trend signals
        
        Args:
            signals: List of signals with timestamps and values
            timeframe_hours: Analysis timeframe in hours
            
        Returns:
            List of detected temporal patterns
        """
        start_time = datetime.now()
        
        try:
            # Convert signals to time series
            time_series = self._prepare_time_series(signals, timeframe_hours)
            
            if len(time_series) < self.config['emergence_config']['min_data_points']:
                self.logger.warning(f"Insufficient data points: {len(time_series)}")
                return []
            
            detected_patterns = []
            
            # 1. Seasonality Detection
            seasonal_patterns = await self._detect_seasonality(time_series)
            detected_patterns.extend(seasonal_patterns)
            
            # 2. Trend Analysis
            trend_patterns = await self._analyze_trends(time_series)
            detected_patterns.extend(trend_patterns)
            
            # 3. Cyclical Pattern Detection
            cyclical_patterns = await self._detect_cyclical_patterns(time_series)
            detected_patterns.extend(cyclical_patterns)
            
            # 4. Anomaly Detection
            anomaly_patterns = await self._detect_temporal_anomalies(time_series)
            detected_patterns.extend(anomaly_patterns)
            
            # 5. Emergence Pattern Recognition
            emergence_patterns = await self._detect_emergence_patterns(time_series)
            detected_patterns.extend(emergence_patterns)
            
            # Update statistics
            processing_time = (datetime.now() - start_time).total_seconds()
            self._update_pattern_stats(len(detected_patterns), processing_time)
            
            self.logger.info(f"✅ Detected {len(detected_patterns)} temporal patterns in {processing_time:.2f}s")
            return detected_patterns
            
        except Exception as e:
            self.logger.error(f"❌ Temporal pattern analysis failed: {e}")
            return []
    
    def _prepare_time_series(self, signals: List, timeframe_hours: int) -> pd.DataFrame:
        """Prepare time series data for analysis"""
        if not signals:
            return pd.DataFrame()
        
        # Extract timestamps and values
        data_points = []
        cutoff_time = datetime.now() - timedelta(hours=timeframe_hours)
        
        for signal in signals:
            # Handle both dict and StandardSignal objects
            if hasattr(signal, 'timestamp'):
                # StandardSignal object
                timestamp = signal.timestamp
                engagement = signal.engagement_score
                sentiment = signal.sentiment_score
                source = signal.source
            else:
                # Dictionary signal
                timestamp = signal.get('timestamp')
                engagement = signal.get('engagement_score', 0.0)
                sentiment = signal.get('sentiment_score', 0.0)
                source = signal.get('source', 'unknown')
            
            if isinstance(timestamp, str):
                timestamp = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
            elif not isinstance(timestamp, datetime):
                continue
            
            if timestamp < cutoff_time:
                continue
            
            # Extract signal strength (composite of engagement, sentiment, etc.)
            signal_strength = self._calculate_signal_strength_unified(signal)
            
            data_points.append({
                'timestamp': timestamp,
                'signal_strength': signal_strength,
                'engagement': engagement,
                'sentiment': sentiment,
                'source': source
            })
        
        if not data_points:
            return pd.DataFrame()
        
        # Create DataFrame and resample to regular intervals
        df = pd.DataFrame(data_points)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df = df.set_index('timestamp').sort_index()
        
        # Resample to hourly intervals and aggregate
        hourly_df = df.resample('1H').agg({
            'signal_strength': 'sum',
            'engagement': 'mean',
            'sentiment': 'mean',
            'source': 'count'
        }).fillna(0)
        
        # Rename source count to signal_count
        hourly_df = hourly_df.rename(columns={'source': 'signal_count'})
        
        return hourly_df
    
    def _calculate_signal_strength(self, signal: Dict) -> float:
        """Calculate composite signal strength (legacy method for dict signals)"""
        engagement = signal.get('engagement_score', 0.0)
        sentiment_abs = abs(signal.get('sentiment_score', 0.0))
        credibility = signal.get('credibility_weight', 1.0)
        
        # Weighted combination
        strength = (engagement * 0.5 + sentiment_abs * 0.3 + credibility * 0.2)
        return min(strength, 1.0)
    
    def _calculate_signal_strength_unified(self, signal) -> float:
        """Calculate composite signal strength for both dict and StandardSignal objects"""
        if hasattr(signal, 'engagement_score'):
            # StandardSignal object
            engagement = signal.engagement_score
            sentiment_abs = abs(signal.sentiment_score)
            credibility = getattr(signal, 'credibility_weight', 1.0)
        else:
            # Dictionary signal
            engagement = signal.get('engagement_score', 0.0)
            sentiment_abs = abs(signal.get('sentiment_score', 0.0))
            credibility = signal.get('credibility_weight', 1.0)
        
        # Weighted combination
        strength = (engagement * 0.5 + sentiment_abs * 0.3 + credibility * 0.2)
        return min(strength, 1.0)
    
    async def _detect_seasonality(self, time_series: pd.DataFrame) -> List[TemporalPattern]:
        """Detect seasonal patterns in time series"""
        if len(time_series) < 48:  # Need at least 2 days of hourly data
            return []
        
        patterns = []
        
        try:
            # Test different seasonal periods
            for period_name, period_length in self.config['seasonal_periods'].items():
                if len(time_series) < period_length * 2:
                    continue
                
                # Perform seasonal decomposition
                decomposition = seasonal_decompose(
                    time_series['signal_strength'], 
                    model='additive', 
                    period=period_length,
                    extrapolate_trend='freq'
                )
                
                # Calculate seasonality strength
                seasonal_strength = self._calculate_seasonality_strength(
                    decomposition.seasonal, 
                    decomposition.resid
                )
                
                if seasonal_strength > 0.3:  # Significant seasonality
                    pattern = TemporalPattern(
                        pattern_type='seasonal',
                        pattern_strength=seasonal_strength,
                        pattern_period=period_length,
                        pattern_confidence=min(seasonal_strength * 1.2, 1.0),
                        pattern_description=f"{period_name.capitalize()} seasonal pattern",
                        detection_method='seasonal_decomposition',
                        data_points=len(time_series)
                    )
                    
                    # Extract peak and valley times
                    pattern.peak_times = self._find_seasonal_peaks(
                        decomposition.seasonal, 
                        time_series.index
                    )
                    pattern.valley_times = self._find_seasonal_valleys(
                        decomposition.seasonal, 
                        time_series.index
                    )
                    
                    patterns.append(pattern)
        
        except Exception as e:
            self.logger.warning(f"Seasonality detection failed: {e}")
        
        return patterns
    
    def _calculate_seasonality_strength(self, seasonal: pd.Series, residual: pd.Series) -> float:
        """Calculate strength of seasonal component"""
        try:
            seasonal_var = seasonal.var()
            residual_var = residual.var()
            
            if seasonal_var + residual_var == 0:
                return 0.0
            
            strength = seasonal_var / (seasonal_var + residual_var)
            return min(strength, 1.0)
        except:
            return 0.0
    
    def _find_seasonal_peaks(self, seasonal: pd.Series, timestamps: pd.DatetimeIndex) -> List[datetime]:
        """Find peak times in seasonal component"""
        try:
            peaks, _ = signal.find_peaks(seasonal.values, height=seasonal.std())
            return [timestamps[i].to_pydatetime() for i in peaks if i < len(timestamps)]
        except:
            return []
    
    def _find_seasonal_valleys(self, seasonal: pd.Series, timestamps: pd.DatetimeIndex) -> List[datetime]:
        """Find valley times in seasonal component"""
        try:
            valleys, _ = signal.find_peaks(-seasonal.values, height=seasonal.std())
            return [timestamps[i].to_pydatetime() for i in valleys if i < len(timestamps)]
        except:
            return []
    
    async def _analyze_trends(self, time_series: pd.DataFrame) -> List[TemporalPattern]:
        """Analyze trend patterns in time series"""
        patterns = []
        
        try:
            signal_values = time_series['signal_strength'].values
            if len(signal_values) < 10:
                return patterns
            
            # Linear trend analysis
            x = np.arange(len(signal_values))
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, signal_values)
            
            # Determine trend strength
            trend_strength = abs(r_value)
            trend_direction = 'increasing' if slope > 0 else 'decreasing'
            
            if trend_strength > self.config['trend_thresholds']['weak']:
                pattern = TemporalPattern(
                    pattern_type='trend',
                    pattern_strength=trend_strength,
                    pattern_confidence=1.0 - p_value if p_value < 1.0 else 0.0,
                    pattern_description=f"{trend_direction.capitalize()} linear trend",
                    trend_slope=slope,
                    detection_method='linear_regression',
                    data_points=len(signal_values)
                )
                
                # Calculate additional metrics
                pattern.autocorrelation = self._calculate_autocorrelation(signal_values)
                pattern.volatility = np.std(signal_values) / np.mean(signal_values) if np.mean(signal_values) > 0 else 0
                
                patterns.append(pattern)
            
            # Polynomial trend analysis for non-linear trends
            if len(signal_values) >= 20:
                poly_pattern = await self._analyze_polynomial_trend(time_series)
                if poly_pattern:
                    patterns.append(poly_pattern)
        
        except Exception as e:
            self.logger.warning(f"Trend analysis failed: {e}")
        
        return patterns
    
    def _calculate_autocorrelation(self, values: np.ndarray, lag: int = 1) -> float:
        """Calculate autocorrelation at specified lag"""
        try:
            if len(values) <= lag:
                return 0.0
            
            correlation = np.corrcoef(values[:-lag], values[lag:])[0, 1]
            return correlation if not np.isnan(correlation) else 0.0
        except:
            return 0.0
    
    async def _analyze_polynomial_trend(self, time_series: pd.DataFrame) -> Optional[TemporalPattern]:
        """Analyze non-linear polynomial trends"""
        try:
            signal_values = time_series['signal_strength'].values
            x = np.arange(len(signal_values))
            
            # Fit polynomial trends of different degrees
            best_pattern = None
            best_score = 0.0
            
            for degree in [2, 3]:
                try:
                    coeffs = np.polyfit(x, signal_values, degree)
                    poly_values = np.polyval(coeffs, x)
                    
                    # Calculate R-squared
                    ss_res = np.sum((signal_values - poly_values) ** 2)
                    ss_tot = np.sum((signal_values - np.mean(signal_values)) ** 2)
                    r_squared = 1 - (ss_res / ss_tot) if ss_tot > 0 else 0
                    
                    if r_squared > best_score and r_squared > 0.6:
                        pattern_type = 'quadratic_trend' if degree == 2 else 'cubic_trend'
                        
                        pattern = TemporalPattern(
                            pattern_type=pattern_type,
                            pattern_strength=r_squared,
                            pattern_confidence=r_squared,
                            pattern_description=f"Degree-{degree} polynomial trend",
                            detection_method=f'polynomial_regression_deg_{degree}',
                            data_points=len(signal_values)
                        )
                        
                        # Find acceleration points (inflection points for cubic)
                        if degree == 3:
                            pattern.acceleration_points = self._find_inflection_points(
                                coeffs, time_series.index
                            )
                        
                        best_pattern = pattern
                        best_score = r_squared
                
                except Exception as e:
                    continue
            
            return best_pattern
        
        except Exception as e:
            self.logger.warning(f"Polynomial trend analysis failed: {e}")
            return None
    
    def _find_inflection_points(self, coeffs: np.ndarray, timestamps: pd.DatetimeIndex) -> List[datetime]:
        """Find inflection points in cubic polynomial"""
        try:
            if len(coeffs) != 4:  # Must be cubic
                return []
            
            # Second derivative coefficients
            second_deriv_coeffs = [6 * coeffs[0], 2 * coeffs[1]]
            
            # Find roots of second derivative (inflection points)
            if second_deriv_coeffs[0] != 0:
                inflection_x = -second_deriv_coeffs[1] / second_deriv_coeffs[0]
                if 0 <= inflection_x < len(timestamps):
                    return [timestamps[int(inflection_x)].to_pydatetime()]
            
            return []
        except:
            return []
    
    async def _detect_cyclical_patterns(self, time_series: pd.DataFrame) -> List[TemporalPattern]:
        """Detect cyclical patterns using FFT analysis"""
        patterns = []
        
        try:
            signal_values = time_series['signal_strength'].values
            if len(signal_values) < 24:  # Need sufficient data for FFT
                return patterns
            
            # Apply FFT
            fft_values = fft(signal_values)
            freqs = fftfreq(len(signal_values))
            
            # Find dominant frequencies
            magnitude = np.abs(fft_values)
            
            # Ignore DC component and find peaks
            magnitude[0] = 0  # Remove DC component
            peaks, properties = signal.find_peaks(
                magnitude[:len(magnitude)//2], 
                height=np.max(magnitude) * 0.1
            )
            
            for peak in peaks:
                freq = freqs[peak]
                if freq > 0:  # Only positive frequencies
                    period = 1 / freq  # Period in hours
                    strength = magnitude[peak] / np.max(magnitude)
                    
                    if strength > 0.3 and 2 <= period <= 168:  # 2 hours to 1 week
                        pattern = TemporalPattern(
                            pattern_type='cyclical',
                            pattern_strength=strength,
                            pattern_period=period,
                            pattern_confidence=strength,
                            pattern_description=f"Cyclical pattern with {period:.1f}h period",
                            detection_method='fft_analysis',
                            data_points=len(signal_values)
                        )
                        patterns.append(pattern)
        
        except Exception as e:
            self.logger.warning(f"Cyclical pattern detection failed: {e}")
        
        return patterns
    
    async def _detect_temporal_anomalies(self, time_series: pd.DataFrame) -> List[TemporalPattern]:
        """Detect temporal anomalies and unusual patterns"""
        patterns = []
        
        try:
            signal_values = time_series['signal_strength'].values
            if len(signal_values) < 10:
                return patterns
            
            # Z-score based anomaly detection
            z_scores = np.abs(stats.zscore(signal_values))
            anomaly_threshold = 2.5
            
            anomaly_indices = np.where(z_scores > anomaly_threshold)[0]
            
            if len(anomaly_indices) > 0:
                anomaly_strength = np.mean(z_scores[anomaly_indices]) / 3.0  # Normalize
                
                pattern = TemporalPattern(
                    pattern_type='anomaly',
                    pattern_strength=min(anomaly_strength, 1.0),
                    pattern_confidence=min(anomaly_strength, 1.0),
                    pattern_description=f"Statistical anomalies detected at {len(anomaly_indices)} points",
                    detection_method='zscore_analysis',
                    data_points=len(signal_values)
                )
                
                # Mark anomaly times
                anomaly_times = [
                    time_series.index[i].to_pydatetime() 
                    for i in anomaly_indices 
                    if i < len(time_series.index)
                ]
                pattern.peak_times = anomaly_times
                
                patterns.append(pattern)
        
        except Exception as e:
            self.logger.warning(f"Anomaly detection failed: {e}")
        
        return patterns
    
    async def _detect_emergence_patterns(self, time_series: pd.DataFrame) -> List[TemporalPattern]:
        """Detect trend emergence patterns"""
        patterns = []
        
        try:
            signal_values = time_series['signal_strength'].values
            if len(signal_values) < self.config['emergence_config']['min_data_points']:
                return patterns
            
            # Calculate velocity (rate of change)
            velocity = np.gradient(signal_values)
            
            # Calculate acceleration (rate of velocity change)
            acceleration = np.gradient(velocity)
            
            # Find emergence indicators
            emergence_score = self._calculate_emergence_score(signal_values, velocity, acceleration)
            
            if emergence_score > 0.5:
                pattern = TemporalPattern(
                    pattern_type='emergence',
                    pattern_strength=emergence_score,
                    pattern_confidence=emergence_score,
                    pattern_description="Trend emergence pattern detected",
                    emergence_velocity=np.mean(velocity[-6:]) if len(velocity) >= 6 else 0,
                    momentum_score=self._calculate_momentum_score(signal_values),
                    persistence_score=self._calculate_persistence_score(signal_values),
                    detection_method='velocity_acceleration_analysis',
                    data_points=len(signal_values)
                )
                
                # Find acceleration points
                accel_threshold = np.std(acceleration) * 1.5
                accel_points = np.where(acceleration > accel_threshold)[0]
                pattern.acceleration_points = [
                    time_series.index[i].to_pydatetime() 
                    for i in accel_points 
                    if i < len(time_series.index)
                ]
                
                patterns.append(pattern)
        
        except Exception as e:
            self.logger.warning(f"Emergence pattern detection failed: {e}")
        
        return patterns
    
    def _calculate_emergence_score(self, values: np.ndarray, velocity: np.ndarray, acceleration: np.ndarray) -> float:
        """Calculate overall emergence score"""
        try:
            # Recent growth trend
            recent_growth = np.mean(velocity[-6:]) if len(velocity) >= 6 else 0
            
            # Positive acceleration
            recent_accel = np.mean(acceleration[-3:]) if len(acceleration) >= 3 else 0
            
            # Sustained increase
            increasing_points = np.sum(velocity > 0) / len(velocity) if len(velocity) > 0 else 0
            
            # Overall signal strength growth
            if len(values) >= 10:
                recent_avg = np.mean(values[-5:])
                earlier_avg = np.mean(values[:5])
                growth_ratio = recent_avg / earlier_avg if earlier_avg > 0 else 1.0
            else:
                growth_ratio = 1.0
            
            # Combine factors
            emergence_score = (
                (recent_growth * 0.3) +
                (recent_accel * 0.2) +
                (increasing_points * 0.2) +
                (min(growth_ratio / 2.0, 1.0) * 0.3)
            )
            
            return min(emergence_score, 1.0)
        
        except:
            return 0.0
    
    def _calculate_momentum_score(self, values: np.ndarray) -> float:
        """Calculate current momentum score"""
        try:
            if len(values) < 6:
                return 0.0
            
            # Recent trend strength
            recent_values = values[-6:]
            x = np.arange(len(recent_values))
            slope, _, r_value, _, _ = stats.linregress(x, recent_values)
            
            momentum = abs(r_value) * (1 if slope > 0 else -1)
            return max(0, momentum)
        
        except:
            return 0.0
    
    def _calculate_persistence_score(self, values: np.ndarray) -> float:
        """Calculate pattern persistence score"""
        try:
            if len(values) < 10:
                return 0.0
            
            # Measure consistency of growth
            velocity = np.gradient(values)
            positive_velocity_ratio = np.sum(velocity > 0) / len(velocity)
            
            # Measure volatility (lower is more persistent)
            volatility = np.std(values) / np.mean(values) if np.mean(values) > 0 else 1.0
            persistence = positive_velocity_ratio * (1.0 - min(volatility, 1.0))
            
            return max(0, min(persistence, 1.0))
        
        except:
            return 0.0
    
    async def generate_emergence_signals(self, patterns: List[TemporalPattern]) -> List[TrendEmergenceSignal]:
        """Generate trend emergence signals from detected patterns"""
        emergence_signals = []
        
        for pattern in patterns:
            if pattern.pattern_type in ['emergence', 'trend'] and pattern.pattern_strength > 0.6:
                # Determine emergence stage
                stage = self._determine_emergence_stage(pattern)
                
                # Generate emergence signal
                signal = TrendEmergenceSignal(
                    trend_id=f"trend_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
                    emergence_score=pattern.pattern_strength,
                    emergence_stage=stage,
                    first_detected=pattern.detected_at,
                    current_velocity=pattern.emergence_velocity,
                    seasonal_component=0.0,  # Will be enhanced with seasonal analysis
                    trend_component=pattern.pattern_strength,
                    noise_level=1.0 - pattern.pattern_confidence
                )
                
                # Add forecasting
                forecast = await self._generate_short_term_forecast(pattern)
                signal.short_term_forecast = forecast['values']
                signal.confidence_intervals = forecast['confidence_intervals']
                
                emergence_signals.append(signal)
        
        self.analysis_stats['emergence_signals_generated'] += len(emergence_signals)
        return emergence_signals
    
    def _determine_emergence_stage(self, pattern: TemporalPattern) -> str:
        """Determine the emergence stage of a pattern"""
        if pattern.emergence_velocity < 0.2:
            return 'inception'
        elif pattern.emergence_velocity < 0.5:
            return 'growth'
        elif pattern.emergence_velocity < 0.8:
            return 'acceleration'
        else:
            return 'maturity'
    
    async def _generate_short_term_forecast(self, pattern: TemporalPattern) -> Dict:
        """Generate short-term forecast based on pattern"""
        try:
            # Simple exponential smoothing forecast
            forecast_horizon = 24  # 24 hours
            
            # Mock forecast for now (would use actual time series data)
            base_value = pattern.pattern_strength
            growth_rate = pattern.emergence_velocity / 10.0
            
            forecast_values = []
            confidence_lower = []
            confidence_upper = []
            
            for i in range(forecast_horizon):
                # Simple growth projection with decay
                value = base_value * (1 + growth_rate) ** i * np.exp(-i / 48.0)
                forecast_values.append(value)
                
                # Simple confidence intervals
                uncertainty = 0.1 * i / forecast_horizon
                confidence_lower.append(value * (1 - uncertainty))
                confidence_upper.append(value * (1 + uncertainty))
            
            return {
                'values': forecast_values,
                'confidence_intervals': {
                    'lower': confidence_lower,
                    'upper': confidence_upper
                }
            }
        
        except Exception as e:
            self.logger.warning(f"Forecast generation failed: {e}")
            return {'values': [], 'confidence_intervals': {}}
    
    def _update_pattern_stats(self, patterns_detected: int, processing_time: float):
        """Update performance statistics"""
        self.analysis_stats['patterns_detected'] += patterns_detected
        
        # Update average processing time
        current_avg = self.analysis_stats['avg_processing_time']
        total_analyses = self.analysis_stats['patterns_detected']
        if total_analyses > 0:
            self.analysis_stats['avg_processing_time'] = (
                (current_avg * (total_analyses - patterns_detected) + processing_time) / total_analyses
            )
        else:
            self.analysis_stats['avg_processing_time'] = processing_time
    
    def get_performance_stats(self) -> Dict:
        """Get current performance statistics"""
        return self.analysis_stats.copy()
    
    async def predict_trend_emergence(self, historical_signals: List[Dict], forecast_hours: int = 72) -> Dict:
        """Predict trend emergence based on historical patterns"""
        try:
            # Analyze historical patterns
            patterns = await self.analyze_temporal_patterns(historical_signals)
            
            # Generate emergence predictions
            predictions = {
                'emergence_probability': 0.0,
                'predicted_peak_time': None,
                'confidence_level': 0.0,
                'contributing_patterns': [],
                'risk_factors': []
            }
            
            # Calculate emergence probability
            emergence_patterns = [p for p in patterns if p.pattern_type == 'emergence']
            if emergence_patterns:
                avg_emergence_strength = np.mean([p.pattern_strength for p in emergence_patterns])
                predictions['emergence_probability'] = avg_emergence_strength
                predictions['contributing_patterns'] = [p.pattern_description for p in emergence_patterns]
            
            # Estimate confidence based on data quality and pattern consistency
            if patterns:
                pattern_consistency = np.std([p.pattern_confidence for p in patterns])
                predictions['confidence_level'] = max(0, 1.0 - pattern_consistency)
            
            return predictions
        
        except Exception as e:
            self.logger.error(f"Trend emergence prediction failed: {e}")
            return {'emergence_probability': 0.0, 'confidence_level': 0.0}

# Global temporal engine instance
_temporal_engine = None

def get_temporal_engine() -> AdvancedTemporalPatternEngine:
    """Get or create the global temporal pattern engine instance"""
    global _temporal_engine
    if _temporal_engine is None:
        _temporal_engine = AdvancedTemporalPatternEngine()
    return _temporal_engine 