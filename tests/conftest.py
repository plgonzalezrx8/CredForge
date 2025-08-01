"""
Test configuration and fixtures for CredForge tests.
"""
import os
import tempfile
import pytest
from pathlib import Path

@pytest.fixture
def temp_dir():
    """Create a temporary directory for test files."""
    with tempfile.TemporaryDirectory() as temp_dir:
        yield Path(temp_dir)

@pytest.fixture
def sample_credentials():
    """Sample credentials for testing."""
    return [
        "user1:hash1:password1",
        "user2:hash2:password2",
        "user3:hash3:password3",
        "user4:hash4:password4",
        "user5:hash5:password5",
    ]

@pytest.fixture
def sample_ntds_data():
    """Sample NTDS data for testing."""
    return [
        "user1:1001:hash1:hash1_nt:disabled:false:false:false",
        "user2:1002:hash2:hash2_nt:enabled:false:false:false",
        "user3:1003:hash3:hash3_nt:disabled:false:false:false",
        "user4:1004:hash4:hash4_nt:enabled:false:false:false",
    ]

@pytest.fixture
def sample_passwords():
    """Sample passwords for testing."""
    return [
        "password1",
        "password2",
        "password3",
        "password1",  # Duplicate
        "password4",
        "password2",  # Duplicate
    ]
