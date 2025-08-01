"""
Unit tests for process_ntds.py
"""
import os
from pathlib import Path
import pytest

def test_process_ntds_file(temp_dir, sample_ntds_data):
    """Test basic functionality of process_ntds_file function."""
    # Create a test input file with NTDS data
    input_file = temp_dir / "test_ntds.txt"
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(sample_ntds_data) + '\n')
    
    # Output file path
    output_file = temp_dir / "active_accounts.ntds"
    
    # Import the function to test
    from credforge.process_ntds import process_ntds_file, is_account_disabled
    
    # First, test is_account_disabled function
    assert is_account_disabled("user1:1001:hash1:hash1_nt:disabled:false:false:false") is True
    assert is_account_disabled("user2:1002:hash2:hash2_nt:enabled:false:false:false") is False
    
    # Now test process_ntds_file
    process_ntds_file(str(input_file), str(output_file))
    
    # Verify the output file was created
    assert output_file.exists()
    
    # Read the output file and verify contents
    with open(output_file, 'r', encoding='utf-8') as f:
        active_accounts = [line.strip() for line in f.readlines() if line.strip()]
    
    # We expect 2 active accounts (enabled) out of 4 total
    assert len(active_accounts) == 2
    assert any("user2" in account for account in active_accounts)
    assert any("user4" in account for account in active_accounts)

def test_process_ntds_file_no_disabled(temp_dir):
    """Test process_ntds_file with no disabled accounts."""
    # Create a test input file with all accounts enabled
    input_file = temp_dir / "all_active.txt"
    test_data = [
        "user1:1001:hash1:hash1_nt:enabled:false:false:false",
        "user2:1002:hash2:hash2_nt:enabled:false:false:false"
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data) + '\n')
    
    # Output file path
    output_file = temp_dir / "active_accounts.ntds"
    
    # Import the function to test
    from credforge.process_ntds import process_ntds_file
    
    # Process the file
    process_ntds_file(str(input_file), str(output_file))
    
    # Verify the output file was created and contains all accounts
    assert output_file.exists()
    
    with open(output_file, 'r', encoding='utf-8') as f:
        active_accounts = [line.strip() for line in f.readlines() if line.strip()]
    
    assert len(active_accounts) == 2

def test_process_ntds_file_all_disabled(temp_dir):
    """Test process_ntds_file with all accounts disabled."""
    # Create a test input file with all accounts disabled
    input_file = temp_dir / "all_disabled.txt"
    test_data = [
        "user1:1001:hash1:hash1_nt:disabled:false:false:false",
        "user2:1002:hash2:hash2_nt:disabled:false:false:false"
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data) + '\n')
    
    # Output file path
    output_file = temp_dir / "active_accounts.ntds"
    
    # Import the function to test
    from credforge.process_ntds import process_ntds_file
    
    # Process the file
    process_ntds_file(str(input_file), str(output_file))
    
    # Verify the output file was created but is empty (no active accounts)
    assert output_file.exists()
    assert output_file.stat().st_size == 0  # File should be empty
