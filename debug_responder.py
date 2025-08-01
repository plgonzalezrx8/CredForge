"""
Debug script to understand the responder2hashcat validation issue
"""
from credforge.responder2hashcat import is_valid_ntlm_response, process_file
import tempfile
import os

def debug_validation():
    print("Testing individual validation cases:")
    
    test_cases = [
        "[+] This is a comment line and should be ignored",
        "",
        "USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788",  # Should be valid
        "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788",  # Should be invalid
        "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788",  # Should be valid
    ]
    
    for i, case in enumerate(test_cases):
        if case.startswith("[+]") or case == "":
            print(f"Case {i+1}: '{case[:50]}...' - SKIPPED (comment/empty)")
        else:
            result = is_valid_ntlm_response(case)
            print(f"Case {i+1}: '{case[:50]}...' - {'VALID' if result else 'INVALID'}")
    
    print("\nTesting process_file function:")
    
    # Create temporary files
    with tempfile.TemporaryDirectory() as temp_dir:
        input_file = os.path.join(temp_dir, "test_input.txt")
        output_file = os.path.join(temp_dir, "output.txt")
        rejects_file = os.path.join(temp_dir, "rejects.txt")
        
        # Write test data
        with open(input_file, 'w') as f:
            f.write('\n'.join(test_cases) + '\n')
        
        # Process the file
        accepted, rejected = process_file(input_file, output_file, rejects_file)
        
        print(f"Results: {accepted} accepted, {rejected} rejected")
        print(f"Expected: 2 accepted, 1 rejected")
        
        # Show what was accepted
        if os.path.exists(output_file):
            print("\nAccepted responses:")
            with open(output_file, 'r') as f:
                for line in f:
                    print(f"  {line.strip()}")
        
        # Show what was rejected
        if os.path.exists(rejects_file):
            print("\nRejected responses:")
            with open(rejects_file, 'r') as f:
                for line in f:
                    print(f"  {line.strip()}")

if __name__ == "__main__":
    debug_validation()
