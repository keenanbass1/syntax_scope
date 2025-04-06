#!/usr/bin/env python3
"""
Validates that the syntax.json file conforms to the expected schema.
This script is useful for catching schema errors before they reach the frontend.
"""

import json
import sys
from pathlib import Path
from jsonschema import validate, ValidationError

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

# Import utility functions
from scripts.utils import load_json, get_data_path, get_public_path

def validate_syntax_json():
    """Validate the syntax.json file against the schema"""
    # Load the schema
    schema_path = Path(__file__).resolve().parent.parent / "schema" / "syntax_schema.json"
    schema = load_json(schema_path)
    
    if not schema:
        print(f"❌ Schema file not found or empty: {schema_path}")
        return False
    
    # Convert the single object schema to an array schema
    array_schema = {
        "type": "array",
        "items": schema
    }
    
    # Files to validate
    files_to_validate = [
        get_data_path("syntax.json"),
        get_public_path("syntax.json")
    ]
    
    all_valid = True
    
    for file_path in files_to_validate:
        if not file_path.exists():
            print(f"❌ File not found: {file_path}")
            all_valid = False
            continue
        
        data = load_json(file_path)
        if not data:
            print(f"❌ File is empty or invalid JSON: {file_path}")
            all_valid = False
            continue
        
        try:
            validate(instance=data, schema=array_schema)
            print(f"✅ {file_path} is valid against the schema")
        except ValidationError as e:
            print(f"❌ {file_path} validation error:")
            print(f"   Path: {'.'.join(str(x) for x in e.path)}")
            print(f"   Message: {e.message}")
            all_valid = False
    
    return all_valid

def main():
    """Main function"""
    print("\nValidating syntax.json files against schema...")
    valid = validate_syntax_json()
    
    if valid:
        print("\n✅ All files are valid")
        return True
    else:
        print("\n❌ Some files failed validation")
        return False

if __name__ == "__main__":
    main() 