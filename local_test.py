#!/usr/bin/env python3
"""
Local test script for the transcript summarizer.
This script simulates the S3 environment by reading from a local file.
"""

import json
import os
import boto3
from transcript_summarizer import generate_summary, extract_conversation
from dotenv import load_dotenv

# Load environment variables from .env file if present
load_dotenv()

def local_test():
    """Run a local test of the transcript summarization"""
    
    # Check if AWS credentials are configured
    try:
        boto3.client('sts').get_caller_identity()
        print("AWS credentials verified successfully")
    except Exception as e:
        print(f"AWS credentials error: {e}")
        print("Please run 'aws configure' to set up your AWS credentials")
        return
    
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
    
    # Initialize Bedrock client
    try:
        bedrock_runtime = boto3.client('bedrock-runtime')
        print("\nConnected to Amazon Bedrock")
    except Exception as e:
        print(f"\nError connecting to Amazon Bedrock: {e}")
        print("Make sure you have the necessary permissions and Bedrock is available in your region")
        return
    
    # Generate summary
    try:
        print("\nGenerating summary with Bedrock (this may take a moment)...")
        summary = generate_summary(bedrock_runtime, conversation_text)
        print("\n--- Generated Summary ---")
        print(summary)
        
        # Save summary to local file
        with open('sample_summary.txt', 'w') as f:
            f.write(summary)
        print("\nSummary saved to sample_summary.txt")
    except Exception as e:
        print(f"\nError generating summary: {e}")
        return

if __name__ == "__main__":
    local_test()
