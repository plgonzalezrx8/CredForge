#!/usr/bin/env python3
"""
Duplicate Line Remover

This script finds and removes duplicate lines from text files while preserving the original
order of first occurrences. It provides detailed statistics about duplicates found and
allows for both in-place modification and output to a new file.

Usage:
    python remove_duplicates.py <input_file> [output_file]
    
If output_file is not provided, the input file will be modified in-place after
user confirmation.

Features:
    - Preserves original line order
    - Shows detailed duplicate statistics
    - Progress reporting for large files
    - Safe in-place modification with backup
    - Handles various text encodings
"""

import os
import sys
from collections import defaultdict
from pathlib import Path
from typing import Dict, List, Tuple, Set

def find_duplicates(input_file: str) -> Tuple[Dict[str, List[int]], int]:
    """
    Find and return duplicate lines in the input file along with their line numbers.
    
    Args:
        input_file: Path to the input file to analyze
        
    Returns:
        Tuple containing:
        - Dictionary mapping duplicate lines to list of line numbers where they appear
        - Total count of unique lines
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If file cannot be read
    """
    if not Path(input_file).is_file():
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    
    seen: Dict[str, int] = {}
    duplicates: Dict[str, List[int]] = defaultdict(list)
    total_lines = 0
    
    try:
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            for line_num, line in enumerate(f, 1):
                total_lines += 1
                line = line.strip()
                
                if line:  # Skip empty lines
                    if line in seen:
                        duplicates[line].append(line_num)
                    else:
                        seen[line] = line_num
                        
                # Show progress for large files
                if total_lines % 10000 == 0:
                    print(f"Analyzed {total_lines:,} lines...", end='\r')
        
        if total_lines >= 10000:
            print(f"Analyzed {total_lines:,} lines... Done!")
    
    except Exception as e:
        raise IOError(f"Error reading file '{input_file}': {e}")
    
    return dict(duplicates), len(seen)

def remove_duplicates(input_file: str, output_file: str = None) -> Tuple[int, int]:
    """
    Remove duplicate lines from the input file and save to output file.
    
    Args:
        input_file: Path to the input file
        output_file: Path to the output file (if None, modifies input file in-place)
        
    Returns:
        Tuple containing:
        - Number of unique lines kept
        - Number of duplicate lines removed
        
    Raises:
        FileNotFoundError: If input file doesn't exist
        IOError: If files cannot be read/written
    """
    if not Path(input_file).is_file():
        raise FileNotFoundError(f"Input file '{input_file}' not found.")
    
    # Determine output strategy
    temp_file = False
    if output_file is None:
        output_file = input_file + '.tmp'
        temp_file = True
    
    seen: Set[str] = set()
    removed_count = 0
    total_lines = 0
    processed_lines = 0
    
    try:
        # First pass: count total lines for progress
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as f:
            total_lines = sum(1 for _ in f)
        
        print(f"Processing {total_lines:,} lines...")
        
        # Process the file
        with open(input_file, 'r', encoding='utf-8', errors='ignore') as infile, \
             open(output_file, 'w', encoding='utf-8') as outfile:
            
            for i, line in enumerate(infile, 1):
                original_line = line
                line = line.strip()
                
                if line:  # Process non-empty lines
                    if line not in seen:
                        seen.add(line)
                        outfile.write(original_line)  # Preserve original formatting
                        processed_lines += 1
                    else:
                        removed_count += 1
                else:
                    # Preserve empty lines
                    outfile.write(original_line)
                
                # Print progress every 1000 lines
                if i % 1000 == 0 or i == total_lines:
                    print(f"Processed {i:,}/{total_lines:,} lines...", end='\r')
        
        print(f"Processed {total_lines:,}/{total_lines:,} lines... Done!")
        
        # If we were working with a temporary file, replace the original
        if temp_file:
            # Create backup of original file
            backup_file = input_file + '.backup'
            if Path(backup_file).exists():
                os.remove(backup_file)
            os.rename(input_file, backup_file)
            os.rename(output_file, input_file)
            print(f"Original file backed up as: {backup_file}")
    
    except Exception as e:
        # Clean up temp file if something went wrong
        if temp_file and Path(output_file).exists():
            os.remove(output_file)
        raise IOError(f"Error processing files: {e}")
    
    return processed_lines, removed_count

def main():
    """Main function to handle command line arguments and coordinate duplicate removal."""
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <input_file> [output_file]")
        print("\nArguments:")
        print("  input_file   Path to the file to analyze for duplicates")
        print("  output_file  Path to save deduplicated content (optional)")
        print("\nIf output_file is not provided, the input file will be modified in-place.")
        print("A backup will be created automatically when modifying in-place.")
        sys.exit(1)
    
    input_file = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) > 2 else None
    
    try:
        print("Duplicate Line Remover")
        print("=" * 22)
        print(f"Analyzing file: {input_file}\n")
        
        print("Finding duplicates...")
        duplicates, unique_count = find_duplicates(input_file)
        
        if duplicates:
            total_duplicate_instances = sum(len(v) for v in duplicates.values())
            
            print(f"\n📊 Duplicate Analysis Results:")
            print(f"   Unique duplicate entries found: {len(duplicates)}")
            print(f"   Total duplicate instances: {total_duplicate_instances}")
            print(f"   Unique lines in file: {unique_count}")
            print(f"   Potential space savings: {total_duplicate_instances} lines\n")
            
            # Show sample duplicates
            print("Sample duplicate entries:")
            for i, (line, line_nums) in enumerate(list(duplicates.items())[:5]):
                display_line = (line[:47] + '...') if len(line) > 50 else line
                display_nums = line_nums[:3]
                if len(line_nums) > 3:
                    display_nums.append(f"... +{len(line_nums)-3} more")
                print(f"  {i+1}. \"{display_line}\" (lines: {', '.join(map(str, display_nums))})")
            
            if len(duplicates) > 5:
                print(f"  ... and {len(duplicates) - 5} more duplicate entries")
            
            print("\n" + "="*50)
            response = input("Do you want to remove duplicates? (y/n): ").strip().lower()
            
            if response == 'y':
                print("\nRemoving duplicates...")
                final_count, removed_count = remove_duplicates(input_file, output_file)
                
                print(f"\n✅ Processing Complete!")
                print(f"   Lines processed: {final_count + removed_count:,}")
                print(f"   Duplicates removed: {removed_count:,}")
                print(f"   Unique lines kept: {final_count:,}")
                
                if output_file:
                    print(f"   Output saved to: {output_file}")
                else:
                    print(f"   Original file updated in-place")
                    print(f"   Backup created with .backup extension")
            else:
                print("\nOperation cancelled. No changes were made.")
        else:
            print("\n✅ No duplicates found in the file.")
            print("The file is already free of duplicate lines.")
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(0)
    except (FileNotFoundError, IOError) as e:
        print(f"\nError: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
