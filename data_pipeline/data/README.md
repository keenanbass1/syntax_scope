# SyntaxScope Data Files

This directory contains the data files used by the SyntaxScope command syntax search engine.

## File Structure

- `raw/`: Contains raw data scraped from various sources
  - `tldr/`: Data from the TLDR pages GitHub repository
  - `other_sources/`: Data from other sources (if applicable)
- `processed/`: Contains processed and enriched data
  - `enriched_commands.json`: Commands with added categories and tags
  - `ai_explanations.json`: AI-generated explanations for commands
  - `combined_data.json`: Merged data from all sources
- `final/`: Contains the final data ready for the frontend
  - `syntax.json`: The main data file used by the frontend

## Data Format

The data follows the schema defined in `../schema/syntax_schema.json`. Each command entry includes:

- `id`: Unique identifier
- `command`: The command syntax
- `description`: Brief description of what the command does
- `category`: Primary shell or language (bash, powershell, zsh, python, etc.)
- `tags`: Array of tags for categorizing and searching
- `explanation`: AI-generated detailed explanation (if available)
- `examples`: Array of example usages with code and descriptions
- `source`: Information about where the command data came from
- `created_at`: Timestamp when the entry was created
- `updated_at`: Timestamp when the entry was last updated

## Data Sources

- [TLDR Pages](https://github.com/tldr-pages/tldr): A community-driven collection of simplified man pages
- AI-generated explanations: Created using Ollama with appropriate models

## License

The data in this directory is subject to the licenses of the original sources. See the `source` field in each entry for specific license information.