#!/usr/bin/env python3
"""
Script to export the combined data to a JSON file for the frontend.
"""

import utils
from pathlib import Path
from typing import List, Dict, Any

logger = utils.logger

# Input/output paths
INPUT_PATH = utils.DATA_DIR / "processed" / "combined_data.json"
OUTPUT_PATH = utils.PUBLIC_DATA_DIR / "syntax.json"

def export_to_json() -> List[Dict[str, Any]]:
    """
    Export the combined data to a JSON file for the frontend.

    Returns:
        List of exported command entries
    """
    # Load the combined data
    if not INPUT_PATH.exists():
        logger.error(f"Combined data file not found: {INPUT_PATH}")
        return []

    commands = utils.load_json(INPUT_PATH)
    logger.info(f"Loaded {len(commands)} commands from {INPUT_PATH}")

    # Ensure the output directory exists
    OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Save the data to the public directory
    utils.save_json(commands, OUTPUT_PATH)
    logger.info(f"Exported {len(commands)} commands to {OUTPUT_PATH}")

    # Print statistics
    categories = {}
    with_explanation = 0
    with_tags = 0

    for cmd in commands:
        category = cmd.get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1

        if cmd.get('explanation'):
            with_explanation += 1
            
        if cmd.get('tags') and len(cmd.get('tags', [])) > 0:
            with_tags += 1

    logger.info(f"Commands with explanations: {with_explanation}/{len(commands)}")
    logger.info(f"Commands with tags: {with_tags}/{len(commands)}")

    logger.info("Category breakdown:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  - {category}: {count} commands")

    return commands

def main():
    """Run the script"""
    export_to_json()

if __name__ == "__main__":
    main()
