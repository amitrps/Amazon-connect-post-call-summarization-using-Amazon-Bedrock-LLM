#!/usr/bin/env python3
"""
Mock test script for the transcript summarizer.
This script simulates the entire process without requiring Bedrock access.
"""

import json
import os
from transcript_summarizer import extract_conversation

def mock_generate_summary(conversation_text):
    """
    Mock function to generate a summary without using Bedrock
    
    Args:
        conversation_text (str): The conversation text to summarize
        
    Returns:
        str: Generated summary
    """
    print("Generating mock summary (simulating Bedrock call)...")
    
    # Create a mock summary based on the conversation
    summary = """
Main reason for the call:
The customer called because their order (ABC123456) was delayed. It was supposed to arrive yesterday but had not been received yet.

Key points discussed:
- Customer was concerned about the delay as they needed the items for an event this weekend
- Agent confirmed the order was shipped on Monday
- There was a delay with the carrier
- According to tracking information, the order should be delivered by the end of the day

Issues identified:
- Shipping delay with the carrier
- Customer anxiety about receiving items in time for weekend event

Resolution or next steps:
- Agent added a note to prioritize the order
- Agent sent the tracking link to the customer's email
- Customer can monitor the delivery status

Follow-up actions required:
- None specified, as the order is expected to be delivered by the end of the day
"""
    return summary

def local_mock_test():
    """Run a local test of the transcript summarization with mocked Bedrock"""
    
    # Load sample transcript
    try:
        with open('sample_transcript.json', 'r') as f:
            transcript_data = json.load(f)
        print("Loaded sample transcript successfully")
    except FileNotFoundError:
        print("Error: sample_transcript.json not found")
        return
    except json.JSONDecodeError:
        print("Error: Invalid JSON in sample_transcript.json")
        return
    
    # Extract conversation
    conversation_text = extract_conversation(transcript_data)
    print("\n--- Extracted Conversation ---")
    print(conversation_text)
    
    # Generate mock summary
    try:
        summary = mock_generate_summary(conversation_text)
        print("\n--- Generated Summary ---")
        print(summary)
        
        # Save summary to local file
        with open('sample_summary.txt', 'w') as f:
            f.write(summary)
        print("\nSummary saved to sample_summary.txt")
    except Exception as e:
        print(f"\nError generating summary: {e}")
        return
    
    # Explain the full process
    print("\n--- Process Explanation ---")
    print("1. In a real deployment, the script would:")
    print("   - Download the transcript from S3")
    print("   - Extract the conversation (as shown above)")
    print("   - Send the conversation to Amazon Bedrock for summarization")
    print("   - Save the summary back to S3")
    print("\n2. When deployed as a Lambda function:")
    print("   - It can be triggered by S3 events when new transcripts are uploaded")
    print("   - The Lambda would process the transcript and store the summary")
    print("   - Environment variables would configure the buckets and paths")

if __name__ == "__main__":
    local_mock_test()
