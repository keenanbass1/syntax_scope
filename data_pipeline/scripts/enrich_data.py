#!/usr/bin/env python3
"""
Script to enrich command data with categories and tags.
"""

import re
from collections import Counter
import utils

logger = utils.logger

# Setup paths
INPUT_FILE = utils.DATA_DIR / "raw" / "tldr" / "tldr_commands.json"
OUTPUT_FILE = utils.DATA_DIR / "processed" / "enriched_commands.json"

# Ensure output directory exists
OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

# Define categories with their regex patterns
CATEGORY_PATTERNS = {
    "file-management": [
        r"\bcp\b", r"\bmv\b", r"\brm\b", r"\bls\b", r"\bfind\b", r"\bgrep\b",
        r"\bchmod\b", r"\bchown\b", r"\btouch\b", r"\bmkdir\b", r"\brmdir\b",
        r"file", r"directory", r"folder", r"path",
    ],
    "system-admin": [
        r"\bsystemctl\b", r"\bservice\b", r"\bchroot\b", r"\bdmesg\b",
        r"\bsudo\b", r"\bsu\b", r"\bcrontab\b", r"\bapt\b", r"\bpacman\b",
        r"\byum\b", r"\bdnf\b", r"\bbrew\b", r"install", r"update", r"system"
    ],
    "network": [
        r"\bcurl\b", r"\bwget\b", r"\bping\b", r"\bssh\b", r"\bscp\b",
        r"\brsync\b", r"\btelnet\b", r"\bnetstat\b", r"\bifconfig\b",
        r"\bcertbot\b", r"\bnslookup\b", r"\bdig\b", r"network", r"http"
    ],
    "development": [
        r"\bgit\b", r"\bnpm\b", r"\bpip\b", r"\bcargo\b", r"\bmake\b",
        r"\bpython\b", r"\bnode\b", r"\bgcc\b", r"\bclang\b", r"\bjava\b",
        r"compile", r"build", r"code"
    ],
    "database": [
        r"\bmysql\b", r"\bpsql\b", r"\bmongo\b", r"\bredis\b", r"\bsqlite\b",
        r"database", r"query", r"sql"
    ],
    "text-processing": [
        r"\bcat\b", r"\bgrep\b", r"\bsed\b", r"\bawk\b", r"\bcut\b",
        r"\bsort\b", r"\buniq\b", r"\bwc\b", r"\btr\b", r"\btail\b", r"\bhead\b",
        r"text", r"string", r"replace"
    ],
    "monitoring": [
        r"\btop\b", r"\bhtop\b", r"\bps\b", r"\bfree\b", r"\bdf\b",
        r"\bdu\b", r"\blsof\b", r"monitor", r"stats", r"usage", r"process"
    ],
    "containers": [
        r"\bdocker\b", r"\bpodman\b", r"\bkubectl\b", r"\bhelm\b",
        r"container", r"image", r"kubernetes", r"k8s"
    ],
    "security": [
        r"\bopenssl\b", r"\bssh-keygen\b", r"\bgpg\b", r"\bcertbot\b",
        r"\bfirewall\b", r"\bufw\b", r"\biptables\b", r"security",
        r"encrypt", r"password", r"firewall"
    ],
    "shell": [
        r"\balias\b", r"\becho\b", r"\benv\b", r"\bexport\b", r"\bset\b",
        r"\bshopt\b", r"\bbash\b", r"\bzsh\b", r"\bsh\b", r"variable",
        r"environment", r"shell"
    ],
}

# Tag extraction patterns
TAG_PATTERNS = {
    "file": [r"file", r"files", r"folder", r"directory", r"path"],
    "search": [r"search", r"find", r"locate", r"grep"],
    "network": [r"network", r"http", r"url", r"web", r"ping", r"connect"],
    "install": [r"install", r"update", r"upgrade", r"package"],
    "git": [r"git", r"commit", r"branch", r"merge", r"repository"],
    "docker": [r"docker", r"container", r"image", r"volume"],
    "user": [r"user", r"permission", r"group", r"access"],
    "process": [r"process", r"kill", r"job", r"background"],
    "archive": [r"compress", r"extract", r"zip", r"tar", r"archive"],
    "text": [r"text", r"string", r"pattern", r"replace", r"format"],
}

def assign_category(item):
    """Assign a category to an item based on its command and description"""
    cmd = item.get("command", "").lower()
    desc = item.get("description", "").lower()
    text = f"{cmd} {desc}"

    scores = Counter()

    for category, patterns in CATEGORY_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                scores[category] += 1

    # Return the category with the highest score, or a default
    if scores:
        return scores.most_common(1)[0][0]
    return "other"

def extract_tags(item):
    """Extract relevant tags from the item's command and description"""
    cmd = item.get("command", "").lower()
    desc = item.get("description", "").lower()
    title = item.get("title", "").lower()
    text = f"{title} {cmd} {desc}"

    tags = set()

    # Add the command as a tag if it's a simple command
    if " " not in cmd and len(cmd) > 1:
        binary_name = cmd.split()[0].split("/")[-1]
        tags.add(binary_name)

    # Add language as a tag
    if "language" in item:
        tags.add(item["language"])

    # Add matches from patterns
    for tag, patterns in TAG_PATTERNS.items():
        for pattern in patterns:
            if re.search(pattern, text, re.IGNORECASE):
                tags.add(tag)
                break

    # Add category as a tag
    if "category" in item:
        tags.add(item["category"])

    # Limit to 5 most relevant tags
    return sorted(list(tags))[:5]

def enrich_item(item):
    """Add additional metadata to an item"""
    enriched = item.copy()

    # Ensure we have the basic fields
    for field in ["command", "description", "category"]:
        if field not in enriched:
            enriched[field] = ""

    # Add category
    enriched["category"] = assign_category(item)

    # Add tags
    enriched["tags"] = extract_tags(enriched)

    # Generate a unique ID if not present
    if "id" not in enriched:
        # Use command and category to create a unique, deterministic ID
        key = f"{enriched['command']}-{enriched['category']}"
        enriched["id"] = utils.generate_id(key)

    # Add timestamps if missing
    if not enriched.get('created_at'):
        enriched['created_at'] = utils.get_timestamp()

    enriched['updated_at'] = utils.get_timestamp()

    return enriched

def enrich_data():
    """Main function to enrich the scraped data"""
    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return []

    try:
        data = utils.load_json(INPUT_FILE)
    except Exception as e:
        logger.error(f"Error loading input file: {e}")
        return []

    logger.info(f"Enriching {len(data)} items...")

    # Enrich all items
    enriched_data = [enrich_item(item) for item in data]

    # Save the enriched data
    utils.save_json(enriched_data, OUTPUT_FILE)

    # Print statistics
    categories = Counter()
    for item in enriched_data:
        categories[item.get("category", "unknown")] += 1

    logger.info(f"✅ Enriched {len(enriched_data)} items")
    logger.info(f"Output written to {OUTPUT_FILE}")

    logger.info("\nCategory breakdown:")
    for category, count in categories.most_common():
        logger.info(f"  - {category}: {count} items")

    return enriched_data

def main():
    """Run the script"""
    enrich_data()

if __name__ == "__main__":
    main()