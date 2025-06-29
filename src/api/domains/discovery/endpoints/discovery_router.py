#!/usr/bin/env python3
"""
Discovery Router - SaaS Idea Discovery Endpoints
Handles all discovery-related API endpoints
"""

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from typing import Optional, Dict, Any
import logging

from src.api.domains.auth.endpoints.auth import get_current_user
from src.api.domains.discovery.models.requests import DiscoveryRequest, SaveIdeaRequest
from src.api.domains.discovery.services.discovery_service import discovery_service
from src.api.domains.discovery.services.ideas_service import ideas_service

logger = logging.getLogger(__name__)

# Create router with discovery prefix
router = APIRouter(prefix="/api", tags=["Discovery"])

@router.post("/discover")
async def discover_opportunities(
    request: DiscoveryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Main discovery endpoint - find SaaS opportunities from Reddit"""
    logger.info(f"Discovery request from user {current_user.get('email', 'Unknown')}")
    
    try:
        # Process discovery request
        result = await discovery_service.discover_opportunities(request)
        
        # Log successful discovery
        logger.info(f"Discovery completed: {len(result.get('opportunities', []))} opportunities found")
        
        return result
        
    except Exception as e:
        logger.error(f"Discovery failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Discovery failed: {str(e)}")

@router.get("/discovery-history")
async def get_discovery_history(current_user: dict = Depends(get_current_user)):
    """Get user's discovery history"""
    try:
        history = await discovery_service.get_user_discovery_history(current_user["user_id"])
        return {"history": history}
    except Exception as e:
        logger.error(f"Failed to get discovery history: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve discovery history")

@router.get("/system-ideas")
async def get_system_ideas():
    """Get system-generated ideas (public endpoint)"""
    try:
        # Read directly from overnight discovery data
        from pathlib import Path
        import json
        
        data_dir = Path("overnight_discovery_data")
        all_ideas = []
        
        if data_dir.exists():
            # Get all cycle files
            cycle_files = sorted(data_dir.glob("cycle_*.json"))
            
            for cycle_file in cycle_files:
                try:
                    with open(cycle_file, 'r', encoding='utf-8') as f:
                        cycle_data = json.load(f)
                        
                    # Extract ideas from cycle data
                    if 'ideas' in cycle_data:
                        for idea in cycle_data['ideas']:
                            # Standardize the idea format
                            standardized_idea = {
                                'solution': idea.get('solution', idea.get('title', 'Unknown Solution')),
                                'problem': idea.get('problem', idea.get('description', 'Unknown Problem')),
                                'source': idea.get('source', 'entrepreneur'),
                                'score': idea.get('score', 3),
                                'reddit_url': idea.get('reddit_url', ''),
                                'reddit_score': idea.get('reddit_score', 0),
                                'discovery_type': idea.get('discovery_type', 'reddit_scraping'),
                                'cycle_file': cycle_file.name
                            }
                            all_ideas.append(standardized_idea)
                            
                except Exception as e:
                    logger.warning(f"Failed to read cycle file {cycle_file}: {e}")
                    continue
        
        # Also read from bulletproof analysis files
        bulletproof_files = [
            "bulletproof_intelligence_analysis_20250606_005321.json",
            "bulletproof_intelligence_analysis_20250606_010505.json",
            "fixed_sources_results_20250606_004255.json",
            "super_fixed_scrapers_20250606_004420.json"
        ]
        
        for bulletproof_file in bulletproof_files:
            try:
                if Path(bulletproof_file).exists():
                    with open(bulletproof_file, 'r', encoding='utf-8') as f:
                        bulletproof_data = json.load(f)
                    
                    # Extract ideas from bulletproof data
                    if isinstance(bulletproof_data, dict):
                        for source, source_data in bulletproof_data.items():
                            if isinstance(source_data, dict) and 'ideas' in source_data:
                                for idea in source_data['ideas']:
                                    standardized_idea = {
                                        'solution': idea.get('solution', idea.get('title', 'Unknown Solution')),
                                        'problem': idea.get('problem', idea.get('description', 'Unknown Problem')),
                                        'source': source,
                                        'score': idea.get('score', 3),
                                        'reddit_url': idea.get('url', ''),
                                        'reddit_score': idea.get('reddit_score', 0),
                                        'discovery_type': 'bulletproof_analysis',
                                        'cycle_file': bulletproof_file
                                    }
                                    all_ideas.append(standardized_idea)
                                    
            except Exception as e:
                logger.warning(f"Failed to read bulletproof file {bulletproof_file}: {e}")
                continue
        
        # Return results
        return {
            "success": True,
            "ideas": all_ideas,
            "count": len(all_ideas),
            "sources": list(set(idea['source'] for idea in all_ideas)),
            "discovery_types": list(set(idea['discovery_type'] for idea in all_ideas))
        }
        
    except Exception as e:
        logger.error(f"Failed to get system ideas: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to get system ideas: {str(e)}")

@router.post("/save-idea")
async def save_idea(
    request: SaveIdeaRequest,
    current_user: dict = Depends(get_current_user)
):
    """Save an idea to user's personal collection"""
    try:
        # Save idea with user association
        idea_id = await ideas_service.save_user_idea(
            user_id=current_user["user_id"],
            idea_data=request.dict()
        )
        
        logger.info(f"Idea saved by user {current_user.get('email')}: {idea_id}")
        
        return {
            "success": True,
            "message": "Idea saved successfully",
            "idea_id": idea_id
        }
        
    except Exception as e:
        logger.error(f"Failed to save idea: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save idea: {str(e)}")

@router.get("/my-ideas")
async def get_my_ideas(current_user: dict = Depends(get_current_user)):
    """Get user's saved ideas"""
    try:
        ideas = await ideas_service.get_user_ideas(current_user["user_id"])
        return {"ideas": ideas}
    except Exception as e:
        logger.error(f"Failed to get user ideas: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to retrieve user ideas")

@router.post("/discover/enhanced")
async def enhanced_discovery(
    request: DiscoveryRequest,
    current_user: dict = Depends(get_current_user)
):
    """Enhanced discovery with advanced analysis"""
    logger.info(f"Enhanced discovery request from user {current_user.get('email', 'Unknown')}")
    
    try:
        # Use enhanced discovery service
        result = await discovery_service.enhanced_discovery(request)
        
        # Add performance metrics
        result["enhanced"] = True
        result["user_id"] = current_user["user_id"]
        
        logger.info(f"Enhanced discovery completed: {len(result.get('opportunities', []))} opportunities")
        
        return result
        
    except Exception as e:
        logger.error(f"Enhanced discovery failed: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Enhanced discovery failed: {str(e)}")

@router.get("/discovery/subreddit/{subreddit_name}")
async def discover_subreddit(
    subreddit_name: str,
    limit: Optional[int] = 10,
    current_user: dict = Depends(get_current_user)
):
    """Discover opportunities from a specific subreddit"""
    logger.info(f"Subreddit discovery request: r/{subreddit_name} from user {current_user.get('email', 'Unknown')}")
    
    try:
        # Create discovery request for specific subreddit
        from src.api.domains.discovery.models.requests import DiscoveryRequest
        request = DiscoveryRequest(
            subreddits=[subreddit_name],
            limit=limit,
            analysis_depth="standard"
        )
        
        # Process discovery request
        result = await discovery_service.discover_opportunities(request)
        
        # Add subreddit-specific metadata
        result["subreddit"] = subreddit_name
        result["request_type"] = "subreddit_specific"
        
        logger.info(f"Subreddit discovery completed: {len(result.get('opportunities', []))} opportunities from r/{subreddit_name}")
        
        return result
        
    except Exception as e:
        logger.error(f"Subreddit discovery failed for r/{subreddit_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Subreddit discovery failed: {str(e)}")

@router.get("/discovery/subreddit/{subreddit_name}/quick")
async def quick_subreddit_discovery(subreddit_name: str):
    """Quick subreddit discovery (no auth required for testing)"""
    logger.info(f"Quick subreddit discovery: r/{subreddit_name}")
    
    try:
        # Use the overnight discovery system for quick results
        from overnight_discovery_cycle import OvernightDiscoveryEngine
        
        engine = OvernightDiscoveryEngine()
        ideas = await engine.discover_subreddit_ideas([subreddit_name], limit=5)
        
        return {
            "success": True,
            "subreddit": subreddit_name,
            "ideas": ideas,
            "count": len(ideas),
            "source": "overnight_discovery_engine"
        }
        
    except Exception as e:
        logger.error(f"Quick subreddit discovery failed for r/{subreddit_name}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Quick discovery failed: {str(e)}")

@router.get("/discovery/status")
async def discovery_status():
    """Get discovery system status (public endpoint)"""
    try:
        # Check if overnight discovery data exists
        from pathlib import Path
        data_dir = Path("overnight_discovery_data")
        
        if data_dir.exists():
            cycle_files = list(data_dir.glob("cycle_*.json"))
            latest_cycle = max(cycle_files, key=lambda x: x.stat().st_mtime) if cycle_files else None
            
            status = {
                "system_status": "operational",
                "data_directory": str(data_dir),
                "total_cycles": len(cycle_files),
                "latest_cycle": latest_cycle.name if latest_cycle else None,
                "discovery_engine": "overnight_discovery_system"
            }
        else:
            status = {
                "system_status": "no_data",
                "message": "No discovery data found"
            }
        
        return status
        
    except Exception as e:
        logger.error(f"Failed to get discovery status: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to get system status") 