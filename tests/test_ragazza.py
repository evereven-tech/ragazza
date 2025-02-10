import pytest
from ragazza.ragazza import parse_arguments

def test_parse_arguments():
    """Test the argument parser with basic inputs"""
    args = parse_arguments(['input.pdf', 'output.md'])
    assert args.input == 'input.pdf'
    assert args.output == 'output.md'
