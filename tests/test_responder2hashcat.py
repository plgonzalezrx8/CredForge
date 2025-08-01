"""
Unit tests for responder2hashcat.py
"""
import os
from pathlib import Path
import pytest

def test_is_valid_ntlm_response():
    """Test the is_valid_ntlm_response function."""
    from credforge.responder2hashcat import is_valid_ntlm_response
    
    # Valid NTLM responses
    assert is_valid_ntlm_response("USER::DOMAIN:1122334455667788:hash1:hash2:1122334455667788") is True
    assert is_valid_ntlm_response("USER::DOMAIN:1122334455667788:hash1:hash2:1122334455667788:extra:fields:ok") is True
    
    # Invalid NTLM responses
    assert is_valid_ntlm_response("") is False
    assert is_valid_ntlm_response("USER:DOMAIN:hash1:hash2") is False  # Not enough fields
    assert is_valid_ntlm_response("USER::DOMAIN:nothex:hash1:hash2:11223344") is False  # Invalid hex

def test_process_file_basic(temp_dir):
    """Test basic functionality of process_file function."""
    # Create a test input file with valid and invalid NTLM responses
    input_file = temp_dir / "responder.log"
    test_data = [
        "[+] This is a comment line and should be ignored",
        "",
        "USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788",  # Valid
        "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788",  # Invalid (bad hash)
        "USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788",  # Valid
    ]
    
    with open(input_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(test_data) + '\n')
    
    # Output files
    output_file = temp_dir / "hashes.txt"
    rejects_file = temp_dir / "rejects.txt"
    
    # Import the function to test
    from credforge.responder2hashcat import process_file
    
    # Call the function
    accepted, rejected = process_file(str(input_file), str(output_file), str(rejects_file))
    
    # Verify the results
    assert accepted == 2  # 2 valid NTLM responses
    assert rejected == 1  # 1 invalid NTLM response
    
    # Verify the output files were created
    assert output_file.exists()
    assert rejects_file.exists()
    
    # Check the contents of the output file (valid hashes)
    with open(output_file, 'r', encoding='utf-8') as f:
        valid_hashes = [line.strip() for line in f.readlines() if line.strip()]
    
    assert len(valid_hashes) == 2
    assert any("USER1::DOMAIN:1122334455667788:hash1:hash2:1122334455667788" in line for line in valid_hashes)
    assert any("USER3::DOMAIN:1122334455667788:hash3:hash4:1122334455667788" in line for line in valid_hashes)
    
    # Check the contents of the rejects file
    with open(rejects_file, 'r', encoding='utf-8') as f:
        rejects = [line.strip() for line in f.readlines() if line.strip()]
    
    assert len(rejects) == 1
    assert "USER2::DOMAIN:invalidhash:hash1:hash2:1122334455667788" in rejects[0]

def test_process_file_empty_input(temp_dir):
    """Test process_file with an empty input file."""
    # Create an empty input file
    input_file = temp_dir / "empty.log"
    input_file.touch()
    
    # Output files
    output_file = temp_dir / "hashes.txt"
    rejects_file = temp_dir / "rejects.txt"
    
    # Import the function to test
    from credforge.responder2hashcat import process_file
    
    # Call the function
    accepted, rejected = process_file(str(input_file), str(output_file), str(rejects_file))
    
    # Verify the results
    assert accepted == 0
    assert rejected == 0
    
    # Verify the output files were created but are empty
    assert output_file.exists()
    assert output_file.stat().st_size == 0
    
    assert rejects_file.exists()
    assert rejects_file.stat().st_size == 0
