#!/usr/bin/env python3
"""
Script to fetch command syntax from TLDR pages GitHub repository.
"""

import re
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import utils

logger = utils.logger

# Setup paths
OUTPUT_FILE = utils.DATA_DIR / "raw" / "tldr" / "tldr_commands.json"
CLONE_DIR = utils.DATA_DIR / "raw" / "tldr" / "repo"

def clone_tldr_repo():
    """Clone or update the TLDR pages repository"""
    if CLONE_DIR.exists():
        logger.info("Updating existing TLDR repository...")
        try:
            subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=CLONE_DIR,
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to update repository: {e}")
            return False
    else:
        logger.info("Cloning TLDR repository...")
        try:
            CLONE_DIR.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", "--depth=1", "https://github.com/tldr-pages/tldr.git", str(CLONE_DIR)],
                check=True,
                capture_output=True
            )
            return True
        except subprocess.CalledProcessError as e:
            logger.error(f"Failed to clone repository: {e}")
            return False

def parse_md_file(file_path):
    """Parse a TLDR markdown file and extract command information"""
    try:
        content = file_path.read_text(encoding="utf-8")

        # Extract the title (first line after # )
        title_match = re.search(r"^# (.*?)$", content, re.MULTILINE)
        if not title_match:
            return None
        title = title_match.group(1).strip()

        # Extract the description (line after the title)
        desc_match = re.search(r"^# .*?\n> (.*?)(?:\n>|\n\n)", content, re.DOTALL)
        description = desc_match.group(1).strip() if desc_match else ""

        # Replace multiple spaces/newlines in description
        description = re.sub(r"\s+", " ", description)

        # Extract all command examples
        commands = []
        examples = re.findall(r"- (.*?):\n\n`(.*?)`", content, re.DOTALL)

        for example_desc, cmd in examples:
            example_desc = re.sub(r"\s+", " ", example_desc.strip())
            commands.append({
                "code": cmd.strip(),
                "description": example_desc
            })

        # Determine the language based on the directory structure
        parts = file_path.parts
        language = "unknown"
        for idx, part in enumerate(parts):
            if part == "pages":
                if idx + 1 < len(parts):
                    language = parts[idx + 1]
                break

        # Map common language directories to more specific shells
        language_map = {
            "common": "bash",
            "linux": "bash",
            "osx": "bash",
            "windows": "powershell",
            "sunos": "bash",
            "android": "bash",
        }

        language = language_map.get(language, language)

        # Create a single entry with all examples
        command_name = file_path.stem

        result = {
            "id": utils.generate_id(f"{language}:{command_name}"),
            "command": command_name,
            "description": description if description else title,
            "category": utils.categorize_command(command_name),
            "tags": utils.extract_tags_from_command(command_name, description),
            "examples": commands,
            "source": {
                "name": "tldr-pages",
                "url": f"https://github.com/tldr-pages/tldr/blob/main/pages/{language}/{command_name}.md",
                "license": "MIT"
            },
            "created_at": utils.get_timestamp(),
            "updated_at": utils.get_timestamp()
        }

        return result

    except Exception as e:
        logger.error(f"Error parsing {file_path}: {e}")
        return None

def scrape_tldr_pages():
    """Main function to scrape TLDR pages"""
    if not clone_tldr_repo():
        logger.error("Failed to clone/update TLDR repository. Exiting.")
        return []

    pages_dir = CLONE_DIR / "pages"
    if not pages_dir.exists():
        logger.error(f"Pages directory not found at {pages_dir}")
        return []

    # Find all markdown files
    md_files = list(pages_dir.glob("**/*.md"))
    logger.info(f"Found {len(md_files)} markdown files")

    # Parse all files in parallel
    all_commands = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(parse_md_file, file): file for file in md_files}

        for future in as_completed(futures):
            file = futures[future]
            try:
                result = future.result()
                if result:
                    all_commands.append(result)
            except Exception as e:
                logger.error(f"Error processing {file}: {e}")

    # Write the combined results to JSON
    utils.save_json(all_commands, OUTPUT_FILE)

    # Print statistics
    categories = {}
    for cmd in all_commands:
        category = cmd.get("category", "unknown")
        categories[category] = categories.get(category, 0) + 1

    logger.info(f"✅ Scraped {len(all_commands)} commands from TLDR pages")
    logger.info(f"Output written to {OUTPUT_FILE}")

    logger.info("\nCategory breakdown:")
    for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        logger.info(f"  - {category}: {count} commands")

    return all_commands

def main():
    """Run the script"""
    scrape_tldr_pages()

if __name__ == "__main__":
    main()
