#!/usr/bin/env python3
"""
Main script to run the entire data pipeline in sequence.
"""

import os
import sys
import time
import argparse
from pathlib import Path

# Add the current directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent))

# Import pipeline modules
import utils
import scrape_tldr
import enrich_data
import enrich_with_ai
import combine_all
import export_to_json

logger = utils.logger

def run_pipeline(skip_ai: bool = False, limit: int = 0):
    """
    Run the entire data pipeline in sequence.

    Args:
        skip_ai: Whether to skip the AI enrichment step
        limit: Limit the number of commands to process in the AI step
    """
    start_time = time.time()
    logger.info("Starting SyntaxScope data pipeline")

    # Step 1: Scrape TLDR pages
    logger.info("\n=== Step 1: Scraping TLDR pages ===")
    try:
        commands = scrape_tldr.scrape_tldr_pages()
        logger.info(f"Scraped {len(commands)} commands from TLDR pages")
    except Exception as e:
        logger.error(f"Error in Step 1 (Scrape TLDR): {e}")
        return False

    # Step 2: Enrich data with categories and tags
    logger.info("\n=== Step 2: Enriching data with categories and tags ===")
    try:
        enriched_commands = enrich_data.enrich_data()
        logger.info(f"Enriched {len(enriched_commands)} commands")
    except Exception as e:
        logger.error(f"Error in Step 2 (Enrich Data): {e}")
        return False

    # Step 3: Enrich with AI explanations (optional)
    if not skip_ai:
        logger.info("\n=== Step 3: Enriching with AI explanations ===")
        try:
            # Set environment variable for the limit
            if limit > 0:
                os.environ["PROCESS_LIMIT"] = str(limit)
                logger.info(f"Processing only {limit} commands in AI step")

            ai_commands = enrich_with_ai.enrich_with_ai_explanations(limit)
            logger.info(f"Added AI explanations to {len(ai_commands)} commands")
        except Exception as e:
            logger.error(f"Error in Step 3 (Enrich with AI): {e}")
            logger.warning("Continuing pipeline without AI enrichment")
    else:
        logger.info("\n=== Step 3: Skipping AI enrichment ===")

    # Step 4: Combine all data sources
    logger.info("\n=== Step 4: Combining all data sources ===")
    try:
        combined_commands = combine_all.combine_data()
        logger.info(f"Combined {len(combined_commands)} commands")
    except Exception as e:
        logger.error(f"Error in Step 4 (Combine All): {e}")
        return False

    # Step 5: Export to JSON for frontend
    logger.info("\n=== Step 5: Exporting to JSON for frontend ===")
    try:
        exported_commands = export_to_json.export_to_json()
        logger.info(f"Exported {len(exported_commands)} commands to frontend")
    except Exception as e:
        logger.error(f"Error in Step 5 (Export to JSON): {e}")
        return False

    # Calculate total time
    end_time = time.time()
    total_time = end_time - start_time
    logger.info(f"\n=== Pipeline completed in {total_time:.2f} seconds ===")
    logger.info(f"Final output: {utils.PUBLIC_DATA_DIR / 'syntax.json'}")

    return True

def main():
    """Parse arguments and run the pipeline"""
    parser = argparse.ArgumentParser(description="Run the SyntaxScope data pipeline")
    parser.add_argument("--skip-ai", action="store_true", help="Skip the AI enrichment step")
    parser.add_argument("--limit", type=int, default=0, help="Limit the number of commands to process in the AI step")

    args = parser.parse_args()

    success = run_pipeline(skip_ai=args.skip_ai, limit=args.limit)

    if success:
        logger.info("Pipeline completed successfully")
        return 0
    else:
        logger.error("Pipeline failed")
        return 1

if __name__ == "__main__":
    main()