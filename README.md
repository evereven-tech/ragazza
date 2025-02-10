# Visual PDF to RAG

A tool to convert PDF slides into markdown format with AI-powered content analysis, suitable for loading into LLM Models.

## Features

- Extracts text content from PDF slides
- Generates visual descriptions using Claude AI
- Provides educational purpose analysis for each slide
- Supports error handling and retry mechanisms
- Progress tracking with tqdm
- Comprehensive logging

## Installation

1. Install system dependencies:
   ```bash
   # Ubuntu/Debian
   sudo apt-get install poppler-utils
   
   # macOS
   brew install poppler
   
   # Windows: Download and add Poppler to PATH
   ```

2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## AWS Configuration

Ensure you have AWS credentials configured:
1. Install AWS CLI: `pip install awscli`
2. Run `aws configure`
3. Enter your AWS Access Key ID, Secret Access Key, default region, and output format

## Usage

Basic usage:
```bash
python ragazza.py input.pdf output.md
```

Advanced options:
```bash
python ragazza.py --model "anthropic.claude-3-sonnet-20240229-v1:0" --max-tokens 1000 input.pdf output.md
```

## Output

The script generates:
- A markdown file with structured content for each slide
- Temporary images in ./tmp directory (automatically cleaned up)
- A log file (ragazza.log) with processing details

