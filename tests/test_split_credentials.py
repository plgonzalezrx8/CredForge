"""
Unit tests for split-credentials.py
"""
import os
from pathlib import Path
import pytest

def test_split_credentials_basic(temp_dir, sample_credentials):
    """Test basic functionality of split_credentials function."""
    # Create a test input file
    input_file = temp_dir / "test_creds.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_credentials) + '\n')
    
    # Import the function to test
    from credforge.split_credentials import split_credentials
    
    # Call the function
    result = split_credentials(str(input_file), str(temp_dir))
    
    # Verify the results
    assert result is True
    
    # Verify the expected output files were created
    # The function creates files with the input filename as prefix
    output_files = [
        temp_dir / "test_creds_usernames.txt",
        temp_dir / "test_creds_passwords.txt",
        temp_dir / "test_creds_usernames_passwords.txt"
    ]
    
    for file in output_files:
        assert file.exists(), f"Expected file {file} was not created"
    
    # Verify the contents of usernames.txt
    with open(temp_dir / "test_creds_usernames.txt", 'r', encoding='utf-8') as f:
        usernames = [line.strip() for line in f.readlines()]
        assert usernames == ["user1", "user2", "user3", "user4", "user5"]
    
    # Verify the contents of passwords.txt
    with open(temp_dir / "test_creds_passwords.txt", 'r', encoding='utf-8') as f:
        passwords = [line.strip() for line in f.readlines()]
        assert passwords == ["password1", "password2", "password3", "password4", "password5"]

def test_split_credentials_invalid_file():
    """Test split_credentials with a non-existent input file."""
    from credforge.split_credentials import split_credentials
    result = split_credentials("nonexistent_file.txt")
    assert result is False

def test_split_credentials_empty_file(temp_dir):
    """Test split_credentials with an empty input file."""
    # Create an empty input file
    input_file = temp_dir / "empty_creds.txt"
    input_file.touch()
    
    from credforge.split_credentials import split_credentials
    result = split_credentials(str(input_file), str(temp_dir))
    assert result is False
