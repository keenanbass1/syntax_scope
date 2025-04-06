#!/usr/bin/env python3
"""
Script to combine data from different sources into a single dataset.
"""

import utils
from pathlib import Path
from typing import List, Dict, Any

logger = utils.logger

# Input/output paths
ENRICHED_PATH = utils.DATA_DIR / "processed" / "enriched_commands.json"
AI_EXPLANATIONS_PATH = utils.DATA_DIR / "processed" / "ai_explanations.json"
OUTPUT_PATH = utils.DATA_DIR / "processed" / "combined_data.json"

def combine_data() -> List[Dict[str, Any]]:
    """
    Combine data from different sources into a single dataset.

    Returns:
        List of combined command entries
    """
    # Load the enriched command data
    if not ENRICHED_PATH.exists():
        logger.error(f"Enriched commands file not found: {ENRICHED_PATH}")
        return []

    enriched_commands = utils.load_json(ENRICHED_PATH)
    logger.info(f"Loaded {len(enriched_commands)} enriched commands from {ENRICHED_PATH}")

    # Load the AI explanations data if available
    ai_commands = []
    if AI_EXPLANATIONS_PATH.exists():
        ai_commands = utils.load_json(AI_EXPLANATIONS_PATH)
        logger.info(f"Loaded {len(ai_commands)} commands with AI explanations from {AI_EXPLANATIONS_PATH}")

    # Create a dictionary of commands by ID for easier merging
    command_dict = {cmd.get('id'): cmd for cmd in enriched_commands if cmd.get('id')}

    # Merge in AI explanations and tags
    for cmd in ai_commands:
        cmd_id = cmd.get('id')
        if not cmd_id:
            continue

        if cmd_id in command_dict:
            # Update the explanation if it exists
            if cmd.get('explanation'):
                command_dict[cmd_id]['explanation'] = cmd['explanation']
                command_dict[cmd_id]['updated_at'] = cmd.get('updated_at', utils.get_timestamp())
            
            # Update tags if they exist in the AI data
            if cmd.get('tags') and len(cmd.get('tags', [])) > 0:
                # If the original command already has tags, merge them and remove duplicates
                if command_dict[cmd_id].get('tags'):
                    # Combine AI tags with existing tags, removing duplicates
                    existing_tags = set(command_dict[cmd_id]['tags'])
                    ai_tags = set(cmd['tags'])
                    combined_tags = list(existing_tags.union(ai_tags))
                    # Limit to a reasonable number of tags (e.g., 5)
                    command_dict[cmd_id]['tags'] = combined_tags[:5]
                else:
                    # Just use the AI tags if none exist
                    command_dict[cmd_id]['tags'] = cmd['tags']
                
                command_dict[cmd_id]['updated_at'] = cmd.get('updated_at', utils.get_timestamp())
        else:
            # Add the command if it's not already in the dictionary
            command_dict[cmd_id] = cmd

    # Convert back to a list
    combined_commands = list(command_dict.values())

    # Validate against schema
    if not utils.validate_against_schema(combined_commands):
        logger.warning("Combined data does not fully conform to schema")

    # Save the combined data
    utils.save_json(combined_commands, OUTPUT_PATH)
    logger.info(f"Saved {len(combined_commands)} combined commands to {OUTPUT_PATH}")

    # Print statistics
    categories = {}
    with_explanation = 0
    with_tags = 0

    for cmd in combined_commands:
        category = cmd.get('category', 'unknown')
        categories[category] = categories.get(category, 0) + 1

        if cmd.get('explanation'):
            with_explanation += 1
        
        if cmd.get('tags') and len(cmd.get('tags', [])) > 0:
            with_tags += 1

    logger.info(f"Commands with explanations: {with_explanation}/{len(combined_commands)}")
    logger.info(f"Commands with tags: {with_tags}/{len(combined_commands)}")

    logger.info("Category breakdown:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  - {category}: {count} commands")

    return combined_commands

def main():
    """Run the script"""
    combine_data()

if __name__ == "__main__":
    main()
