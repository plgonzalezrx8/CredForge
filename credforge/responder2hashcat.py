#!/usr/bin/env python3
"""
Responder to Hashcat Converter

This script processes Responder's NTLMv1/2 challenge/response captures and converts them into
Hashcat-compatible formats. It filters valid NTLM authentication attempts and separates them
from malformed or invalid entries.

Usage:
    python responder2hashcat.py <input_file> [output_file] [rejects_file]

Arguments:
    input_file    Path to the Responder capture file
    output_file   Path to save valid Hashcat-compatible hashes (default: clean.txt)
    rejects_file  Path to save rejected/invalid entries (default: rejects.txt)

Example:
    python responder2hashcat.py Responder-Session.log valid_hashes.txt invalid_entries.txt
"""

import re
import sys
import os
from typing import Tuple, TextIO

def is_valid_ntlm_response(line: str) -> bool:
    """
    Check if a line contains a valid NTLM response format.
    
    Args:
        line: Input line to validate
        
    Returns:
        bool: True if line matches NTLM response pattern, False otherwise
    """
    # Pattern matches NTLMv1/2 challenge/response hashes
    pattern = r'^[^:]+::[^:]+:[0-9A-Fa-f]{16}:[0-9A-Fa-f]{32}:[0-9A-Fa-f]{64,}$'
    return bool(re.match(pattern, line))

def process_file(input_file: str, output_file: str, rejects_file: str) -> Tuple[int, int]:
    """
    Process the input file and separate valid NTLM responses from invalid ones.
    
    Args:
        input_file: Path to the input file
        output_file: Path to write valid hashes
        rejects_file: Path to write rejected entries
        
    Returns:
        Tuple[int, int]: Count of accepted and rejected entries
    """
    accepted = 0
    rejected = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='replace') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile, \
             open(rejects_file, 'w', encoding='utf-8') as rejectfile:
            
            for line in infile:
                line = line.strip()
                if not line:  # Skip empty lines
                    continue
                    
                if is_valid_ntlm_response(line):
                    outfile.write(f"{line}\n")
                    accepted += 1
                else:
                    rejectfile.write(f"{line}\n")
                    rejected += 1
                    
    except IOError as e:
        print(f"Error processing files: {e}", file=sys.stderr)
        sys.exit(1)
    
    return accepted, rejected

def main():
    # Check for correct number of arguments
    if len(sys.argv) < 2:
        print("Error: No input file specified\n")
        print("Usage: python responder2hashcat.py <input_file> [output_file] [rejects_file]")
        print("  input_file    Path to the Responder capture file")
        print("  output_file   Path to save valid hashes (default: clean.txt)")
        print("  rejects_file  Path to save rejected entries (default: rejects.txt)")
        sys.exit(1)
    
    # Set default file paths
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else 'clean.txt'
    rejects_file = sys.argv[3] if len(sys.argv) > 3 else 'rejects.txt'
    
    # Validate input file exists
    if not os.path.isfile(input_file):
        print(f"Error: Input file '{input_file}' not found", file=sys.stderr)
        sys.exit(1)
    
    print(f"Processing: {input_file}")
    print(f"Valid hashes will be saved to: {output_file}")
    print(f"Invalid entries will be saved to: {rejects_file}")
    
    # Process the file
    accepted, rejected = process_file(input_file, output_file, rejects_file)
    total = accepted + rejected
    
    # Print summary
    print("\nProcessing complete!")
    print(f"Total entries processed: {total}")
    print(f"Accepted (valid) hashes: {accepted} ({accepted/max(total, 1)*100:.1f}%)")
    print(f"Rejected entries: {rejected} ({rejected/max(total, 1)*100:.1f}%)")

if __name__ == "__main__":
    main()