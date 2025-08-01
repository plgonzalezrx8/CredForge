#!/usr/bin/env python3
"""
Script to split a credentials file into separate username, password, and combined files.
Input format: username:hash:password (one per line)
Output: 3 files - usernames.txt, passwords.txt, usernames_passwords.txt
"""

import sys
import os
from pathlib import Path

def split_credentials(input_file, output_dir=None):
    """
    Split credentials file into separate files for usernames, passwords, and combined.
    
    Args:
        input_file (str): Path to input file with format username:hash:password
        output_dir (str): Directory to save output files (default: same as input file)
    """
    
    # Validate input file exists
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' not found.")
        return False
    
    # Set output directory
    if output_dir is None:
        output_dir = os.path.dirname(input_file)
    
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Define output file paths
    base_name = Path(input_file).stem
    usernames_file = os.path.join(output_dir, f"{base_name}_usernames.txt")
    passwords_file = os.path.join(output_dir, f"{base_name}_passwords.txt")
    hashes_file = os.path.join(output_dir, f"{base_name}_hashes.txt")
    combined_file = os.path.join(output_dir, f"{base_name}_usernames_passwords.txt")
    usernames_hashes_file = os.path.join(output_dir, f"{base_name}_usernames_hashes.txt")
    
    usernames = []
    passwords = []
    hashes = []
    combined = []
    usernames_hashes = []
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                
                # Skip empty lines
                if not line:
                    continue
                
                # Split by colon - expect username:hash:password
                parts = line.split(':')
                
                if len(parts) < 3:
                    print(f"Warning: Line {line_num} has unexpected format: {line}")
                    continue
                
                # Extract username, hash, and password
                username = parts[0]
                hash_value = parts[1]
                password = ':'.join(parts[2:])  # Handle passwords that contain colons
                
                # Extract just the username part if it contains domain\username format
                if '\\' in username:
                    username = username.split('\\')[-1]  # Take the part after the last backslash
                
                # Skip entries with empty hashes (which would mean the line doesn't have the expected format)
                if not hash_value or hash_value.strip() == '':
                    print(f"Warning: Line {line_num} has empty hash, skipping: {line}")
                    continue
                
                usernames.append(username)
                passwords.append(password)
                hashes.append(hash_value)
                combined.append(f"{username}:{password}")
                usernames_hashes.append(f"{username}:{hash_value}")
        
        # Write output files
        with open(usernames_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(usernames) + '\n')
        
        with open(passwords_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(passwords) + '\n')
        
        with open(hashes_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(hashes) + '\n')
        
        with open(combined_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(combined) + '\n')
        
        with open(usernames_hashes_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(usernames_hashes) + '\n')
        
        # Check if any credentials were processed
        if len(usernames) == 0:
            print(f"No valid credentials found in '{input_file}'")
            return False
        
        print(f"Successfully processed {len(usernames)} credentials from '{input_file}'")
        print(f"Output files created:")
        print(f"  - Usernames: {usernames_file}")
        print(f"  - Passwords: {passwords_file}")
        print(f"  - Hashes:    {hashes_file}")
        print(f"  - Combined:  {combined_file}")
        print(f"  - User:Hash: {usernames_hashes_file}")
        
        return True
        
    except Exception as e:
        print(f"Error processing file: {e}")
        return False

def main():
    """Main function to handle command line arguments."""
    
    if len(sys.argv) < 2:
        print("Usage: python split-credentials.py <input_file> [output_directory]")
        print("\nExample:")
        print("  python split-credentials.py Userandpasswords2.txt")
        print("  python split-credentials.py Userandpasswords2.txt ./output/")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    success = split_credentials(input_file, output_dir)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
