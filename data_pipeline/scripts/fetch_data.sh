

#!/bin/bash
echo "📡 Running syntax data pipeline..."
cd data_pipeline/scripts

python3 scrape_tldr.py
python3 enrich_with_ai.py
python3 combine_all.py
python3 export_to_json.py

echo "✅ Data updated! Ready to serve."
