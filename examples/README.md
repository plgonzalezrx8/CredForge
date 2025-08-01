# CredForge Example Files

This directory contains sample data files that demonstrate how to use each tool in the CredForge toolkit. These files contain dummy/fake data for testing purposes only.

## Example Files

### 1. `sample_ntds_dump.txt`
**Used with:** `process_ntds` tool
**Description:** Sample NTDS dump file with both enabled and disabled accounts
**Usage:**
```bash
credforge-process-ntds -w examples/sample_ntds_dump.txt -o examples/active_accounts.txt
```

### 2. `sample_hash_plaintext.txt`
**Used with:** `combine_list_passwords` tool
**Description:** Sample file with hash:plaintext pairs (cracked passwords)
**Usage:**
```bash
credforge-combine-list-passwords
# When prompted:
# - Cracked passwords file: examples/sample_hash_plaintext.txt
# - NTDS file: examples/sample_ntds_dump.txt
# - Output file: examples/matched_output.txt
```

### 3. `sample_user_hash_plaintext.txt`
**Used with:** `split_credentials` tool
**Description:** Sample credential file with username:hash:plaintext format
**Usage:**
```bash
credforge-split-credentials examples/sample_user_hash_plaintext.txt examples/output/
```

### 4. `sample_ntlm_responses.txt`
**Used with:** `responder2hashcat` tool
**Description:** Sample NTLM challenge/response captures (includes some invalid entries)
**Usage:**
```bash
credforge-responder2hashcat examples/sample_ntlm_responses.txt examples/clean_hashes.txt examples/rejected.txt
```

### 5. `sample_with_duplicates.txt`
**Used with:** `remove_duplicates` tool
**Description:** Sample file containing duplicate entries
**Usage:**
```bash
credforge-remove-duplicates examples/sample_with_duplicates.txt examples/deduplicated.txt
```

### 6. `sample_plaintext_list.txt`
**Used with:** `password_analyzer` tool
**Description:** Sample list of plaintext passwords for analysis
**Usage:**
```bash
credforge-password-analyzer examples/sample_plaintext_list.txt
```

## Quick Test Workflow

Try this complete workflow to see all tools in action:

```bash
# 1. Process NTDS dump to get active accounts
credforge-process-ntds -w examples/sample_ntds_dump.txt -o examples/active_accounts.txt

# 2. Combine cracked passwords with NTDS data
credforge-combine-list-passwords
# Use: examples/sample_hash_plaintext.txt and examples/active_accounts.txt

# 3. Split the combined credentials
credforge-split-credentials examples/matched_output.txt examples/split_output/

# 4. Analyze password patterns
credforge-password-analyzer examples/sample_plaintext_list.txt

# 5. Remove duplicates from any file
credforge-remove-duplicates examples/sample_with_duplicates.txt examples/clean_list.txt

# 6. Process NTLM responses
credforge-responder2hashcat examples/sample_ntlm_responses.txt examples/valid_hashes.txt examples/invalid_entries.txt
```

## Important Notes

- All data in these files is **fake/dummy data** for demonstration purposes only
- These files are safe to use for testing and learning
- The hashes and passwords are not real credentials
- Use these examples to understand tool functionality before working with real data
- Always follow your organization's security policies when working with actual credential data

## File Formats

Each example file demonstrates the expected input format for its corresponding tool. Refer to the main README.md for detailed format specifications.
