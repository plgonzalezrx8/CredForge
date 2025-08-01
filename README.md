# CredForge - Credential Processing and Analysis Toolkit

**CredForge** is a comprehensive collection of Python scripts for processing, analyzing, and managing credential data from various sources including NTDS dumps, password files, and credential lists. This powerful toolkit helps security professionals forge insights from credential datasets with precision and efficiency.

## Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Scripts](#scripts)
  - [split_credentials.py](#split_credentialspy)
  - [combine_list_passwords.py](#combine_list_passwordspy)
  - [process_ntds.py](#process_ntdspy)
  - [password_analyzer.py](#password_analyzerpy)
  - [remove_duplicates.py](#remove_duplicatespy)
  - [responder2hashcat.py](#responder2hashcatpy)
- [Running the Tools](#running-the-tools)
- [Testing](#testing)
- [Usage Examples](#usage-examples)
- [File Formats](#file-formats)
- [Project Structure](#project-structure)

## Overview

This toolkit provides utilities for security professionals and researchers to process and analyze credential data efficiently. The scripts handle various common tasks including:

- Splitting credential files into separate components
- Matching cracked passwords with hash databases
- Filtering NTDS dumps by account status
- Analyzing password frequency and patterns
- Removing duplicate entries from files

## Installation

### Prerequisites
- Python 3.6 or higher
- pip (Python package installer)

### Install from Source

1. Clone the repository:
```bash
git clone https://github.com/yourusername/CredForge.git
cd CredForge
```

2. Install the package in development mode:
```bash
pip install -e .
```

3. Install development dependencies (for testing):
```bash
pip install -r requirements-dev.txt
```

### Verify Installation

```bash
# Test that the package is installed correctly
python -c "import credforge; print('CredForge installed successfully!')"
```

## Scripts

### split_credentials.py

**Purpose:** Splits credential files containing username:hash:password entries into separate files for usernames, passwords, hashes, and combined formats.

**Features:**
- Extracts usernames, passwords, and hashes into separate files
- Creates combined username:password files
- Creates combined username:hash files
- Handles malformed lines gracefully with warnings
- Skips lines with empty hashes
- Provides detailed processing statistics

**Usage:**
```bash
python -m credforge.split_credentials
# OR
python credforge/split_credentials.py
```

**Interactive Prompts:**
- Input file path (e.g., `credentials.txt`)
- Base name for output files (e.g., `processed`)

**Input Format:**
```
username:hash:password
domain\user:ntlmhash:plaintext
```

**Output Files:**
- `{basename}_usernames.txt` - One username per line
- `{basename}_passwords.txt` - One password per line  
- `{basename}_hashes.txt` - One hash per line
- `{basename}_combined.txt` - username:password format
- `{basename}_usernames_hashes.txt` - username:hash format

**Example:**
```bash
Input file: UserAndPasswords.txt
Base name: processed

Output:
- processed_usernames.txt
- processed_passwords.txt
- processed_hashes.txt
- processed_combined.txt
- processed_usernames_hashes.txt
```

---

### combine_list_passwords.py

**Purpose:** Matches cracked passwords with NTDS hash dumps to create username:hash:password credential files.

**Features:**
- Reads cracked password files (hash:password format)
- Processes NTDS dump files to extract usernames and hashes
- Matches NTLM hashes with cracked passwords
- Outputs combined credential files
- Shows processing statistics and preview of matches

**Usage:**
```bash
python -m credforge.combine_list_passwords
# OR
python credforge/combine_list_passwords.py
```

**Interactive Prompts:**
- Path to cracked passwords file
- Path to NTLM hash file (NTDS dump)
- Output file name (default: `Userandpasswords.txt`)

**Input Formats:**

*Cracked passwords file:*
```
hash1:password1
hash2:password2
```

*NTDS hash file:*
```
username:rid:lmhash:ntlmhash::: (status=Enabled)
domain\user:1001:aad3b435b51404ee:ntlmhash::: (status=Disabled)
```

**Output Format:**
```
username:ntlmhash:password
domain\user:ntlmhash:plaintext
```

**Example Output:**
```
NTLM Hash and Password Matcher
===================================
Enter the path to the cracked passwords file: cracked.txt
Enter the path to the NTLM hash file: ntds_dump.txt
Enter the output file name: matched_credentials.txt

Successfully processed files!
Found 826 matches
Results written to matched_credentials.txt
```

---

### process_ntds.py

**Purpose:** Filters NTDS dump files to remove disabled accounts, keeping only active accounts.

**Features:**
- Processes NTDS dump files with account status information
- Filters out accounts with `(status=Disabled)`
- Preserves only active accounts `(status=Enabled)`
- Shows processing progress for large files
- Provides detailed statistics on filtered accounts
- Handles file validation and error checking

**Usage:**
```bash
python -m credforge.process_ntds -w <input_ntds_file> -o <output_file>
# OR
python credforge/process_ntds.py -w <input_ntds_file> -o <output_file>
```

**Arguments:**
- `-w, --ntds-file`: Path to the input NTDS file
- `-o, --output`: Path to the output file for active accounts

**Input Format:**
```
username:rid:lmhash:ntlmhash::: (status=Enabled)
username:rid:lmhash:ntlmhash::: (status=Disabled)
```

**Output Format:**
```
username:rid:lmhash:ntlmhash::: (status=Enabled)
```

**Example:**
```bash
python process_ntds.py -w FULL-HASHES.NTDS -o active_accounts.ntds

Processing FULL-HASHES.NTDS...
Total accounts to process: 10,000
Filtering out disabled accounts...
Processed 10,000 of 10,000 accounts...

Processing complete!
Total accounts processed: 10,000
Disabled accounts found: 3,250 (32.5%)
Active accounts written to active_accounts.ntds: 6,750 (67.5%)
```

---

### password_analyzer.py

**Purpose:** Analyzes password files to identify the most frequently used passwords and password patterns.

**Features:**
- Counts occurrences of each unique password
- Displays top 10 most common passwords
- Shows password reuse statistics
- Calculates percentage distribution
- Handles large password files efficiently
- Provides comprehensive usage statistics

**Usage:**
```bash
python -m credforge.password_analyzer <input_file>
# OR
python credforge/password_analyzer.py <input_file>
```

**Arguments:**
- `password_file`: Path to file containing passwords (one per line)

**Input Format:**
```
password1
password2
password1
password3
```

**Example Output:**
```bash
python password_analyzer.py passwords.txt

Password Analysis for: passwords.txt
============================================================
Total passwords analyzed: 2,553
Unique passwords found: 1,847
Password reuse rate: 1.4x

Top 10 Most Common Passwords:
----------------------------------------
Rank  Password                     Count      % of Total
------------------------------------------------------------
1     P@ssw0rd12                   45         1.76%
2     Welcome1                     32         1.25%
3     Password123                  28         1.10%
4     123456                       25         0.98%
5     password                     22         0.86%
6     admin                        19         0.74%
7     P@ssword1                    17         0.67%
8     qwerty                       15         0.59%
9     letmein                      14         0.55%
10    welcome                      12         0.47%
============================================================
```

---

### remove_duplicates.py

**Purpose:** Identifies and removes duplicate lines from text files while preserving the original order.

**Features:**
- Scans files for duplicate lines
- Reports duplicate lines with line numbers
- Option to remove duplicates in-place or save to new file
- Preserves original line order (keeps first occurrence)
- Shows progress for large files
- Provides detailed statistics on duplicates found

**Usage:**
```bash
# Analyze and modify in-place
python -m credforge.remove_duplicates <input_file>
# OR
python credforge/remove_duplicates.py <input_file>

# Save to new file
python -m credforge.remove_duplicates <input_file> <output_file>
# OR
python credforge/remove_duplicates.py <input_file> <output_file>
```

**Arguments:**
- `input_file`: Path to the file to analyze
- `output_file` (optional): Path to save deduplicated content

**Example Output:**
```bash
python remove_duplicates.py usernames.txt

Finding duplicates...

Found 3 unique duplicate entries:
  "john.doe" - Duplicate on lines: [1, 15, 23]
  "admin" - Duplicate on lines: [5, 18]
  "test.user" - Duplicate on lines: [8, 12, 19]

Total unique lines: 1,250
Total duplicate instances: 6

Do you want to remove duplicates? (y/n): y
Removing duplicates...
Duplicates removed successfully!
Original file backed up as: usernames.txt.backup
```

### responder2hashcat.py

**Purpose:** Processes Responder's NTLMv1/2 challenge/response captures and converts them into Hashcat-compatible formats. It filters valid NTLM authentication attempts and separates them from malformed or invalid entries.

**Features:**
- Validates NTLM response formats
- Separates valid hashes from invalid entries
- Provides detailed processing statistics
- Handles file I/O errors gracefully
- Supports custom output file paths
- Shows progress and summary of processed entries

**Usage:**
```bash
python -m credforge.responder2hashcat <input_file> [output_file] [rejects_file]
# OR
python credforge/responder2hashcat.py <input_file> [output_file] [rejects_file]
```

**Arguments:**
- `input_file`    Path to the Responder capture file (required)
- `output_file`   Path to save valid Hashcat-compatible hashes (default: clean.txt)
- `rejects_file`  Path to save rejected/invalid entries (default: rejects.txt)

**Example:**
```bash
python responder2hashcat.py Responder-Session.log valid_hashes.txt invalid_entries.txt

Processing: Responder-Session.log
Valid hashes will be saved to: valid_hashes.txt
Invalid entries will be saved to: invalid_entries.txt

Processing complete!
Total entries processed: 1245
Accepted (valid) hashes: 1020 (81.9%)
Rejected entries: 225 (18.1%)
```

**Input Format:**
```
username::domain:challenge:response:response
USERNAME::DOMAIN:1122334455667788:00112233445566778899AABBCCDDEEFF:00112233445566778899AABBCCDDEEFF00112233445566778899AABBCCDDEEFF
```

**Output Format (valid hashes):**
```
username::domain:challenge:response:response
```

**Notes:**
- Only lines matching the NTLM response pattern are considered valid
- Empty lines in the input are automatically skipped
- The script handles file encoding issues automatically
- Progress is shown for large files

---

## Running the Tools

CredForge tools can be run in two ways:

### Method 1: As Python Modules (Recommended)
```bash
python -m credforge.tool_name [arguments]
```

### Method 2: Direct Script Execution
```bash
python credforge/tool_name.py [arguments]
```

### Available Tools
- `split_credentials` - Split credential files into components
- `combine_list_passwords` - Match passwords with NTDS dumps
- `process_ntds` - Filter NTDS dumps by account status
- `password_analyzer` - Analyze password patterns and frequency
- `remove_duplicates` - Remove duplicate entries from files
- `responder2hashcat` - Convert Responder captures to Hashcat format

## Testing

### Running All Tests
```bash
# Run all tests with pytest
pytest

# Run tests with verbose output
pytest -v

# Run tests with coverage report
pytest --cov=credforge

# Run tests and generate HTML coverage report
pytest --cov=credforge --cov-report=html
```

### Running Specific Tests
```bash
# Test a specific module
pytest tests/test_split_credentials.py

# Test a specific function
pytest tests/test_password_analyzer.py::test_analyze_passwords

# Run tests matching a pattern
pytest -k "test_split"
```

### Test Structure
The test suite includes comprehensive tests for all modules:
- `tests/test_combine_list_passwords.py` - Tests for password matching functionality
- `tests/test_password_analyzer.py` - Tests for password analysis features
- `tests/test_process_ntds.py` - Tests for NTDS processing
- `tests/test_remove_duplicates.py` - Tests for duplicate removal
- `tests/test_responder2hashcat.py` - Tests for Responder conversion
- `tests/test_split_credentials.py` - Tests for credential splitting

### Test Configuration
Test configuration is managed through:
- `pytest.ini` - Pytest configuration
- `tests/conftest.py` - Shared test fixtures and utilities

## Requirements

- Python 3.6 or higher
- No external dependencies for core functionality (uses only standard library)
- Development dependencies (for testing): pytest, pytest-cov

## Usage Examples

### Complete Workflow Example

1. **Process NTDS dump to get active accounts:**
```bash
python -m credforge.process_ntds -w domain_dump.ntds -o active_accounts.ntds
```

2. **Match cracked passwords with active accounts:**
```bash
python -m credforge.combine_list_passwords
# Input: cracked_passwords.txt, active_accounts.ntds
# Output: matched_credentials.txt
```

3. **Split credentials into separate files:**
```bash
python -m credforge.split_credentials
# Input: matched_credentials.txt
# Output: multiple separated files
```

4. **Analyze password patterns:**
```bash
python -m credforge.password_analyzer matched_credentials_passwords.txt
```

5. **Remove duplicates from any file:**
```bash
python -m credforge.remove_duplicates matched_credentials_usernames.txt
```

### Batch Processing

For processing multiple files, you can use these scripts in batch:

```bash
# Process multiple NTDS files (Linux/Mac)
for file in *.ntds; do
    python -m credforge.process_ntds -w "$file" -o "active_${file}"
done

# Process multiple NTDS files (Windows PowerShell)
Get-ChildItem *.ntds | ForEach-Object {
    python -m credforge.process_ntds -w $_.Name -o "active_$($_.Name)"
}

# Analyze multiple password files (Linux/Mac)
for file in *_passwords.txt; do
    echo "Analyzing $file"
    python -m credforge.password_analyzer "$file" > "${file%.txt}_analysis.txt"
done

# Analyze multiple password files (Windows PowerShell)
Get-ChildItem *_passwords.txt | ForEach-Object {
    Write-Host "Analyzing $($_.Name)"
    python -m credforge.password_analyzer $_.Name > "$($_.BaseName)_analysis.txt"
}
```

## File Formats

### NTDS Dump Format
```
domain\username:RID:LMhash:NTLMhash::: (status=Enabled)
domain\username:RID:LMhash:NTLMhash::: (status=Disabled)
```

### Cracked Passwords Format
```
ntlmhash:plaintext_password
hash1:password1
hash2:password2
```

### Credential Files Format
```
username:hash:password
domain\user:ntlmhash:plaintext
```

### Password Files Format
```
password1
password2
password3
```

## Project Structure

```
CredForge/
├── credforge/                 # Main package directory
│   ├── __init__.py           # Package initialization
│   ├── combine_list_passwords.py
│   ├── password_analyzer.py
│   ├── process_ntds.py
│   ├── remove_duplicates.py
│   ├── responder2hashcat.py
│   ├── setup.py
│   └── split_credentials.py
├── tests/                    # Test suite
│   ├── __init__.py
│   ├── conftest.py          # Test configuration and fixtures
│   ├── test_combine_list_passwords.py
│   ├── test_password_analyzer.py
│   ├── test_process_ntds.py
│   ├── test_remove_duplicates.py
│   ├── test_responder2hashcat.py
│   └── test_split_credentials.py
├── debug/                    # Debug files and development artifacts
├── .gitignore               # Git ignore rules
├── .coverage                # Coverage data
├── pyproject.toml           # Project configuration
├── pytest.ini              # Pytest configuration
├── requirements-dev.txt     # Development dependencies
├── run_tests.py            # Test runner script
└── README.md               # This file
```

## Notes

- Always backup original files before processing
- Scripts handle various edge cases and malformed data gracefully
- Progress indicators are shown for large file processing
- All scripts provide detailed error messages and usage instructions
- Files are processed with UTF-8 encoding by default
- Debug files and development artifacts are stored in the `debug/` folder
- Comprehensive test suite ensures reliability and correctness

## Security Considerations

- These tools are intended for authorized security testing and research only
- Ensure proper handling and storage of sensitive credential data
- Follow your organization's data handling policies
- Consider encrypting processed files containing sensitive information
- The `.gitignore` file is configured to prevent accidental commit of sensitive files

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run the tests (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## License

This project is intended for educational and authorized security testing purposes only.

---

*Last updated: 2025-07-31*
