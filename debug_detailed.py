"""
Detailed debug script to understand exactly why USER3 is being rejected
"""
from credforge.responder2hashcat import is_valid_ntlm_response

def detailed_debug():
    test_line = "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788"
    print(f"Testing line: {test_line}")
    
    # Manual validation step by step
    print("\nStep-by-step validation:")
    
    # Check basic structure
    if not test_line or test_line.count(':') < 5:
        print("❌ Failed: Not enough colons")
        return False
    else:
        print("✅ Passed: Has enough colons")
    
    parts = test_line.split(':')
    print(f"Parts: {parts}")
    
    # Check length
    if len(parts) < 6:
        print("❌ Failed: Not enough parts")
        return False
    else:
        print("✅ Passed: Has enough parts")
    
    # Check double colon
    if parts[1] != '':
        print("❌ Failed: Second field not empty")
        return False
    else:
        print("✅ Passed: Second field is empty (double colon)")
    
    # Check required fields not empty
    if not parts[0] or not parts[2] or not parts[3] or not parts[4] or not parts[5]:
        print(f"❌ Failed: Required field is empty")
        print(f"  parts[0]: '{parts[0]}'")
        print(f"  parts[2]: '{parts[2]}'")
        print(f"  parts[3]: '{parts[3]}'")
        print(f"  parts[4]: '{parts[4]}'")
        print(f"  parts[5]: '{parts[5]}'")
        return False
    else:
        print("✅ Passed: All required fields are non-empty")
    
    # Check for invalid data
    print("\nChecking fields 3-5 for invalid data:")
    for i, part in enumerate(parts[3:6], 3):
        print(f"  parts[{i}]: '{part}' -> {part.lower()}")
        if part.lower() in ['nothex', 'invalidhash']:
            print(f"❌ Failed: Field {i} contains invalid data: '{part}'")
            return False
        else:
            print(f"✅ Passed: Field {i} is valid")
    
    print("\n✅ All validation checks passed!")
    
    # Now test the actual function
    result = is_valid_ntlm_response(test_line)
    print(f"\nActual function result: {result}")
    
    return result

if __name__ == "__main__":
    detailed_debug()
