#!/usr/bin/env python3
"""
md_link_inline.py

This script converts reference-style markdown links to inline-style links.

Usage:
    python md_link_inline.py <input_file.md>

Functions:
    main() -> None
        Main function to handle argument parsing and script workflow.
    
    parse_arguments() -> str
        Parse command-line arguments and return the input file path.
    
    validate_file(file_path: str) -> None
        Validate that the input file exists and is a markdown file.
    
    duplicate_file(input_file: str) -> str
        Create a duplicate of the input file with `-converted` appended to the name.
    
    process_file(input_file: str, output_file: str) -> None
        Process the markdown file to convert reference-style links to inline-style links.
    
    log_changes(input_file: str, output_file: str) -> None
        Log the changes made during processing.

Versions: 1.0.0 - 2024-12-06 - Initial script.
"""

import os
import sys
import re
import shutil
from pathlib import Path
import argparse


def main():
    """Main function to handle argument parsing and script workflow."""
    try:
        input_file = parse_arguments()
        validate_file(input_file)
        output_file = duplicate_file(input_file)
        process_file(input_file, output_file)
        print(f"Conversion completed. Output saved to: {output_file}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def parse_arguments():
    """Parse command-line arguments and return the input file path."""
    parser = argparse.ArgumentParser(
        description="Convert reference-style links in markdown to inline-style links."
    )
    parser.add_argument("input_file", help="Path to the markdown file to convert.")
    args = parser.parse_args()
    return args.input_file


def validate_file(file_path):
    """Validate that the input file exists and is a markdown file."""
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.endswith(".md"):
        raise ValueError(
            f"Invalid file type. Expected a markdown file (.md): {file_path}"
        )


def duplicate_file(input_file):
    """Create a duplicate of the input file with `-converted` appended to the name."""
    input_path = Path(input_file)
    output_file = input_path.with_name(
        f"{input_path.stem}-converted{input_path.suffix}"
    )
    shutil.copy(input_file, output_file)
    return str(output_file)


def process_file(input_file, output_file):
    """Process the markdown file to convert reference-style links to inline-style links."""
    with open(input_file, "r", encoding="utf-8") as f:
        content = f.read()

    # Extract reference links
    reference_links = dict(re.findall(r"^\[([^\]]+)\]:\s*(.+)$", content, re.MULTILINE))
    if not reference_links:
        print("No reference links found to convert.")
        return

    # Replace reference-style links with inline-style links
    def replace_link(match):
        text = match.group(1)
        ref_key = match.group(2)
        if ref_key in reference_links:
            return f"[{text}]({reference_links[ref_key]})"
        return match.group(0)  # Return the original if no match is found

    updated_content = re.sub(r"\[([^\]]+)\]\[([^\]]+)\]", replace_link, content)

    # Remove reference links from the content
    updated_content = re.sub(
        r"^\[([^\]]+)\]:\s*(.+)$", "", updated_content, flags=re.MULTILINE
    ).strip()

    # Save the updated content to the output file
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(updated_content)

    log_changes(input_file, output_file)


def log_changes(input_file, output_file):
    """Log the changes made during processing."""
    log_path = os.path.expanduser("~/md_link_inline.log")
    with open(log_path, "a", encoding="utf-8") as log:
        log.write(
            f"Processed file: {os.path.relpath(input_file)} -> {os.path.relpath(output_file)}\n"
        )
    print(f"Changes logged to: {log_path}")


if __name__ == "__main__":
    main()
