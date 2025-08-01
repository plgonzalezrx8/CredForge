"""
Final comprehensive debug to understand and fix the test failure
"""
from credforge.responder2hashcat import process_file, is_valid_ntlm_response
import tempfile
import os
from pathlib import Path

def final_debug():
    print("=== FINAL DEBUG: Understanding the test failure ===\n")
    
    # Exact test data
    test_data = [
        "[+] This is a comment line and should be ignored",
        "",
        "USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788",  # Valid
        "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788",  # Invalid (bad hash)
        "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788",  # Valid
    ]
    
    print("1. Test data analysis:")
    for i, line in enumerate(test_data):
        print(f"   Line {i+1}: {line}")
        if line.startswith("[+]") or line == "":
            print(f"            -> IGNORED (comment/empty)")
        else:
            result = is_valid_ntlm_response(line)
            expected = "VALID" if i+1 in [3, 5] else "INVALID"  # Lines 3 and 5 should be valid
            status = "✅" if (result and expected == "VALID") or (not result and expected == "INVALID") else "❌"
            print(f"            -> {expected} (actual: {'VALID' if result else 'INVALID'}) {status}")
    
    print(f"\n2. Expected results:")
    print(f"   - Lines to process: 3 (ignoring comment and empty lines)")
    print(f"   - Expected valid: 2 (USER1 and USER3)")
    print(f"   - Expected invalid: 1 (USER2)")
    
    # Create temp directory and run the actual process
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        input_file = temp_path / "responder.log"
        output_file = temp_path / "hashes.txt"
        rejects_file = temp_path / "rejects.txt"
        
        # Write test data
        with open(input_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(test_data) + '\n')
        
        print(f"\n3. Running process_file:")
        print(f"   Input: {input_file}")
        print(f"   Output: {output_file}")
        print(f"   Rejects: {rejects_file}")
        
        # Process the file
        accepted, rejected = process_file(str(input_file), str(output_file), str(rejects_file))
        
        print(f"\n4. Actual results:")
        print(f"   Accepted: {accepted}")
        print(f"   Rejected: {rejected}")
        
        # Read and display the output files
        print(f"\n5. Output file contents:")
        if output_file.exists():
            with open(output_file, 'r') as f:
                lines = f.readlines()
                print(f"   Accepted lines ({len(lines)}):")
                for i, line in enumerate(lines, 1):
                    print(f"     {i}: {line.strip()}")
        else:
            print("   No output file created")
        
        print(f"\n6. Rejects file contents:")
        if rejects_file.exists():
            with open(rejects_file, 'r') as f:
                lines = f.readlines()
                print(f"   Rejected lines ({len(lines)}):")
                for i, line in enumerate(lines, 1):
                    print(f"     {i}: {line.strip()}")
        else:
            print("   No rejects file created")
        
        print(f"\n7. Test status:")
        if accepted == 2 and rejected == 1:
            print("   ✅ TEST WOULD PASS")
        else:
            print("   ❌ TEST WOULD FAIL")
            print(f"      Expected: 2 accepted, 1 rejected")
            print(f"      Actual:   {accepted} accepted, {rejected} rejected")

if __name__ == "__main__":
    final_debug()
