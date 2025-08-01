import sys
import os

print("Python version:", sys.version)
print("\nPython path:")
for p in sys.path:
    print(f"  {p}")

print("\nCurrent working directory:", os.getcwd())
print("\nContents of project directory:")
for item in os.listdir():
    print(f"  {item}")

print("\nAttempting to import from credforge package:")
try:
    from credforge import __version__
    print(f"Successfully imported credforge.__version__: {__version__}")
except ImportError as e:
    print(f"Error importing credforge: {e}")

print("\nAttempting to import a module:")
try:
    from credforge import split_credentials
    print("Successfully imported credforge.split_credentials")
except ImportError as e:
    print(f"Error importing credforge.split_credentials: {e}")
    print("\nTroubleshooting:")
    print("1. Ensure you're running from the project root directory")
    print("2. Try running: pip install -e .")
    print("3. Check that the credforge directory has an __init__.py file")
