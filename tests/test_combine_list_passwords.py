"""
Unit tests for combine-list-passwords.py
"""
import os
from pathlib import Path
import pytest

def test_process_password_files_basic(temp_dir):
    """Test basic functionality of process_password_files function."""
    # Create a test cracked passwords file (format: hash:password)
    cracked_file = temp_dir / "cracked.txt"
    cracked_data = [
        "hash1:password1",
        "hash2:password2",
        "hash3:password3"
    ]
    with open(cracked_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(cracked_data) + '\n')
    
    # Create a test hash file (format: username:hash:...)
    hash_file = temp_dir / "hashes.txt"
    hash_data = [
        "user1:hash1:other:data",
        "user2:hash2:other:data",
        "user3:hash4:other:data"  # hash4 is not in cracked file
    ]
    with open(hash_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(hash_data) + '\n')
    
    # Output file path
    output_file = temp_dir / "output.txt"
    
    # Import the function to test
    from credforge.combine_list_passwords import process_password_files
    
    # Call the function
    process_password_files(str(cracked_file), str(hash_file), str(output_file))
    
    # Verify the output file was created
    assert output_file.exists()
    
    # Read the output file and verify contents
    with open(output_file, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    # We expect 2 matches (hash1 and hash2, but not hash4)
    assert len(lines) == 2
    assert any("user1:hash1:password1" in line for line in lines)
    assert any("user2:hash2:password2" in line for line in lines)

def test_process_password_files_no_matches(temp_dir):
    """Test process_password_files with no matching hashes."""
    # Create a test cracked passwords file
    cracked_file = temp_dir / "cracked.txt"
    with open(cracked_file, 'w', encoding='utf-8') as f:
        f.write("hash1:password1\n")
    
    # Create a test hash file with no matching hashes
    hash_file = temp_dir / "hashes.txt"
    with open(hash_file, 'w', encoding='utf-8') as f:
        f.write("user1:different_hash:other:data\n")
    
    # Output file path
    output_file = temp_dir / "output.txt"
    
    # Import the function to test
    from credforge.combine_list_passwords import process_password_files
    
    # Call the function
    process_password_files(str(cracked_file), str(hash_file), str(output_file))
    
    # Verify the output file was created but is empty (no matches)
    assert output_file.exists()
    assert output_file.stat().st_size == 0

def test_process_password_files_empty_files(temp_dir):
    """Test process_password_files with empty input files."""
    # Create empty input files
    cracked_file = temp_dir / "empty_cracked.txt"
    hash_file = temp_dir / "empty_hashes.txt"
    output_file = temp_dir / "output.txt"
    
    # Create empty files
    cracked_file.touch()
    hash_file.touch()
    
    # Import the function to test
    from credforge.combine_list_passwords import process_password_files
    
    # Call the function with empty files
    process_password_files(str(cracked_file), str(hash_file), str(output_file))
    
    # Verify the output file was created but is empty
    assert output_file.exists()
    assert output_file.stat().st_size == 0
