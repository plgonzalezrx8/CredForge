"""
Simple test runner to help diagnose test execution issues.
"""
import sys
import os
import pytest

def main():
    print("Running tests with Python:", sys.executable)
    print("Python version:", sys.version)
    print("Current working directory:", os.getcwd())
    
    # Add the current directory to the path
    sys.path.insert(0, os.getcwd())
    
    # Try to run pytest programmatically
    print("\nRunning pytest...")
    result = pytest.main(["-v", "--tb=short", "tests"])
    print("\nTest result code:", result)
    return result

if __name__ == "__main__":
    sys.exit(main())
