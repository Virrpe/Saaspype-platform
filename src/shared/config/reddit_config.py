"""
Reddit API Configuration
Manages Reddit API credentials and settings for production use
"""

import os
from typing import Optional

class RedditConfig:
    """Reddit API configuration settings"""
    
    def __init__(self):
        # Reddit API credentials (set these in environment variables for production)
        self.client_id = os.getenv('REDDIT_CLIENT_ID')
        self.client_secret = os.getenv('REDDIT_CLIENT_SECRET')
        self.user_agent = os.getenv('REDDIT_USER_AGENT', 'Luciq:trend-discovery:v2.1 (by /u/luciq_bot)')
        
        # Rate limiting settings
        self.requests_per_minute = int(os.getenv('REDDIT_RATE_LIMIT', '60'))
        self.request_timeout = int(os.getenv('REDDIT_TIMEOUT', '10'))
        
        # API endpoints
        self.oauth_url = "https://oauth.reddit.com"
        self.auth_url = "https://www.reddit.com/api/v1/access_token"
        
        # Fallback settings
        self.use_fallback_api = os.getenv('REDDIT_USE_FALLBACK', 'true').lower() == 'true'
        self.fallback_url = "https://www.reddit.com"
    
    def is_configured(self) -> bool:
        """Check if Reddit API credentials are properly configured"""
        return bool(self.client_id and self.client_secret)
    
    def get_credentials_status(self) -> dict:
        """Get status of Reddit API credentials configuration"""
        return {
            'client_id_set': bool(self.client_id),
            'client_secret_set': bool(self.client_secret),
            'user_agent': self.user_agent,
            'configured': self.is_configured(),
            'fallback_enabled': self.use_fallback_api
        }

# Global configuration instance
reddit_config = RedditConfig()

# Helper function to get setup instructions
def get_reddit_api_setup_instructions() -> str:
    """Get instructions for setting up Reddit API credentials"""
    return """
Reddit API Setup Instructions:

1. Create a Reddit App:
   - Go to https://www.reddit.com/prefs/apps
   - Click "Create App" or "Create Another App"
   - Choose "web app" type
   - Set redirect URI to: http://localhost:8000/auth/reddit/callback
   - Note your client ID (under the app name) and client secret

2. Set Environment Variables:
   For Windows (PowerShell):
   $env:REDDIT_CLIENT_ID="your_client_id"
   $env:REDDIT_CLIENT_SECRET="your_client_secret"
   $env:REDDIT_USER_AGENT="YourApp:v1.0 (by /u/yourusername)"

   For Linux/Mac:
   export REDDIT_CLIENT_ID="your_client_id"
   export REDDIT_CLIENT_SECRET="your_client_secret"
   export REDDIT_USER_AGENT="YourApp:v1.0 (by /u/yourusername)"

3. Restart the Luciq API server

For development/testing, the system will fall back to public Reddit JSON API.
For production, proper OAuth2 credentials are recommended for better rate limits.
""" 