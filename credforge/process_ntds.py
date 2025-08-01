#!/usr/bin/env python3
"""
NTDS File Processor

This script processes an NTDS file and removes any lines containing disabled accounts.
Disabled accounts are identified by the account status flag in the NTDS dump.

Usage:
    python process_ntds.py -w <input_ntds_file> -o <output_file>
"""

import argparse
import re
import sys
from pathlib import Path

def is_account_disabled(ntds_line):
    """
    Check if an account is disabled based on the NTDS line.
    
    The status is in the 5th field (index 4) of colon-separated values.
    """
    parts = ntds_line.strip().split(':')
    if len(parts) >= 5:
        status = parts[4].lower()
        return status == 'disabled'
    return False

def process_ntds_file(input_file, output_file):
    """Process the NTDS file and write non-disabled accounts to the output file."""
    total_lines = 0
    disabled_lines = 0
    
    try:
        # Count total lines for progress reporting
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)
        
        # Process the file
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            print(f"Processing {input_file}...")
            print(f"Total accounts to process: {total_lines:,}")
            print("Filtering out disabled accounts...")
            
            for i, line in enumerate(infile, 1):
                # Show progress every 10,000 lines
                if i % 10000 == 0:
                    print(f"Processed {i:,} of {total_lines:,} accounts...")
                
                # Skip empty lines
                line = line.strip()
                if not line:
                    continue
                
                # Check if account is disabled
                if is_account_disabled(line):
                    disabled_lines += 1
                    continue
                
                # Write non-disabled accounts to output
                outfile.write(line + '\n')
        
        # Print summary
        active_lines = total_lines - disabled_lines
        print("\nProcessing complete!")
        print(f"Total accounts processed: {total_lines:,}")
        print(f"Disabled accounts found: {disabled_lines:,} ({disabled_lines/total_lines:.1%})")
        print(f"Active accounts written to {output_file}: {active_lines:,} ({active_lines/total_lines:.1%})")
        
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.", file=sys.stderr)
        sys.exit(1)
    except PermissionError:
        print(f"Error: Permission denied when accessing files.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}", file=sys.stderr)
        sys.exit(1)

def main():
    parser = argparse.ArgumentParser(description='Process NTDS file to remove disabled accounts.')
    parser.add_argument('-w', '--ntds-file', required=True, 
                        help='Path to the NTDS file to process')
    parser.add_argument('-o', '--output', required=True,
                        help='Path to the output file for active accounts')
    
    args = parser.parse_args()
    
    # Validate input file exists
    if not Path(args.ntds_file).is_file():
        print(f"Error: Input file '{args.ntds_file}' does not exist.", file=sys.stderr)
        sys.exit(1)
    
    # Check if output file already exists
    if Path(args.output).exists():
        print(f"Warning: Output file '{args.output}' already exists and will be overwritten.")
        response = input("Continue? (y/n): ").strip().lower()
        if response != 'y':
            print("Operation cancelled by user.")
            sys.exit(0)
    
    # Process the NTDS file
    process_ntds_file(args.ntds_file, args.output)

if __name__ == "__main__":
    main()
