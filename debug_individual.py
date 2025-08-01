"""
Debug individual line validation
"""
from credforge.responder2hashcat import is_valid_ntlm_response

def test_individual_lines():
    lines = [
        "USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788",
        "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788", 
        "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788"
    ]
    
    for i, line in enumerate(lines, 1):
        print(f"\nTesting line {i}: {line}")
        
        # Test validation
        result = is_valid_ntlm_response(line)
        print(f"Validation result: {result}")
        
        # Debug the validation step by step
        parts = line.split(':')
        print(f"Parts: {parts}")
        print(f"Length: {len(parts)}")
        print(f"Fields 3-5: {parts[3:6]}")
        
        # Check for invalid data in fields 3-5
        invalid_found = False
        for j, part in enumerate(parts[3:6], 3):
            if part.lower() in ['nothex', 'invalidhash']:
                print(f"  Field {j} '{part}' is INVALID")
                invalid_found = True
            else:
                print(f"  Field {j} '{part}' is valid")
        
        if invalid_found:
            print("  -> Should be REJECTED")
        else:
            print("  -> Should be ACCEPTED")

if __name__ == "__main__":
    test_individual_lines()
