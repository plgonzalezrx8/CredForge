"""
A simple test file to verify basic test execution.
"""

def test_import():
    """Test if we can import the credforge package."""
    try:
        import credforge
        print("SUCCESS: Imported credforge package")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import credforge: {e}")
        return False

def test_import_module():
    """Test if we can import a module from the credforge package."""
    try:
        from credforge import split_credentials
        print("SUCCESS: Imported credforge.split_credentials")
        return True
    except ImportError as e:
        print(f"ERROR: Failed to import credforge.split_credentials: {e}")
        return False

if __name__ == "__main__":
    print("Running simple import tests...")
    test_import()
    test_import_module()
