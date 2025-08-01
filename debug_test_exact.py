"""
Debug script that exactly mimics the failing test to understand the issue
"""
from credforge.responder2hashcat import process_file, is_valid_ntlm_response
import tempfile
import os

def debug_exact_test():
    print("Debugging the exact test scenario:")
    
    # Exact test data from the failing test
    test_data = [
        "[+] This is a comment line and should be ignored",
        "",
        "USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788",  # Valid
        "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788",  # Invalid (bad hash)
        "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788",  # Valid
    ]
    
    print("Test data:")
    for i, line in enumerate(test_data):
        print(f"  {i+1}: {line}")
    
    print("\nValidation results for each line:")
    for i, line in enumerate(test_data):
        if line.startswith("[+]") or line == "":
            print(f"  {i+1}: SKIPPED (comment/empty)")
        else:
            result = is_valid_ntlm_response(line)
            print(f"  {i+1}: {'VALID' if result else 'INVALID'} - {line[:50]}...")
    
    # Create temporary directory and files exactly like the test
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, "responder.log")
        output_file = os.path.join(temp_dir, "hashes.txt")
        rejects_file = os.path.join(temp_dir, "rejects.txt")
        
        # Write test data exactly like the test
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_data) + '\n')
        
        print(f"\nInput file created: {input_file}")
        print("Input file contents:")
        with open(input_file, 'r') as f:
            for i, line in enumerate(f, 1):
                print(f"  Line {i}: {repr(line)}")
        
        # Call process_file exactly like the test
        accepted, rejected = process_file(input_file, output_file, rejects_file)
        
        print(f"\nResults:")
        print(f"  Accepted: {accepted}")
        print(f"  Rejected: {rejected}")
        print(f"  Expected: 2 accepted, 1 rejected")
        
        # Show what was accepted
        print(f"\nAccepted responses (from {output_file}):")
        if os.path.exists(output_file):
            with open(output_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    print(f"  {i}: {line.strip()}")
        else:
            print("  No output file created")
        
        # Show what was rejected
        print(f"\nRejected responses (from {rejects_file}):")
        if os.path.exists(rejects_file):
            with open(rejects_file, 'r') as f:
                for i, line in enumerate(f, 1):
                    print(f"  {i}: {line.strip()}")
        else:
            print("  No rejects file created")

if __name__ == "__main__":
    debug_exact_test()
