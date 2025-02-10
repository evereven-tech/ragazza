import os
import sys
import time
import json
import shutil
import logging
import argparse
from datetime import datetime
from pathlib import Path
import PyPDF2
from pdf2image import convert_from_path
import boto3
import random
from tqdm import tqdm

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s: %(message)s',
    handlers=[
        logging.FileHandler('ragazza.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def exponential_backoff(attempt, max_attempts=5, base_delay=1):
    """Implement exponential backoff with jitter"""
    if attempt >= max_attempts:
        raise Exception("Maximum retry attempts reached")
    delay = min(300, base_delay * (2 ** attempt) + random.uniform(0, 0.1))
    time.sleep(delay)

def invoke_claude(prompt, bedrock_client, max_attempts=5):
    """Invoke Claude through AWS Bedrock with retry logic"""
    body = json.dumps({
        "anthropic_version": "bedrock-2023-05-31",
        "max_tokens": 1000,
        "temperature": 0,
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ]
    })

    for attempt in range(max_attempts):
        try:
            response = bedrock_client.invoke_model(
                modelId="anthropic.claude-3-sonnet-20240229-v1:0",
                body=body
            )
            response_body = json.loads(response.get('body').read())
            return response_body['content'][0]['text']
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {str(e)}")
            exponential_backoff(attempt)
    
    raise Exception("Failed to get response from Claude after all retries")

def create_temp_dir(pdf_name, timestamp):
    """Create temporary directory for intermediate files"""
    temp_dir = f"./tmp/{pdf_name}_{timestamp}"
    os.makedirs(temp_dir, exist_ok=True)
    return temp_dir

def extract_text_from_pdf(pdf_path, page_num):
    """Extract text from a PDF page"""
    with open(pdf_path, 'rb') as file:
        pdf_reader = PyPDF2.PdfReader(file)
        page = pdf_reader.pages[page_num]
        return page.extract_text().strip()

def get_page_description(image_path, bedrock_client):
    """Get page description using Claude"""
    prompt = f"""Please describe the visual content of this slide objectively and in detail. 
    Focus on visual elements, layout, graphics, diagrams, and overall structure."""
    
    return invoke_claude(prompt, bedrock_client)

def get_page_explanation(text_content, visual_description, bedrock_client):
    """Get content explanation using Claude"""
    prompt = f"""Based on the extracted text and visual description of the slide, 
    explain the educational purpose and main message it tries to convey.
    
    Extracted text: {text_content}
    
    Visual description: {visual_description}"""
    
    return invoke_claude(prompt, bedrock_client)

def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(description='Convert PDF to markdown with AI analysis')
    parser.add_argument('input', help='Input PDF file path')
    parser.add_argument('output', help='Output markdown file path')
    parser.add_argument('--model', default='anthropic.claude-3-5-sonnet-20241022-v2:0', help='AWS Bedrock Claude model to use')
    parser.add_argument('--max-tokens', type=int, default=1000, help='Maximum tokens for Claude response')
    return parser.parse_args()

def cleanup_temp_dir(temp_dir):
    """Clean up temporary directory"""
    try:
        shutil.rmtree(temp_dir)
        logger.info(f"Temporary directory {temp_dir} cleaned up")
    except Exception as e:
        logger.error(f"Could not remove temporary directory: {e}")

def main():
    try:
        args = parse_arguments()
        input_pdf = args.input
        output_md = args.output
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        pdf_name = Path(input_pdf).stem
        
        # Create temporary directory
        temp_dir = create_temp_dir(pdf_name, timestamp)
        
        # Initialize AWS Bedrock client for N. Virginia region
        bedrock_runtime = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        # Convert PDF to images
        logger.info("Converting PDF to images...")
        images = convert_from_path(input_pdf)
        
        with open(output_md, 'w', encoding='utf-8') as md_file:
            for page_num, image in tqdm(enumerate(images), total=len(images), desc="Processing Pages"):
                logger.info(f"Processing page {page_num + 1}")
                
                # Save page image
                image_path = f"{temp_dir}/page_{page_num + 1}.png"
                image.save(image_path)
                
                # Extract text
                text_content = extract_text_from_pdf(input_pdf, page_num)
                
                # Get visual description
                visual_description = get_page_description(image_path, bedrock_runtime)
                
                # Get explanation
                explanation = get_page_explanation(text_content, visual_description, bedrock_runtime)
                
                # Write to markdown file
                md_file.write(f"## Page {page_num + 1}\n\n")
                md_file.write("### Extracted Content\n")
                md_file.write(f"```\n{text_content}\n```\n\n")
                md_file.write("### Visual Description\n")
                md_file.write(f"{visual_description}\n\n")
                md_file.write("### Content Explanation\n")
                md_file.write(f"{explanation}\n\n")
                md_file.write("---\n\n")
                
    except Exception as e:
        logger.error(f"Error processing PDF: {e}")
        sys.exit(1)
    finally:
        # Clean up temporary directory
        cleanup_temp_dir(temp_dir)

if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError:
        logger.error(f"Error: Input PDF file not found.")
        sys.exit(1)
    except PermissionError:
        logger.error(f"Error: Permission denied when accessing files.")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)
    finally:
        # Cleanup will be handled by the context manager
        pass
