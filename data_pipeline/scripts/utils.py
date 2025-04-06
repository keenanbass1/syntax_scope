#!/usr/bin/env python3
"""
Utility functions for the SyntaxScope data pipeline.
"""

import os
import json
import logging
import hashlib
import datetime
import jsonschema
from pathlib import Path
from typing import Dict, List, Any, Optional, Union

# Path constants
ROOT_DIR = Path(__file__).parent.parent.parent
DATA_DIR = ROOT_DIR / "data_pipeline" / "data"
SCHEMA_DIR = ROOT_DIR / "data_pipeline" / "schema"
PUBLIC_DATA_DIR = ROOT_DIR / "public" / "data"
LOG_DIR = ROOT_DIR / "data_pipeline" / "logs"

# Ensure directories exist
DATA_DIR.mkdir(exist_ok=True, parents=True)
SCHEMA_DIR.mkdir(exist_ok=True, parents=True)
PUBLIC_DATA_DIR.mkdir(exist_ok=True, parents=True)
LOG_DIR.mkdir(exist_ok=True, parents=True)

# Configure logging after ensuring directories exist
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOG_DIR / "pipeline.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger("syntaxscope")

# Create subdirectories if they don't exist
(DATA_DIR / "raw").mkdir(exist_ok=True)
(DATA_DIR / "raw" / "tldr").mkdir(exist_ok=True)
(DATA_DIR / "raw" / "other_sources").mkdir(exist_ok=True)
(DATA_DIR / "processed").mkdir(exist_ok=True)
(DATA_DIR / "final").mkdir(exist_ok=True)

# Path helpers
def get_data_path(filename):
    """Get the full path to a file in the data directory"""
    return DATA_DIR / filename

def get_public_path(filename):
    """Get the full path to a file in the public data directory"""
    return PUBLIC_DATA_DIR / filename

def load_json(file_path: Union[str, Path]) -> Any:
    """
    Load JSON data from a file.

    Args:
        file_path: Path to the JSON file

    Returns:
        The loaded JSON data

    Raises:
        FileNotFoundError: If the file doesn't exist
        json.JSONDecodeError: If the file contains invalid JSON
    """
    try:
        file_path = Path(file_path)
        if not file_path.exists():
            logger.warning(f"File not found: {file_path}")
            return []
        with open(file_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"File not found: {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in {file_path}: {e}")
        return []

def save_json(data: Any, file_path: Union[str, Path], pretty: bool = True) -> bool:
    """
    Save data to a JSON file.

    Args:
        data: The data to save
        file_path: Path where to save the JSON file
        pretty: Whether to format the JSON with indentation

    Returns:
        True if successful, False otherwise
    """
    try:
        file_path = Path(file_path)
        file_path.parent.mkdir(exist_ok=True, parents=True)

        with open(file_path, 'w', encoding='utf-8') as f:
            if pretty:
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                json.dump(data, f, ensure_ascii=False)

        logger.info(f"Saved JSON to {file_path}")
        return True
    except IOError as e:
        logger.error(f"Error saving JSON to {file_path}: {e}")
        return False

def validate_against_schema(data: Any, schema_path: Union[str, Path] = None) -> bool:
    """
    Validate data against the JSON schema.

    Args:
        data: The data to validate
        schema_path: Path to the schema file (defaults to syntax_schema.json)

    Returns:
        True if valid, False otherwise
    """
    if schema_path is None:
        schema_path = SCHEMA_DIR / "syntax_schema.json"

    try:
        schema = load_json(schema_path)
        jsonschema.validate(instance=data, schema=schema)
        logger.info("Data validation successful")
        return True
    except jsonschema.exceptions.ValidationError as e:
        logger.error(f"Schema validation error: {e}")
        return False
    except Exception as e:
        logger.error(f"Error during schema validation: {e}")
        return False

def generate_id(text: str) -> str:
    """
    Generate a unique ID based on the text.

    Args:
        text: Text to generate ID from

    Returns:
        A unique ID string
    """
    return hashlib.md5(text.encode('utf-8')).hexdigest()[:12]

def get_timestamp() -> str:
    """
    Get the current timestamp in ISO format.

    Returns:
        Current timestamp string
    """
    return datetime.datetime.now().isoformat()

def retry_operation(func, max_retries: int = 3, *args, **kwargs):
    """
    Retry an operation multiple times before giving up.

    Args:
        func: The function to retry
        max_retries: Maximum number of retry attempts
        *args, **kwargs: Arguments to pass to the function

    Returns:
        The result of the function call

    Raises:
        Exception: The last exception raised by the function
    """
    last_exception = None
    for attempt in range(max_retries):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed: {e}")
            if attempt + 1 < max_retries:
                logger.info(f"Retrying...")

    logger.error(f"All {max_retries} attempts failed")
    if last_exception:
        raise last_exception

def merge_data(data_list: List[Dict]) -> List[Dict]:
    """
    Merge multiple data sources, avoiding duplicates.

    Args:
        data_list: List of data dictionaries to merge

    Returns:
        Merged list of dictionaries
    """
    merged = {}

    for data in data_list:
        for item in data:
            # Use command as key for deduplication
            key = item.get('command', '')
            if key:
                if key not in merged:
                    merged[key] = item
                else:
                    # Merge fields from both entries
                    for field, value in item.items():
                        if field not in merged[key] or not merged[key][field]:
                            merged[key][field] = value

    return list(merged.values())

def categorize_command(command: str) -> str:
    """
    Determine the likely category (shell) for a command.

    Args:
        command: The command string

    Returns:
        Category name (bash, powershell, etc.)
    """
    command = command.lower()

    # PowerShell indicators
    if any(indicator in command for indicator in [
        'get-', 'set-', 'new-', 'remove-', '-object', '-property',
        '$_', '$null', '$true', '$false'
    ]):
        return 'powershell'

    # Python indicators
    if any(indicator in command for indicator in [
        'import ', 'def ', 'class ', 'print(', '.py', 'python'
    ]):
        return 'python'

    # Zsh-specific indicators
    if any(indicator in command for indicator in [
        'zsh', 'setopt', 'zstyle'
    ]):
        return 'zsh'

    # Default to bash for most Unix commands
    return 'bash'

def extract_tags_from_command(command: str, description: str) -> List[str]:
    """
    Extract relevant tags from a command and its description.

    Args:
        command: The command string
        description: The command description

    Returns:
        List of tags
    """
    tags = set()

    # Common operations
    operations = {
        'list': ['ls', 'dir', 'find', 'get-', 'list'],
        'search': ['grep', 'find', 'select-string', 'where-object', 'findstr'],
        'file': ['file', 'touch', 'mkdir', 'rm', 'cp', 'mv', 'cat', 'more', 'less'],
        'network': ['curl', 'wget', 'netstat', 'ping', 'ssh', 'nc', 'nslookup'],
        'process': ['ps', 'kill', 'top', 'get-process', 'stop-process'],
        'user': ['user', 'chmod', 'chown', 'sudo', 'su'],
        'package': ['apt', 'yum', 'brew', 'npm', 'pip', 'gem', 'install'],
        'git': ['git'],
        'docker': ['docker'],
        'archive': ['tar', 'zip', 'unzip', 'gzip', 'gunzip'],
    }

    # Add operation tags
    for tag, keywords in operations.items():
        if any(keyword in command.lower() for keyword in keywords):
            tags.add(tag)

    # Add shell-specific tags
    category = categorize_command(command)
    tags.add(category)

    # Extract additional tags from description
    description_words = description.lower().split()
    common_terms = ['file', 'directory', 'process', 'network', 'user', 'system',
                   'search', 'find', 'list', 'create', 'delete', 'remove', 'install']

    for term in common_terms:
        if term in description_words:
            tags.add(term)

    return list(tags)

# Stats functions
def print_stats(title, items, key_fn=None):
    """Print statistics about the items"""
    if not items:
        logger.info(f"{title}: 0 items")
        return

    logger.info(f"{title}: {len(items)} items")

    if key_fn:
        counts = {}
        for item in items:
            key = key_fn(item)
            counts[key] = counts.get(key, 0) + 1

        for key, count in sorted(counts.items(), key=lambda x: x[1], reverse=True):
            logger.info(f"  - {key}: {count}")