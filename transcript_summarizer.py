import json
import boto3
import os
from datetime import datetime

def process_transcript(bucket_name, transcript_key, output_bucket, output_prefix):
    """
    Process Amazon Connect transcript, generate summary using Bedrock, and save to S3
    
    Args:
        bucket_name (str): Source S3 bucket containing the transcript
        transcript_key (str): S3 key for the transcript JSON file
        output_bucket (str): Destination S3 bucket for the summary
        output_prefix (str): Prefix for the output summary file
    """
    # Initialize AWS clients
    s3_client = boto3.client('s3')
    bedrock_runtime = boto3.client('bedrock-runtime')
    
    # Download transcript from S3
    print(f"Downloading transcript from s3://{bucket_name}/{transcript_key}")
    response = s3_client.get_object(Bucket=bucket_name, Key=transcript_key)
    transcript_data = json.loads(response['Body'].read().decode('utf-8'))
    
    # Extract conversation from transcript
    conversation_text = extract_conversation(transcript_data)
    
    # Generate summary using Bedrock
    summary = generate_summary(bedrock_runtime, conversation_text)
    
    # Save summary to S3
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
    filename = os.path.basename(transcript_key).replace('.json', '')
    output_key = f"{output_prefix}/{filename}-summary-{timestamp}.txt"
    
    print(f"Saving summary to s3://{output_bucket}/{output_key}")
    s3_client.put_object(
        Bucket=output_bucket,
        Key=output_key,
        Body=summary,
        ContentType='text/plain'
    )
    
    return {
        'transcript_key': transcript_key,
        'summary_key': output_key,
        'summary': summary
    }

def extract_conversation(transcript_data):
    """
    Extract conversation text from Amazon Connect transcript JSON
    
    Args:
        transcript_data (dict): The transcript JSON data
        
    Returns:
        str: Formatted conversation text
    """
    conversation = []
    
    # Handle different transcript formats
    if 'Transcript' in transcript_data:
        # Format 1: Direct transcript array
        items = transcript_data.get('Transcript', [])
    elif 'Participants' in transcript_data and 'Transcript' in transcript_data:
        # Format 2: Participants and transcript sections
        items = transcript_data.get('Transcript', [])
    else:
        # Try to find transcript items in the structure
        items = []
        for key, value in transcript_data.items():
            if isinstance(value, list) and len(value) > 0 and 'ParticipantId' in value[0]:
                items = value
                break
    
    # Process transcript items
    for item in items:
        participant_id = item.get('ParticipantId', '')
        participant_role = item.get('ParticipantRole', 'Unknown')
        content = item.get('Content', '')
        
        if content:
            conversation.append(f"{participant_role}: {content}")
    
    return "\n".join(conversation)

def generate_summary(bedrock_runtime, conversation_text):
    """
    Generate summary using Amazon Bedrock
    
    Args:
        bedrock_runtime: Bedrock runtime client
        conversation_text (str): The conversation text to summarize
        
    Returns:
        str: Generated summary
    """
    # Using Claude model for summarization
    model_id = "anthropic.claude-3-7-sonnet-20250219-v1:0"  # Update with your preferred model
    
    prompt = f"""
    Below is a transcript from a customer service call. Please provide a comprehensive summary that includes:
    
    1. Main reason for the call
    2. Key points discussed
    3. Any issues identified
    4. Resolution or next steps
    5. Any follow-up actions required
    
    Transcript:
    {conversation_text}
    
    Summary:
    """
    
    request_body = {
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0.5,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    }
    
    response = bedrock_runtime.invoke_model(
        modelId=model_id,
        body=json.dumps(request_body)
    )
    
    response_body = json.loads(response.get('body').read())
    summary = response_body.get('content', [{}])[0].get('text', '')
    
    return summary

def lambda_handler(event, context):
    """
    AWS Lambda handler function
    
    Args:
        event (dict): Lambda event data
        context: Lambda context
        
    Returns:
        dict: Processing results
    """
    # Get parameters from event or environment variables
    source_bucket = event.get('source_bucket', os.environ.get('SOURCE_BUCKET'))
    transcript_key = event.get('transcript_key', os.environ.get('TRANSCRIPT_KEY'))
    output_bucket = event.get('output_bucket', os.environ.get('OUTPUT_BUCKET'))
    output_prefix = event.get('output_prefix', os.environ.get('OUTPUT_PREFIX', 'summaries'))
    
    if not all([source_bucket, transcript_key, output_bucket]):
        raise ValueError("Missing required parameters: source_bucket, transcript_key, output_bucket")
    
    result = process_transcript(source_bucket, transcript_key, output_bucket, output_prefix)
    return result

# For local testing
if __name__ == "__main__":
    # Replace with your actual values for testing
    test_event = {
        'source_bucket': 'your-transcript-bucket',
        'transcript_key': 'transcripts/call-123456.json',
        'output_bucket': 'your-output-bucket',
        'output_prefix': 'call-summaries'
    }
    
    result = lambda_handler(test_event, None)
    print(f"Summary generated: {result['summary']}")
