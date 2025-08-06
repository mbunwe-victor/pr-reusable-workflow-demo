import pytest
import os
import tempfile
from pathlib import Path


@pytest.fixture(scope="session")
def temp_workflow_dir():
    """Create a temporary directory for workflow testing."""
    with tempfile.TemporaryDirectory() as temp_dir:
        workflow_dir = Path(temp_dir) / ".github" / "workflows"
        workflow_dir.mkdir(parents=True, exist_ok=True)
        yield temp_dir


@pytest.fixture
def clean_environment():
    """Ensure clean environment for each test."""
    # Save original environment
    original_env = dict(os.environ)
    
    yield
    
    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)