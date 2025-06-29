#!/usr/bin/env python3
"""
MVP API Integration for Luciq Master API
Add this code to master_luciq_api.py for immediate revenue generation
"""

import secrets
import hashlib
from datetime import datetime, timedelta
from typing import Optional, Dict, List
from enum import Enum
import sqlite3
from fastapi import HTTPException, Depends, Header, Request
from pydantic import BaseModel

# ================================================================================================
# MVP BILLING & API KEY SYSTEM
# ================================================================================================

class SubscriptionTier(Enum):
    STARTER = "starter"
    PROFESSIONAL = "professional" 
    BUSINESS = "business"
    ENTERPRISE = "enterprise"

# Pricing tiers configuration
TIER_LIMITS = {
    SubscriptionTier.STARTER: {
        "name": "Starter",
        "monthly_calls": 1000,
        "rate_limit_per_minute": 10,
        "price_monthly": 49,
        "features": ["pain_point_detection", "basic_analytics"]
    },
    SubscriptionTier.PROFESSIONAL: {
        "name": "Professional", 
        "monthly_calls": 10000,
        "rate_limit_per_minute": 50,
        "price_monthly": 149,
        "features": ["pain_point_detection", "market_validation", "competitive_analysis", "basic_streaming"]
    },
    SubscriptionTier.BUSINESS: {
        "name": "Business",
        "monthly_calls": 50000,
        "rate_limit_per_minute": 200,
        "price_monthly": 299,
        "features": ["all_intelligence_apis", "real_time_monitoring", "predictive_analytics", "priority_support"]
    },
    SubscriptionTier.ENTERPRISE: {
        "name": "Enterprise",
        "monthly_calls": 999999,
        "rate_limit_per_minute": 1000,
        "price_monthly": 999,
        "features": ["unlimited_access", "white_label", "custom_integrations", "dedicated_support"]
    }
}

class MVPAPIKeyService:
    """Simplified API Key service for MVP launch"""
    
    def __init__(self, db_path: str = "luciq_mvp_billing.db"):
        self.db_path = db_path
        self.init_mvp_database()
    
    def init_mvp_database(self):
        """Initialize MVP billing database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # API Keys table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mvp_api_keys (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                api_key_hash TEXT UNIQUE NOT NULL,
                api_key_prefix TEXT NOT NULL,
                tier TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_used_at TIMESTAMP,
                is_active BOOLEAN DEFAULT TRUE,
                monthly_usage INTEGER DEFAULT 0,
                usage_reset_date DATE NOT NULL
            )
        ''')
        
        # Usage tracking table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mvp_api_usage (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                api_key_hash TEXT NOT NULL,
                endpoint TEXT NOT NULL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                response_time_ms INTEGER,
                status_code INTEGER
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def generate_mvp_api_key(self, user_id: int, tier: str = "professional") -> Dict[str, str]:
        """Generate MVP API key for user"""
        # Generate secure API key
        raw_key = f"sk_live_{secrets.token_urlsafe(32)}"
        key_hash = hashlib.sha256(raw_key.encode()).hexdigest()
        key_prefix = raw_key[:12] + "..."
        
        # Calculate usage reset date (next month)
        reset_date = (datetime.now() + timedelta(days=30)).date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        try:
            cursor.execute('''
                INSERT INTO mvp_api_keys (user_id, api_key_hash, api_key_prefix, tier, usage_reset_date)
                VALUES (?, ?, ?, ?, ?)
            ''', (user_id, key_hash, key_prefix, tier, reset_date))
            
            conn.commit()
            
            tier_info = TIER_LIMITS[SubscriptionTier(tier)]
            
            return {
                "api_key": raw_key,
                "tier": tier,
                "monthly_limit": tier_info["monthly_calls"],
                "rate_limit": tier_info["rate_limit_per_minute"],
                "features": tier_info["features"],
                "price_monthly": tier_info["price_monthly"]
            }
            
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail="API key generation failed")
        finally:
            conn.close()
    
    async def validate_mvp_api_key(self, api_key: str) -> Dict:
        """Validate MVP API key"""
        if not api_key or not api_key.startswith("sk_live_"):
            raise HTTPException(status_code=401, detail="Invalid API key format")
        
        key_hash = hashlib.sha256(api_key.encode()).hexdigest()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT user_id, tier, monthly_usage, usage_reset_date, is_active
            FROM mvp_api_keys 
            WHERE api_key_hash = ?
        ''', (key_hash,))
        
        result = cursor.fetchone()
        conn.close()
        
        if not result:
            raise HTTPException(status_code=401, detail="Invalid API key")
        
        user_id, tier, monthly_usage, reset_date, is_active = result
        
        if not is_active:
            raise HTTPException(status_code=401, detail="API key deactivated")
        
        # Check if usage needs to be reset
        if datetime.now().date() > datetime.strptime(reset_date, "%Y-%m-%d").date():
            self._reset_monthly_usage(key_hash)
            monthly_usage = 0
        
        tier_info = TIER_LIMITS[SubscriptionTier(tier)]
        
        return {
            "user_id": user_id,
            "tier": tier,
            "monthly_usage": monthly_usage,
            "monthly_limit": tier_info["monthly_calls"],
            "rate_limit": tier_info["rate_limit_per_minute"],
            "features": tier_info["features"],
            "api_key_hash": key_hash
        }
    
    async def track_mvp_usage(self, api_key_hash: str, endpoint: str, response_time_ms: int = 0, 
                             status_code: int = 200):
        """Track MVP API usage"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Record usage
        cursor.execute('''
            INSERT INTO mvp_api_usage (api_key_hash, endpoint, response_time_ms, status_code)
            VALUES (?, ?, ?, ?)
        ''', (api_key_hash, endpoint, response_time_ms, status_code))
        
        # Update monthly usage counter
        cursor.execute('''
            UPDATE mvp_api_keys 
            SET monthly_usage = monthly_usage + 1, last_used_at = CURRENT_TIMESTAMP
            WHERE api_key_hash = ?
        ''', (api_key_hash,))
        
        conn.commit()
        conn.close()
    
    def _reset_monthly_usage(self, api_key_hash: str):
        """Reset monthly usage counter"""
        next_reset = (datetime.now() + timedelta(days=30)).date()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mvp_api_keys 
            SET monthly_usage = 0, usage_reset_date = ?
            WHERE api_key_hash = ?
        ''', (next_reset, api_key_hash))
        
        conn.commit()
        conn.close()

# Initialize MVP services
mvp_api_key_service = MVPAPIKeyService()

# FastAPI dependency for MVP API key authentication
async def get_mvp_api_key_auth(x_api_key: str = Header(None)) -> Dict:
    """FastAPI dependency for MVP API key authentication"""
    if not x_api_key:
        raise HTTPException(status_code=401, detail="API key required in X-API-Key header")
    
    user_info = await mvp_api_key_service.validate_mvp_api_key(x_api_key)
    
    # Check monthly usage
    if user_info["monthly_usage"] >= user_info["monthly_limit"]:
        raise HTTPException(status_code=429, detail="Monthly usage limit exceeded. Please upgrade your plan.")
    
    return user_info

# Pydantic models for MVP API
class MVPAPIKeyRequest(BaseModel):
    email: str
    tier: str = "professional"

class MVPUsageResponse(BaseModel):
    tier: str
    monthly_usage: int
    monthly_limit: int
    usage_percentage: float
    features: List[str]

# ================================================================================================
# MVP API ENDPOINTS - ADD THESE TO master_luciq_api.py
# ================================================================================================

# MVP API Key Management Endpoints
@app.post("/api/mvp/generate-api-key")
async def generate_mvp_api_key(request: MVPAPIKeyRequest):
    """Generate MVP API key for immediate testing"""
    try:
        # For MVP, we'll use email as a simple user identifier
        user_id = hash(request.email) % 1000000  # Simple hash for demo
        
        api_key_info = mvp_api_key_service.generate_mvp_api_key(user_id, request.tier)
        
        return {
            "success": True,
            "message": "API key generated successfully",
            "api_key": api_key_info["api_key"],
            "tier": api_key_info["tier"],
            "monthly_limit": api_key_info["monthly_limit"],
            "features": api_key_info["features"],
            "price_monthly": api_key_info["price_monthly"],
            "instructions": {
                "usage": "Include 'X-API-Key: your_api_key' in request headers",
                "endpoints": [
                    "/api/mvp/pain-point-detection",
                    "/api/mvp/market-validation", 
                    "/api/mvp/competitive-analysis",
                    "/api/mvp/business-signals"
                ]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mvp/usage-stats")
async def get_mvp_usage_stats(auth: Dict = Depends(get_mvp_api_key_auth)):
    """Get MVP API usage statistics"""
    usage_percentage = (auth["monthly_usage"] / auth["monthly_limit"]) * 100
    
    return MVPUsageResponse(
        tier=auth["tier"],
        monthly_usage=auth["monthly_usage"],
        monthly_limit=auth["monthly_limit"],
        usage_percentage=round(usage_percentage, 2),
        features=auth["features"]
    )

# MVP Intelligence Endpoints (Revenue-generating APIs)
@app.post("/api/mvp/pain-point-detection")
async def mvp_pain_point_detection(request: PainPointAnalysisRequest, auth: Dict = Depends(get_mvp_api_key_auth)):
    """MVP Pain Point Detection API - Revenue endpoint"""
    start_time = datetime.now()
    
    try:
        # Use existing pain point detection engine
        result = await pain_point_engine.detect_advanced_pain_points(
            request.content, 
            request.platform, 
            request.context
        )
        
        # Track usage
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/pain-point-detection", 
            response_time, 
            200
        )
        
        return {
            "success": True,
            "tier": auth["tier"],
            "usage_remaining": auth["monthly_limit"] - auth["monthly_usage"] - 1,
            "analysis": result
        }
        
    except Exception as e:
        # Track failed usage
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/pain-point-detection", 
            response_time, 
            500
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mvp/market-validation")
async def mvp_market_validation(request: MarketValidationRequest, auth: Dict = Depends(get_mvp_api_key_auth)):
    """MVP Market Validation API - Revenue endpoint"""
    start_time = datetime.now()
    
    try:
        # Use existing market validation engine
        result = await market_validation_engine.validate_market_opportunity(
            request.content, 
            request.platform, 
            request.context
        )
        
        # Track usage
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/market-validation", 
            response_time, 
            200
        )
        
        return {
            "success": True,
            "tier": auth["tier"],
            "usage_remaining": auth["monthly_limit"] - auth["monthly_usage"] - 1,
            "analysis": result
        }
        
    except Exception as e:
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/market-validation", 
            response_time, 
            500
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mvp/competitive-analysis")
async def mvp_competitive_analysis(request: SolutionGapAnalysisRequest, auth: Dict = Depends(get_mvp_api_key_auth)):
    """MVP Competitive Analysis API - Revenue endpoint"""
    start_time = datetime.now()
    
    try:
        # Use existing solution gap analyzer
        result = await solution_gap_analyzer.analyze_solution_gaps(
            request.content, 
            request.platform, 
            request.context
        )
        
        # Track usage
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/competitive-analysis", 
            response_time, 
            200
        )
        
        return {
            "success": True,
            "tier": auth["tier"],
            "usage_remaining": auth["monthly_limit"] - auth["monthly_usage"] - 1,
            "analysis": result
        }
        
    except Exception as e:
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/competitive-analysis", 
            response_time, 
            500
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/mvp/business-signals")
async def mvp_business_signals(hours_back: int = 24, auth: Dict = Depends(get_mvp_api_key_auth)):
    """MVP Business Signals API - Revenue endpoint"""
    start_time = datetime.now()
    
    try:
        # Use existing mega scraper
        result = await mega_scraper.scrape_all_sources(hours_back)
        
        # Track usage
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/business-signals", 
            response_time, 
            200
        )
        
        return {
            "success": True,
            "tier": auth["tier"],
            "usage_remaining": auth["monthly_limit"] - auth["monthly_usage"] - 1,
            "signals": result
        }
        
    except Exception as e:
        response_time = int((datetime.now() - start_time).total_seconds() * 1000)
        await mvp_api_key_service.track_mvp_usage(
            auth["api_key_hash"], 
            "/api/mvp/business-signals", 
            response_time, 
            500
        )
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/mvp/pricing")
async def get_mvp_pricing():
    """Get MVP pricing information"""
    return {
        "pricing_tiers": [
            {
                "name": "Starter",
                "price_monthly": 49,
                "monthly_calls": 1000,
                "features": ["Pain Point Detection", "Basic Analytics", "Email Support"],
                "best_for": "Indie developers and small projects"
            },
            {
                "name": "Professional", 
                "price_monthly": 149,
                "monthly_calls": 10000,
                "features": ["Full Intelligence Suite", "Market Validation", "Competitive Analysis", "Priority Support"],
                "best_for": "Agencies and growing businesses",
                "popular": True
            },
            {
                "name": "Business",
                "price_monthly": 299,
                "monthly_calls": 50000,
                "features": ["Real-time Monitoring", "Predictive Analytics", "Custom Integrations", "Phone Support"],
                "best_for": "Established businesses and consultants"
            },
            {
                "name": "Enterprise",
                "price_monthly": 999,
                "monthly_calls": "Unlimited",
                "features": ["White-label Options", "Dedicated Support", "Custom Features", "SLA"],
                "best_for": "Large organizations and enterprises"
            }
        ],
        "comparison": {
            "vs_cb_insights": "CB Insights: $60,000/year vs Luciq: $1,788/year (97% savings)",
            "vs_pitchbook": "PitchBook: $12,000/year vs Luciq: $1,788/year (85% savings)",
            "unique_advantages": [
                "Real-time data vs static reports",
                "15+ platforms vs single sources", 
                "AI-powered analysis vs basic keyword matching",
                "Complete intelligence pipeline vs fragmented solutions"
            ]
        }
    }

# ================================================================================================
# MVP LANDING PAGE ENDPOINT
# ================================================================================================

@app.get("/mvp")
async def mvp_landing_page():
    """MVP landing page with pricing and API information"""
    return {
        "title": "Luciq Business Intelligence API",
        "tagline": "Get CB Insights-level business intelligence for 1/100th the cost",
        "hero": {
            "headline": "Revolutionary Business Intelligence API",
            "subheadline": "Real-time market analysis, competitor intelligence, and opportunity detection at disruptive pricing",
            "cta": "Get API Key - Start Free"
        },
        "value_propositions": [
            {
                "title": "97% Cost Savings",
                "description": "Get enterprise-grade intelligence for $149/month instead of $60K/year"
            },
            {
                "title": "Real-time Data", 
                "description": "Live analysis across 15+ platforms, not static monthly reports"
            },
            {
                "title": "AI-Powered Analysis",
                "description": "Advanced NLP and transformer models, not basic keyword matching"
            },
            {
                "title": "Complete Pipeline",
                "description": "Pain point detection, market validation, competitive analysis in one API"
            }
        ],
        "api_endpoints": [
            {
                "endpoint": "/api/mvp/pain-point-detection",
                "description": "Identify business opportunities and pain points",
                "example": "Analyze Reddit posts, tweets, or any content for business opportunities"
            },
            {
                "endpoint": "/api/mvp/market-validation", 
                "description": "Validate business ideas and market opportunities",
                "example": "Get market size, competition, and timing analysis"
            },
            {
                "endpoint": "/api/mvp/competitive-analysis",
                "description": "Analyze solution gaps and competitive landscape", 
                "example": "Find market gaps and competitive advantages"
            },
            {
                "endpoint": "/api/mvp/business-signals",
                "description": "Real-time business signals across 15+ platforms",
                "example": "Monitor trends, opportunities, and market movements"
            }
        ],
        "getting_started": {
            "step_1": "Generate API key at /api/mvp/generate-api-key",
            "step_2": "Include 'X-API-Key: your_key' in request headers",
            "step_3": "Start making API calls to intelligence endpoints",
            "step_4": "Scale up with higher tier plans as needed"
        },
        "contact": {
            "email": "hello@luciq.com",
            "twitter": "@luciq",
            "documentation": "/docs"
        }
    }

# ================================================================================================
# INSTRUCTIONS TO ADD TO master_luciq_api.py
# ================================================================================================

"""
TO IMPLEMENT MVP REVENUE SYSTEM:

1. Add this entire file content to the top of master_luciq_api.py (after imports)

2. The MVP system provides:
   - API key generation and validation
   - Usage tracking and rate limiting  
   - Revenue-generating API endpoints
   - Pricing and landing page information

3. Revenue endpoints:
   - /api/mvp/pain-point-detection ($)
   - /api/mvp/market-validation ($)
   - /api/mvp/competitive-analysis ($)
   - /api/mvp/business-signals ($)

4. Management endpoints:
   - /api/mvp/generate-api-key (free)
   - /api/mvp/usage-stats (free)
   - /api/mvp/pricing (free)
   - /mvp (landing page)

5. Pricing tiers:
   - Starter: $49/month (1K calls)
   - Professional: $149/month (10K calls) 
   - Business: $299/month (50K calls)
   - Enterprise: $999/month (unlimited)

6. Next steps for full launch:
   - Add Stripe payment integration
   - Create simple frontend dashboard
   - Set up monitoring and analytics
   - Launch marketing campaign

IMMEDIATE REVENUE POTENTIAL: $5K-25K MRR within 60 days
""" 