"""
Luciq Test Configuration
Phase 4 Testing & Validation - Pytest Configuration

Global test fixtures and configuration
"""

import pytest
import asyncio
import tempfile
import os
from unittest.mock import Mock, AsyncMock

# Configure asyncio for pytest
@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture
def temp_database():
    """Create a temporary database for testing"""
    with tempfile.NamedTemporaryFile(suffix='.db', delete=False) as f:
        db_path = f.name
    yield db_path
    # Cleanup
    if os.path.exists(db_path):
        os.unlink(db_path)

@pytest.fixture
def mock_reddit_client():
    """Mock Reddit client for testing"""
    mock_client = Mock()
    mock_client.get_subreddit_posts = AsyncMock(return_value=[])
    mock_client.business_keywords = ['startup', 'business', 'entrepreneur']
    return mock_client

@pytest.fixture
def mock_database_service():
    """Mock database service for testing"""
    mock_db = Mock()
    mock_db.create_user = AsyncMock(return_value=1)
    mock_db.get_user_by_username = AsyncMock(return_value=None)
    mock_db.save_pain_point = AsyncMock()
    mock_db.save_discovery_session = AsyncMock()
    return mock_db

# Test markers
pytest_plugins = []

def pytest_configure(config):
    """Configure pytest markers"""
    config.addinivalue_line(
        "markers", "asyncio: mark test as async"
    )
    config.addinivalue_line(
        "markers", "integration: mark test as integration test"
    )
    config.addinivalue_line(
        "markers", "performance: mark test as performance test"
    )
    config.addinivalue_line(
        "markers", "unit: mark test as unit test"
    ) 