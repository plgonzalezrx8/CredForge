#!/usr/bin/env python3
import os
import sys
from collections import defaultdict

def find_duplicates(input_file):
    """
    Find and return duplicate lines in the input file along with their line numbers.
    """
    seen = {}
    duplicates = defaultdict(list)
    
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if line:  # Skip empty lines
                if line in seen:
                    duplicates[line].append(line_num)
                else:
                    seen[line] = line_num
    
    return duplicates, len(seen)

def remove_duplicates(input_file, output_file=None):
    """
    Remove duplicate lines from the input file and save to output file.
    If output_file is not provided, it will modify the input file in-place.
    """
    if output_file is None:
        output_file = input_file + '.tmp'
    
    seen = set()
    removed_count = 0
    total_lines = 0
    
    # First pass: count total lines for progress
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
        total_lines = sum(1 for _ in f)
    
    # Process the file
    with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
         open(output_file, 'w', encoding='utf-8') as outfile:
        
        for i, line in enumerate(infile, 1):
            line = line.strip()
            if line:  # Skip empty lines
                if line not in seen:
                    seen.add(line)
                    outfile.write(line + '\n')
                else:
                    removed_count += 1
            
            # Print progress every 1000 lines
            if i % 1000 == 0 or i == total_lines:
                print(f"Processed {i}/{total_lines} lines...", end='\r')
    
    # If we were working with a temporary file, replace the original
    if output_file.endswith('.tmp'):
        os.replace(output_file, input_file)
    
    return len(seen), removed_count

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file> [output_file]")
        print("If output_file is not provided, the input file will be modified in-place.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    if not os.path.isfile(input_file):
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    
    print("Finding duplicates...")
    duplicates, unique_count = find_duplicates(input_file)
    
    if duplicates:
        print(f"\nFound {len(duplicates)} unique duplicate entries:")
        for line, line_nums in list(duplicates.items())[:5]:  # Show first 5 duplicates
            print(f'  "{line[:50]}{"..." if len(line) > 50 else ""}" - Duplicate on lines: {line_nums[:3]}{"..." if len(line_nums) > 3 else ""}')
        if len(duplicates) > 5:
            print(f"  ... and {len(duplicates) - 5} more")
        
        print(f"\nTotal unique lines: {unique_count}")
        print(f"Total duplicate instances: {sum(len(v) for v in duplicates.values())}")
        
        response = input("\nDo you want to remove duplicates? (y/n): ").strip().lower()
        if response == 'y':
            print("\nRemoving duplicates...")
            final_count, removed_count = remove_duplicates(input_file, output_file)
            print(f"\nDone! Removed {removed_count} duplicate lines.")
            print(f"Original lines: {final_count + removed_count}")
            print(f"Unique lines: {final_count}")
            if output_file:
                print(f"Saved to: {output_file}")
            else:
                print("Original file has been updated in-place.")
        else:
            print("No changes were made.")
    else:
        print("No duplicates found in the file.")

if __name__ == "__main__":
    main()
