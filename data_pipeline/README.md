# SyntaxScope Data Pipeline

This directory contains the data pipeline for the SyntaxScope command syntax search engine. The pipeline scrapes command syntax data from various sources, enriches it with metadata, and exports it for use by the frontend.

## Directory Structure

- `scripts/`: Python scripts for the data pipeline
- `data/`: Data files produced by the pipeline
  - `raw/`: Raw data scraped from sources
  - `processed/`: Processed and enriched data
  - `final/`: Final data ready for the frontend
- `schema/`: JSON schema definitions

## Pipeline Steps

1. **Scrape TLDR Pages**: Fetch command syntax from the TLDR pages GitHub repository
2. **Enrich Data**: Add categories and tags to commands
3. **Enrich with AI**: Use Ollama to add AI-generated explanations for commands
4. **Combine All**: Merge data from different sources
5. **Export to JSON**: Prepare data for the frontend

## Running the Pipeline

To run the entire pipeline:

```bash
cd data_pipeline/scripts
python run_pipeline.py
```

### Command-line Options

- `--skip-ai`: Skip the AI enrichment step
- `--limit N`: Limit the number of commands to process in the AI step

Example:

```bash
python run_pipeline.py --skip-ai  # Skip AI enrichment
python run_pipeline.py --limit 10  # Process only 10 commands in the AI step
```

## Individual Scripts

You can also run individual scripts:

```bash
python scrape_tldr.py       # Scrape TLDR pages
python enrich_data.py       # Enrich with categories and tags
python enrich_with_ai.py    # Add AI explanations
python combine_all.py       # Combine data sources
python export_to_json.py    # Export for frontend
```

## AI Enrichment

The AI enrichment step uses Ollama to generate detailed explanations for commands. To use this feature:

1. Install Ollama: https://ollama.ai/
2. Run Ollama server: `ollama serve`
3. Pull a model: `ollama pull llama3` (or another model)

You can configure the AI enrichment by setting environment variables:

```bash
export OLLAMA_HOST="http://localhost:11434"  # Ollama API host
export OLLAMA_MODEL="llama3"                 # Model to use
export OLLAMA_TIMEOUT="30"                   # Timeout in seconds
export PROCESS_LIMIT="10"                    # Limit number of commands to process
```

## Required Dependencies

- Python 3.6+
- Required packages:
  - `jsonschema`: For schema validation
  - `requests`: For API calls

Install with:

```bash
pip install jsonschema requests
```

## Data Format

The final data format follows the schema defined in `schema/syntax_schema.json`. Each command entry includes:

- `id`: Unique identifier
- `command`: The command syntax
- `description`: Brief description of what the command does
- `category`: Primary shell or language (bash, powershell, zsh, python, etc.)
- `tags`: Array of tags for categorizing and searching
- `explanation`: AI-generated detailed explanation
- `examples`: Array of example usages with code and descriptions
- `source`: Information about where the command data came from
- `created_at`: Timestamp when the entry was created
- `updated_at`: Timestamp when the entry was last updated

## Output Files

The final output is written to:
- `data_pipeline/data/final/syntax.json`: Pipeline output copy
- `public/data/syntax.json`: Frontend-accessible copy

## Adding New Data Sources

To add a new data source:

1. Create a new script in the `scripts/` directory to scrape/process the source
2. Update the `combine_all.py` script to include the new data source
3. Run the pipeline to incorporate the new data

## Troubleshooting

- **Missing AI explanations**: Make sure Ollama is running and the model is available
- **Schema validation errors**: Check that your data conforms to the schema
- **Git repository errors**: Ensure you have git installed and can access GitHub

## License

This data pipeline is licensed under the MIT License. The data sources may have their own licenses - see the `source` field in each entry for specific license information.