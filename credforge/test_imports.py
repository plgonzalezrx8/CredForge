import sys
import os

print("Python Path:")
for path in sys.path:
    print(f"  {path}")

print("\nCurrent Directory:")
print(f"  {os.getcwd()}")

print("\nTrying to import modules...")
try:
    import split_credentials
    print("✅ Successfully imported split_credentials")
except ImportError as e:
    print(f"❌ Failed to import split_credentials: {e}")

try:
    import remove_duplicates
    print("✅ Successfully imported remove_duplicates")
except ImportError as e:
    print(f"❌ Failed to import remove_duplicates: {e}")

print("\nRunning a simple test...")
try:
    print(f"split_credentials module: {split_credentials.__file__}")
    print(f"remove_duplicates module: {remove_duplicates.__file__}")
except Exception as e:
    print(f"Error: {e}")
