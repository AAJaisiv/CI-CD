"""
AWS Lambda function for data processing using boto3.
This function demonstrates AWS SDK usage and data engineering concepts.
"""

import json
import boto3
import csv
import io
from datetime import datetime
from typing import Dict, Any, List
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Initialize AWS clients
s3_client = boto3.client('s3')
lambda_client = boto3.client('lambda')

class DataProcessor:
    """Process data using AWS services."""
    
    def __init__(self, bucket_name: str):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3')
    
    def download_data(self, key: str) -> List[Dict[str, Any]]:
        """Download data from S3 and return as list of dictionaries."""
        try:
            logger.info(f"Downloading data from s3://{self.bucket_name}/{key}")
            
            # Download file from S3
            response = self.s3_client.get_object(Bucket=self.bucket_name, Key=key)
            data = response['Body'].read().decode('utf-8')
            
            # Parse CSV data
            csv_reader = csv.DictReader(io.StringIO(data))
            rows = list(csv_reader)
            
            logger.info(f"Successfully downloaded {len(rows)} rows from {key}")
            
            return rows
            
        except Exception as e:
            logger.error(f"Error downloading data: {str(e)}")
            raise
    
    def process_data(self, data: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Process the data and return metrics."""
        try:
            logger.info("Processing data...")
            
            if not data:
                return {
                    'total_rows': 0,
                    'total_columns': 0,
                    'processing_timestamp': datetime.now().isoformat()
                }
            
            # Basic data processing
            processed_data = {
                'total_rows': len(data),
                'total_columns': len(data[0]) if data else 0,
                'processing_timestamp': datetime.now().isoformat()
            }
            
            # Calculate numeric metrics if amount column exists
            if data and 'amount' in data[0]:
                amounts = []
                for row in data:
                    try:
                        amount = float(row['amount'])
                        amounts.append(amount)
                    except (ValueError, KeyError):
                        continue
                
                if amounts:
                    processed_data.update({
                        'total_amount': sum(amounts),
                        'average_amount': sum(amounts) / len(amounts),
                        'min_amount': min(amounts),
                        'max_amount': max(amounts)
                    })
            
            logger.info(f"Processing complete. Metrics: {processed_data}")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing data: {str(e)}")
            raise
    
    def upload_results(self, results: Dict[str, Any], key: str) -> str:
        """Upload processing results to S3."""
        try:
            logger.info(f"Uploading results to s3://{self.bucket_name}/{key}")
            
            # Convert results to JSON
            results_json = json.dumps(results, indent=2)
            
            # Upload to S3
            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=key,
                Body=results_json,
                ContentType='application/json'
            )
            
            logger.info(f"Results uploaded successfully to {key}")
            return f"s3://{self.bucket_name}/{key}"
            
        except Exception as e:
            logger.error(f"Error uploading results: {str(e)}")
            raise

def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    AWS Lambda handler function.
    
    Expected event structure:
    {
        "input_file": "data/input.csv",
        "output_file": "results/processed_data.json"
    }
    """
    try:
        logger.info("Lambda function started")
        logger.info(f"Event: {json.dumps(event)}")
        
        # Get bucket name from environment or event
        bucket_name = event.get('bucket_name', 'ci-cd-portfolio-dev-data')
        input_file = event.get('input_file', 'data/input.csv')
        output_file = event.get('output_file', f'results/processed_data_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
        
        # Initialize data processor
        processor = DataProcessor(bucket_name)
        
        # Process data
        data = processor.download_data(input_file)
        results = processor.process_data(data)
        
        # Upload results
        results_s3_path = processor.upload_results(results, output_file)
        
        # Prepare response
        response = {
            'statusCode': 200,
            'body': {
                'message': 'Data processing completed successfully',
                'input_file': input_file,
                'output_file': results_s3_path,
                'metrics': results,
                'timestamp': datetime.now().isoformat()
            }
        }
        
        logger.info(f"Lambda function completed successfully: {response}")
        return response
        
    except Exception as e:
        logger.error(f"Lambda function failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': {
                'error': str(e),
                'message': 'Data processing failed',
                'timestamp': datetime.now().isoformat()
            }
        } 