#!/usr/bin/env python3
"""
Test script for log classifier GUI functionality
"""

import re
import tempfile
import os

def test_regex_pattern():
    """Test that the regex pattern correctly identifies thread IDs"""
    print("Testing regex pattern...")
    
    # Use the same pattern as in the GUI
    thread_pattern = re.compile(r'^<(\d+):\d+>')
    
    test_cases = [
        ("<123:456> Test message", True, "123"),
        ("<789:012> Another message", True, "789"),
        ("No thread ID here", False, None),
        ("<123:456> Multiple matches", True, "123"),
        ("<1:2> Short IDs", True, "1"),
    ]
    
    all_passed = True
    for i, (line, should_match, expected_id) in enumerate(test_cases, 1):
        match = thread_pattern.match(line)
        
        if should_match:
            if match and match.group(1) == expected_id:
                print(f"PASS Test {i}: '{line}' -> ID: {match.group(1)}")
            else:
                print(f"FAIL Test {i}: '{line}' -> Expected ID: {expected_id}, Got: {match.group(1) if match else None}")
                all_passed = False
        else:
            if not match:
                print(f"PASS Test {i}: '{line}' -> No match (correct)")
            else:
                print(f"FAIL Test {i}: '{line}' -> Unexpected match: {match.group(1)}")
                all_passed = False
    
    return all_passed

def test_file_processing():
    """Test the file processing logic"""
    print("\nTesting file processing logic...")
    
    # Create a test log file
    test_content = """<123:456> First message from thread 123
This line belongs to thread 123
<789:012> Message from thread 789
Another line for thread 789
<123:456> Back to thread 123
No thread ID here, should go to last thread
<999:000> New thread
"""
    
    with tempfile.NamedTemporaryFile(mode='w', suffix='.log', delete=False) as f:
        f.write(test_content)
        temp_file = f.name
    
    try:
        # Test the processing logic
        thread_pattern = re.compile(r'^<(\d+):\d+>')
        
        open_files = {}
        last_seen_thread_id = None
        no_owner_key = 'no_thread_id_at_start'
        
        with open(temp_file, 'r', encoding='utf-8') as infile:
            lines = infile.readlines()
            
        for line_num, line in enumerate(lines, 1):
            match = thread_pattern.match(line)
            
            if match:
                current_thread_id = match.group(1)
                last_seen_thread_id = current_thread_id
            else:
                current_thread_id = last_seen_thread_id
            
            target_key = current_thread_id if current_thread_id else no_owner_key
            
            if target_key not in open_files:
                open_files[target_key] = []
            
            open_files[target_key].append(line.strip())
        
        # Verify results
        expected_threads = ['123', '789', '999']
        for thread_id in expected_threads:
            if thread_id in open_files:
                print(f"PASS Thread {thread_id} has {len(open_files[thread_id])} lines")
            else:
                print(f"FAIL Thread {thread_id} not found")
                return False
        
        print("PASS File processing test passed")
        return True
        
    finally:
        os.unlink(temp_file)

def main():
    """Run all tests"""
    print("Running log classifier tests...")
    
    test1_passed = test_regex_pattern()
    test2_passed = test_file_processing()
    
    if test1_passed and test2_passed:
        print("\nPASS All tests passed!")
        return 0
    else:
        print("\nFAIL Some tests failed!")
        return 1

if __name__ == "__main__":
    exit(main())