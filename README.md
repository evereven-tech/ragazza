# Ragazza

> The name "Ragazza" was chosen as it's memorable, simple, and cleverly contains "RAG" (Retrieval-Augmented Generation) within its spelling.

A tool to convert PDF slides into markdown format with AI-powered content analysis, suitable for loading into LLM Models.

## Features

- Extracts text content from PDF slides
- Generates visual descriptions using Claude Models (or any other AWS Bedrock availables)
- Provides educational purpose analysis for each slide
- Supports error handling and retry mechanisms
- Progress tracking with tqdm
- Comprehensive logging

## Installation

### Using pip

```bash
pip install ragazza
```

### From source

1. Clone the repository:
   ```bash
   git clone https://github.com/evereven-tech/ragazza.git
   cd ragazza
   ```

2. Use make commands for development:
   ```bash
   make help         # Show all available commands
   make install      # Install package in production mode
   make install-dev  # Install in development mode with dev dependencies
   make build        # Build package distribution
   make lint         # Check style with flake8
   make test         # Run tests
   make clean        # Clean up build artifacts
   ```

### System Dependencies

You'll need to install Poppler for PDF processing:
```bash
# Ubuntu/Debian
sudo apt-get install poppler-utils

# macOS
brew install poppler

# Windows: Download and add Poppler to PATH
```

## AWS Configuration

This tool requires access to AWS Bedrock to use Claude AI models for content analysis:

1. Ensure you have an AWS account with Bedrock access enabled
2. Request model access for Claude models in the AWS Bedrock console
3. Configure your AWS credentials:
   ```bash
   pip install awscli
   aws configure
   ```
4. Enter your AWS Access Key ID, Secret Access Key, and set default region to 'us-east-1'

**Important notes:**
- Using AWS Bedrock incurs costs based on token usage
- AWS Bedrock may not be available in all regions
- Your AWS user/role needs permissions for 'bedrock:InvokeModel'
- If you don't have AWS Bedrock access, this tool cannot function properly

## Usage

Basic usage:
```bash
ragazza input.pdf output.md
```

Advanced options:
```bash
ragazza --model "anthropic.claude-3-5-sonnet-20241022-v2:0" --max-tokens 1000 input.pdf output.md
```

## Output

The script generates:
- A markdown file with structured content for each slide
- Temporary images in ./tmp directory (automatically cleaned up)
- A log file (ragazza.log) with processing details
