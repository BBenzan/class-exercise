import argparse

parser = argparse.ArgumentParser(description="Analyze a data file")

parser.add_argument(
    "--input", "-i",
    required=True,
    help="Path to input CSV file"
)

# Add named arguments (optional)
parser.add_argument(
    "--output", "-o",
    default="results.txt",
    help="Output file path"
)

parser.add_argument(
    "--verbose", "-v", 
    action="store_true", 
    help="Print detailed information"
    # Note 1: verbose has its default value as False
    # Note 2: action="store_true" sets this to True.
)

# Parse the command-line arguments
args = parser.parse_args()
