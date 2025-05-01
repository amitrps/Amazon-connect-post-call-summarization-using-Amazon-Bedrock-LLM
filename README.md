# Amazon Connect Transcript Summarizer using Amazon Bedrock LLM

This project processes Amazon Connect call transcripts stored in S3, generates summaries using Amazon Bedrock LLM, and saves the results back to S3.

## Features

- Reads Amazon Connect JSON transcripts from S3
- Extracts conversation text from different transcript formats
- Generates comprehensive call summaries using Amazon Bedrock LLMs
- Saves summaries back to S3 with timestamps
- Can be deployed as an AWS Lambda function or run locally

## Prerequisites

- Python 3.8+
- AWS account with access to:
  - Amazon S3
  - Amazon Bedrock
  - Amazon Connect (for transcript generation)
- Required IAM permissions:
  - S3 read/write access
  - Bedrock model invocation permissions

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure AWS credentials:
   ```
   aws configure
   ```

## Usage

### As a Lambda Function

Deploy the code as an AWS Lambda function and configure it with the following environment variables:
- `SOURCE_BUCKET`: S3 bucket containing Connect transcripts
- `OUTPUT_BUCKET`: S3 bucket for storing summaries
- `OUTPUT_PREFIX`: (Optional) Prefix for summary files in the output bucket

The Lambda can be triggered by:
- S3 events when new transcripts are uploaded
- Amazon EventBridge scheduled events
- Direct invocation

### Local Execution

For local testing, modify the `test_event` in the script with your bucket and file information:

```python
test_event = {
    'source_bucket': 'your-transcript-bucket',
    'transcript_key': 'transcripts/call-123456.json',
    'output_bucket': 'your-output-bucket',
    'output_prefix': 'call-summaries'
}
```

Then run:
```
python transcript_summarizer.py
```

## Deployment

### AWS Lambda Deployment

1. Package the code:
   ```
   zip -r transcript_summarizer.zip transcript_summarizer.py
   ```

2. Create a Lambda function with the appropriate IAM role and upload the zip file.

3. Configure environment variables in the Lambda console.

4. Set up triggers as needed (S3 events, EventBridge, etc.).

## Customization

- Modify the `generate_summary` function to adjust the prompt or model parameters
- Update the `extract_conversation` function if your transcript format differs
- Add additional processing or analytics as needed
