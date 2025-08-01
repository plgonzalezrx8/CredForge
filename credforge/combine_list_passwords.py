#!/usr/bin/env python3
"""
NTLM Hash and Password Matcher

This script matches cracked passwords with NTDS hash dumps to create username:hash:password
credential files. It reads a file containing hash:password pairs and matches them against
NTDS dump files to produce combined credential output.

Usage:
    python combine_list_passwords.py
    
The script will prompt for:
    - Path to cracked passwords file (format: hash:password)
    - Path to NTLM hash file (NTDS dump format)
    - Output file name for matched credentials
"""

import sys
import os
from pathlib import Path
from typing import Dict, List, Tuple

def process_password_files(cracked_file: str, hash_file: str, output_file: str) -> bool:
    """
    Process cracked passwords and NTDS hash files to find matches.
    
    Args:
        cracked_file: Path to file containing hash:password pairs
        hash_file: Path to NTDS dump file
        output_file: Path to write matched credentials
        
    Returns:
        bool: True if processing was successful, False otherwise
    """
    # Validate input files exist
    if not Path(cracked_file).is_file():
        print(f"Error: Cracked passwords file '{cracked_file}' not found.")
        return False
        
    if not Path(hash_file).is_file():
        print(f"Error: Hash file '{hash_file}' not found.")
        return False
    
    # Read and parse the cracked passwords file
    hash_to_password: Dict[str, str] = {}
    try:
        with open(cracked_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                if line and ':' in line:
                    # Split only on first colon in case password contains colons
                    hash_part, password = line.split(':', 1)
                    hash_to_password[hash_part.lower()] = password
                elif line:  # Non-empty line without colon
                    print(f"Warning: Line {line_num} in cracked file has invalid format: {line}")
                    
        print(f"Loaded {len(hash_to_password)} cracked password hashes.")
        
    except FileNotFoundError:
        print(f"Error: Could not find cracked passwords file '{cracked_file}'")
        return False
    except Exception as e:
        print(f"Error reading cracked passwords file: {e}")
        return False
    
    # Process the hash file and find matches
    matches: List[str] = []
    processed_lines = 0
    
    try:
        with open(hash_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                line = line.strip()
                processed_lines += 1
                
                if not line:
                    continue
                    
                if ':' not in line:
                    print(f"Warning: Line {line_num} in hash file has invalid format: {line}")
                    continue
                    
                parts = line.split(':')
                if len(parts) < 4:  # Need at least username:rid:lm:ntlm
                    print(f"Warning: Line {line_num} has insufficient fields: {line}")
                    continue
                    
                username = parts[0]
                # NTDS format: username:rid:lmhash:ntlmhash:::
                # We want the NTLM hash (4th field, index 3)
                if len(parts) >= 4:
                    ntlm_hash = parts[3].lower()
                else:
                    continue
                    
                # Skip empty hashes
                if not ntlm_hash or ntlm_hash == 'aad3b435b51404eeaad3b435b51404ee':
                    continue
                        
                # Check if this hash has been cracked
                if ntlm_hash in hash_to_password:
                    password = hash_to_password[ntlm_hash]
                    matches.append(f"{username}:{ntlm_hash}:{password}")
                    
        print(f"Processed {processed_lines} lines from hash file.")
        
    except FileNotFoundError:
        print(f"Error: Could not find hash file '{hash_file}'")
        return False
    except Exception as e:
        print(f"Error reading hash file: {e}")
        return False
    
    # Write results to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for match in matches:
                f.write(match + '\n')
        
        print("\nProcessing complete!")
        print(f"Found {len(matches)} matches out of {len(hash_to_password)} cracked hashes.")
        print(f"Results written to: {output_file}")
        
        # Print first few matches as preview
        if matches:
            print("\nFirst few matches:")
            for i in range(min(5, len(matches))):
                # Truncate long usernames/passwords for display
                parts = matches[i].split(':')
                if len(parts) >= 3:
                    user = parts[0][:30] + '...' if len(parts[0]) > 30 else parts[0]
                    hash_part = parts[1][:16] + '...' if len(parts[1]) > 16 else parts[1]
                    pwd = parts[2][:20] + '...' if len(parts[2]) > 20 else parts[2]
                    print(f"  {user}:{hash_part}:{pwd}")
                else:
                    print(f"  {matches[i]}")
            if len(matches) > 5:
                print(f"  ... and {len(matches) - 5} more")
        else:
            print("\nNo matches found. Check that:")
            print("  - Hash formats match between files")
            print("  - NTDS file contains the expected format")
            print("  - Cracked passwords file uses hash:password format")
                
        return True
        
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return False

def main():
    """Main function to handle user interaction and coordinate file processing."""
    print("NTLM Hash and Password Matcher")
    print("=" * 35)
    print("This tool matches cracked passwords with NTDS dumps to create credential files.\n")
    
    try:
        cracked_file = input("Enter the path to the cracked passwords file: ").strip()
        if not cracked_file:
            print("Error: Cracked passwords file path is required.")
            sys.exit(1)
            
        hash_file = input("Enter the path to the NTLM hash file: ").strip()
        if not hash_file:
            print("Error: NTLM hash file path is required.")
            sys.exit(1)
            
        output_file = input("Enter the output file name (or press Enter for 'Userandpasswords.txt'): ").strip()
        if not output_file:
            output_file = "Userandpasswords.txt"
        
        # Warn if output file exists
        if Path(output_file).exists():
            response = input(f"Warning: '{output_file}' already exists. Overwrite? (y/n): ").strip().lower()
            if response != 'y':
                print("Operation cancelled.")
                sys.exit(0)
        
        success = process_password_files(cracked_file, hash_file, output_file)
        
        if not success:
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()