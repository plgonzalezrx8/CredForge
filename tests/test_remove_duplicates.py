"""
Unit tests for remove_duplicates.py
"""
import os
from pathlib import Path
import pytest

def test_remove_duplicates_basic(temp_dir, sample_passwords):
    """Test basic functionality of remove_duplicates function."""
    # Create a test input file with duplicates
    input_file = temp_dir / "test_passwords.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_passwords) + '\n')
    
    # Import the function to test
    from credforge.remove_duplicates import remove_duplicates, find_duplicates
    
    # First, test finding duplicates
    duplicates, unique_count = find_duplicates(str(input_file))
    assert len(duplicates) == 2  # password1 and password2 are duplicated
    assert unique_count == 4  # 4 unique passwords in total
    
    # Now test removing duplicates
    output_file = temp_dir / "deduped_passwords.txt"
    final_count, removed_count = remove_duplicates(str(input_file), str(output_file))
    
    # Verify the results
    assert final_count == 4  # 4 unique passwords
    assert removed_count == 2  # 2 duplicates removed
    
    # Verify the output file contains only unique passwords
    with open(output_file, 'r', encoding='utf-8') as f:
        unique_passwords = [line.strip() for line in f.readlines() if line.strip()]
        assert len(unique_passwords) == 4
        assert len(set(unique_passwords)) == 4  # All entries should be unique

def test_remove_duplicates_in_place(temp_dir, sample_passwords):
    """Test removing duplicates in-place."""
    # Create a test input file with duplicates
    input_file = temp_dir / "test_passwords.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_passwords) + '\n')
    
    # Import the function to test
    from remove_duplicates import remove_duplicates
    
    # Get the original content
    with open(input_file, 'r', encoding='utf-8') as f:
        original_content = f.read()
    
    # Remove duplicates in-place
    final_count, removed_count = remove_duplicates(str(input_file))
    
    # Verify the results
    assert final_count == 4  # 4 unique passwords
    assert removed_count == 2  # 2 duplicates removed
    
    # Verify the file was modified
    with open(input_file, 'r', encoding='utf-8') as f:
        unique_passwords = [line.strip() for line in f.readlines() if line.strip()]
        assert len(unique_passwords) == 4
        assert len(set(unique_passwords)) == 4  # All entries should be unique
    
    # Verify the file was actually modified
    with open(input_file, 'r', encoding='utf-8') as f:
        assert f.read() != original_content

def test_remove_duplicates_empty_file(temp_dir):
    """Test remove_duplicates with an empty file."""
    # Create an empty input file
    input_file = temp_dir / "empty.txt"
    input_file.touch()
    
    # Import the function to test
    from credforge.remove_duplicates import remove_duplicates, find_duplicates
    
    # Test find_duplicates with empty file
    duplicates, unique_count = find_duplicates(str(input_file))
    assert not duplicates
    assert unique_count == 0
    
    # Test remove_duplicates with empty file
    output_file = temp_dir / "output.txt"
    final_count, removed_count = remove_duplicates(str(input_file), str(output_file))
    
    # Verify the results
    assert final_count == 0
    assert removed_count == 0
    assert output_file.exists()
    assert output_file.stat().st_size == 0  # Output file should be empty
