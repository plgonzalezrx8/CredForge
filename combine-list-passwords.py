def process_password_files(cracked_file, hash_file, output_file):
    # Read and parse the cracked passwords file
    hash_to_password = {}
    try:
        with open(cracked_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    # Split only on first colon in case password contains colons
                    hash_part, password = line.split(':', 1)
                    hash_to_password[hash_part.lower()] = password
    except FileNotFoundError:
        print("Error: Could not find cracked passwords file")
        return
    except Exception as e:
        print("Error reading cracked passwords file:", e)
        return
    
    # Process the hash file and find matches
    matches = []
    try:
        with open(hash_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and ':' in line:
                    parts = line.split(':')
                    if len(parts) >= 4:
                        username = parts[0]
                        ntlm_hash = parts[3].lower()  # NTLM hash is the 4th field
                        
                        # Check if this hash has been cracked
                        if ntlm_hash in hash_to_password:
                            password = hash_to_password[ntlm_hash]
                            matches.append(username + ":" + ntlm_hash + ":" + password)
    except FileNotFoundError:
        print("Error: Could not find hash file")
        return
    except Exception as e:
        print("Error reading hash file:", e)
        return
    
    # Write results to output file
    try:
        with open(output_file, 'w') as f:
            for match in matches:
                f.write(match + '\n')
        
        print("Successfully processed files!")
        print("Found", len(matches), "matches")
        print("Results written to", output_file)
        
        # Print first few matches as preview
        if matches:
            print("\nFirst few matches:")
            for i in range(min(5, len(matches))):
                print(" ", matches[i])
            if len(matches) > 5:
                print("  ... and", len(matches) - 5, "more")
                
    except Exception as e:
        print("Error writing to output file:", e)

def main():
    print("NTLM Hash and Password Matcher")
    print("=" * 35)
    
    cracked_file = input("Enter the path to the cracked passwords file: ")
    hash_file = input("Enter the path to the NTLM hash file: ")
    output_file = input("Enter the output file name (or press Enter for 'Userandpasswords.txt'): ")
    
    if not output_file:
        output_file = "Userandpasswords.txt"
    
    process_password_files(cracked_file, hash_file, output_file)

if __name__ == "__main__":
    main()