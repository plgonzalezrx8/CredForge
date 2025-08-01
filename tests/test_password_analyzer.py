"""
Unit tests for password_analyzer.py
"""
import os
from pathlib import Path
import pytest

def test_analyze_passwords_basic(temp_dir):
    """Test basic functionality of analyze_passwords function."""
    # Create a test input file with passwords
    input_file = temp_dir / "test_passwords.txt"
    test_passwords = [
        "password", "password", "password",  # Most common
        "123456", "123456",  # Second most common
        "qwerty", "letmein", "dragon", "baseball"  # Unique
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_passwords) + '\n')
    
    # Import the function to test
    from credforge.password_analyzer import analyze_passwords
    
    # Call the function
    result = analyze_passwords(str(input_file))
    
    # Verify the results
    assert result['total_passwords'] == 8
    assert result['unique_passwords'] == 6
    
    # Check top passwords
    top_passwords = result['top_passwords']
    assert len(top_passwords) == 6  # 6 unique passwords
    assert top_passwords[0][0] == "password"  # Most common
    assert top_passwords[0][1] == 3  # Appears 3 times
    assert top_passwords[1][0] == "123456"  # Second most common
    assert top_passwords[1][1] == 2  # Appears 2 times

def test_analyze_passwords_empty_file(temp_dir):
    """Test analyze_passwords with an empty file."""
    # Create an empty input file
    input_file = temp_dir / "empty.txt"
    input_file.touch()
    
    # Import the function to test
    from credforge.password_analyzer import analyze_passwords
    
    # Call the function and verify it raises an appropriate exception
    with pytest.raises(ValueError, match="No passwords found in the file"):
        analyze_passwords(str(input_file))

def test_analyze_passwords_nonexistent_file():
    """Test analyze_passwords with a non-existent file."""
    from password_analyzer import analyze_passwords
    
    with pytest.raises(FileNotFoundError):
        analyze_passwords("nonexistent_file.txt")
