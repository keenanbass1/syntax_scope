#!/usr/bin/env python3
"""
Script to enrich command data with AI-generated explanations and tags using Ollama.
"""

import os
import time
import requests
import json
from typing import Dict, List, Any, Optional, Tuple
import utils

logger = utils.logger

# Ollama API settings
OLLAMA_HOST = os.environ.get("OLLAMA_HOST", "http://localhost:11434")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3")
OLLAMA_TIMEOUT = int(os.environ.get("OLLAMA_TIMEOUT", "30"))

# Input/output paths
INPUT_PATH = utils.DATA_DIR / "processed" / "enriched_commands.json"
OUTPUT_PATH = utils.DATA_DIR / "processed" / "ai_explanations.json"

# Create sample data for testing
def create_sample_data() -> List[Dict[str, Any]]:
    """
    Create sample data for testing the enrichment process.
    
    Returns:
        List of sample command entries
    """
    return [
        {
            "command": "ls -la",
            "description": "List directory contents with detailed information",
            "category": "bash",
            "examples": [
                {"code": "ls -la /etc", "description": "List detailed contents of /etc directory"}
            ]
        },
        {
            "command": "grep -r 'pattern' .",
            "description": "Search recursively for a pattern in current directory",
            "category": "bash",
            "examples": [
                {"code": "grep -r 'TODO' ./src", "description": "Find all TODOs in source code"}
            ]
        },
        {
            "command": "curl -X POST https://api.example.com/data",
            "description": "Send POST request to an API endpoint",
            "category": "bash",
            "examples": [
                {"code": "curl -X POST -H 'Content-Type: application/json' -d '{\"key\":\"value\"}' https://api.example.com/data", 
                 "description": "POST JSON data to an API"}
            ]
        }
    ]

def generate_explanation_prompt(command: Dict[str, Any]) -> str:
    """
    Generate a prompt for the AI to explain a command.

    Args:
        command: Command data dictionary

    Returns:
        Prompt string for the AI
    """
    cmd = command.get('command', '')
    description = command.get('description', '')
    category = command.get('category', '')
    examples = command.get('examples', [])

    example_text = ""
    if examples:
        example_text = "Examples:\n"
        for i, example in enumerate(examples[:3], 1):  # Limit to 3 examples
            example_text += f"{i}. {example.get('code', '')}: {example.get('description', '')}\n"

    prompt = f"""Explain the following command in detail:

Command: {cmd}
Description: {description}
Category: {category}
{example_text}

Provide a comprehensive explanation that covers:
1. What the command does
2. How it works
3. Common use cases
4. Important options or flags
5. Any potential pitfalls or security considerations

Keep your explanation clear, concise, and informative for someone who might be new to this command.
Limit your response to 300 words.
"""
    return prompt

def generate_tags_prompt(command: Dict[str, Any]) -> str:
    """
    Generate a prompt for the AI to suggest tags for a command.

    Args:
        command: Command data dictionary

    Returns:
        Prompt string for the AI
    """
    cmd = command.get('command', '')
    description = command.get('description', '')
    category = command.get('category', '')

    prompt = f"""You are an expert shell tutor. Given this command, suggest 2-3 general tags that describe what it does.

Command: {cmd}
Description: {description}
Category: {category}

Return ONLY a JSON array of 2-3 lowercase string tags without explanation, like this:
["tag1", "tag2", "tag3"]

Focus on functional categories like "filesystem", "networking", "search", "permissions", "compression", etc.
"""
    return prompt

def get_ai_explanation(prompt: str, max_retries: int = 3) -> Optional[str]:
    """
    Get an AI-generated explanation using Ollama.

    Args:
        prompt: The prompt to send to the AI
        max_retries: Maximum number of retry attempts

    Returns:
        AI-generated explanation or None if failed
    """
    url = f"{OLLAMA_HOST}/api/generate"

    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }

    for attempt in range(max_retries):
        try:
            response = requests.post(url, json=payload, timeout=OLLAMA_TIMEOUT)
            response.raise_for_status()

            result = response.json()
            return result.get('response', '').strip()

        except requests.exceptions.RequestException as e:
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt + 1 < max_retries:
                # Exponential backoff
                wait_time = 2 ** attempt
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    logger.error(f"Failed to get AI response after {max_retries} attempts")
    return None

def parse_tags_response(response: str) -> List[str]:
    """
    Parse the AI response to extract tags.
    
    Args:
        response: The AI-generated response containing tags
        
    Returns:
        List of tags as lowercase strings
    """
    if not response:
        return []
    
    # Clean up the response to ensure it's valid JSON
    # First, try to find a JSON array in the response
    response = response.strip()
    
    # If the response is wrapped in ```json and ```, extract just the JSON part
    if response.startswith("```") and response.endswith("```"):
        response = response[response.find("\n")+1:response.rfind("\n")]
    
    # Try to parse as JSON
    try:
        tags = json.loads(response)
        if isinstance(tags, list):
            # Convert all tags to lowercase strings and remove duplicates
            return list(set(tag.lower() for tag in tags if isinstance(tag, str)))
    except json.JSONDecodeError:
        # If JSON parsing fails, try to extract tags using regex or basic parsing
        logger.warning(f"Failed to parse tags as JSON: {response}")
        
        # Fall back to a simple extraction method
        if "[" in response and "]" in response:
            # Extract content between brackets
            content = response[response.find("[")+1:response.find("]")]
            # Split by commas and clean up
            tags = [tag.strip().strip('"\'').lower() for tag in content.split(",")]
            return list(set(tag for tag in tags if tag))
    
    logger.warning(f"Could not extract valid tags from response: {response}")
    return []

def enrich_with_ai_explanations_and_tags(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Enrich command data with AI-generated explanations and tags.

    Args:
        limit: Optional limit on the number of commands to process

    Returns:
        List of enriched command entries
    """
    # Load the enriched command data
    if not INPUT_PATH.exists():
        logger.error(f"Input file not found: {INPUT_PATH}")
        return []

    commands = utils.load_json(INPUT_PATH)
    logger.info(f"Loaded {len(commands)} commands from {INPUT_PATH}")

    # Limit the number of commands to process if specified
    if limit and limit > 0:
        commands = commands[:limit]
        logger.info(f"Processing only the first {limit} commands")

    # Check if Ollama is available
    try:
        requests.get(f"{OLLAMA_HOST}/api/version", timeout=5)
    except requests.exceptions.RequestException:
        logger.error(f"Ollama not available at {OLLAMA_HOST}. Make sure it's running.")
        return []

    # Process each command
    enriched_commands = []
    for i, command in enumerate(commands):
        command_id = command.get('id', f"unknown-{i}")
        command_name = command.get('command', 'unknown')

        logger.info(f"Processing command {i+1}/{len(commands)}: {command_name} (ID: {command_id})")

        # Generate explanation if needed
        needs_explanation = not command.get('explanation')
        if needs_explanation:
            # Generate the explanation prompt
            explanation_prompt = generate_explanation_prompt(command)
            
            # Get the AI explanation
            explanation = utils.retry_operation(get_ai_explanation, 3, explanation_prompt)
            
            if explanation:
                # Add the explanation to the command
                command['explanation'] = explanation
                logger.info(f"Added AI explanation ({len(explanation)} chars)")
            else:
                logger.warning(f"Failed to get AI explanation for {command_name}")
        
        # Generate tags if needed
        needs_tags = not command.get('tags') or len(command.get('tags', [])) == 0
        if needs_tags:
            # Generate the tags prompt
            tags_prompt = generate_tags_prompt(command)
            
            # Get the AI tags
            tags_response = utils.retry_operation(get_ai_explanation, 3, tags_prompt)
            
            if tags_response:
                # Parse the response to extract tags
                tags = parse_tags_response(tags_response)
                
                if tags:
                    # Add the tags to the command
                    command['tags'] = tags
                    logger.info(f"Added AI tags: {tags}")
                else:
                    logger.warning(f"Failed to parse tags from response: {tags_response}")
            else:
                logger.warning(f"Failed to get AI tags for {command_name}")
        
        # Update timestamp if we modified the command
        if needs_explanation or needs_tags:
            command['updated_at'] = utils.get_timestamp()
        
        enriched_commands.append(command)

        # Save progress periodically
        if (i + 1) % 10 == 0 or i == len(commands) - 1:
            utils.save_json(enriched_commands, OUTPUT_PATH)
            logger.info(f"Saved progress ({i+1}/{len(commands)} commands processed)")

        # Be nice to the API
        time.sleep(1)

    # Final save
    utils.save_json(enriched_commands, OUTPUT_PATH)
    logger.info(f"Completed AI enrichment for {len(enriched_commands)} commands")

    # Count commands with explanations and tags
    with_explanation = sum(1 for cmd in enriched_commands if cmd.get('explanation'))
    with_tags = sum(1 for cmd in enriched_commands if cmd.get('tags') and len(cmd.get('tags', [])) > 0)
    
    logger.info(f"Commands with explanations: {with_explanation}/{len(enriched_commands)}")
    logger.info(f"Commands with tags: {with_tags}/{len(enriched_commands)}")

    return enriched_commands

def enrich_with_ai_explanations(limit: Optional[int] = None) -> List[Dict[str, Any]]:
    """
    Legacy function for backward compatibility.
    Calls the new function that handles both explanations and tags.

    Args:
        limit: Optional limit on the number of commands to process

    Returns:
        List of enriched command entries
    """
    return enrich_with_ai_explanations_and_tags(limit)

def main():
    """Run the script"""
    # Get process limit from environment variable
    process_limit = os.environ.get("PROCESS_LIMIT")
    limit = int(process_limit) if process_limit else None
    
    # Check if we should use sample data
    use_sample = os.environ.get("USE_SAMPLE", "false").lower() in ("true", "1", "yes")
    
    if use_sample:
        logger.info("Using sample data for testing")
        # Create sample data
        sample_data = create_sample_data()
        
        # Use the sample data directly
        utils.save_json(sample_data, INPUT_PATH)
        logger.info(f"Saved {len(sample_data)} sample commands to {INPUT_PATH}")
        
    # Check if input file exists
    if not INPUT_PATH.exists() and not use_sample:
        logger.error(f"Input file not found: {INPUT_PATH}")
        logger.info("Run with USE_SAMPLE=true to generate and use sample data")
        return
    
    # Run the enrichment
    logger.info(f"Starting enrichment process with model {OLLAMA_MODEL}")
    enriched_data = enrich_with_ai_explanations_and_tags(limit)
    
    if enriched_data:
        # Save the enriched data
        utils.save_json(enriched_data, OUTPUT_PATH)
        logger.info(f"Saved {len(enriched_data)} enriched commands to {OUTPUT_PATH}")
        
        # Print stats
        with_explanation = sum(1 for cmd in enriched_data if cmd.get('explanation'))
        with_tags = sum(1 for cmd in enriched_data if cmd.get('tags') and len(cmd.get('tags', [])) > 0)
        
        logger.info(f"Commands with explanations: {with_explanation}/{len(enriched_data)}")
        logger.info(f"Commands with tags: {with_tags}/{len(enriched_data)}")
    else:
        logger.warning("No enriched data was generated")

if __name__ == "__main__":
    main()