#!/usr/bin/env python3
"""
Password Analyzer

This script analyzes a password file and shows the top 10 most common passwords
along with their frequency count.

Usage:
    python password_analyzer.py <password_file>
"""

import sys
from collections import Counter
from pathlib import Path

def analyze_passwords(password_file):
    """Analyze the password file and return password frequencies."""
    try:
        with open(password_file, 'r', encoding='utf-8', errors='ignore') as f:
            passwords = [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        raise FileNotFoundError(f"File '{password_file}' not found.")
    except Exception as e:
        raise Exception(f"Error reading file: {e}")
    
    if not passwords:
        raise ValueError("No passwords found in the file.")
    
    # Count password occurrences
    password_counter = Counter(passwords)
    
    # Get total unique and total passwords
    total_passwords = len(passwords)
    unique_passwords = len(password_counter)
    
    # Get top 10 most common passwords
    top_passwords = password_counter.most_common(10)
    
    return {
        'total_passwords': total_passwords,
        'unique_passwords': unique_passwords,
        'top_passwords': top_passwords
    }

def print_results(results, filename):
    """Print the analysis results in a formatted way."""
    print(f"\nPassword Analysis for: {filename}")
    print("=" * 60)
    print(f"Total passwords analyzed: {results['total_passwords']:,}")
    print(f"Unique passwords found: {results['unique_passwords']:,}")
    print(f"Password reuse rate: {results['total_passwords']/results['unique_passwords']:.1f}x")
    print("\nTop 10 Most Common Passwords:")
    print("-" * 40)
    print(f"{'Rank':<5} {'Password':<30} {'Count':<10} {'% of Total'}")
    print("-" * 60)
    
    for i, (password, count) in enumerate(results['top_passwords'], 1):
        percent = (count / results['total_passwords']) * 100
        # Truncate long passwords for display
        display_pw = (password[:27] + '...') if len(password) > 30 else password
        print(f"{i:<5} {display_pw:<30} {count:<10} {percent:.2f}%")
    
    print("=" * 60)

def main():
    if len(sys.argv) != 2:
        print("Usage: python password_analyzer.py <password_file>", file=sys.stderr)
        sys.exit(1)
    
    password_file = sys.argv[1]
    
    if not Path(password_file).is_file():
        print(f"Error: '{password_file}' is not a valid file.", file=sys.stderr)
        sys.exit(1)
    
    try:
        results = analyze_passwords(password_file)
        print_results(results, password_file)
    except KeyboardInterrupt:
        print("\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
