🧪 Web Scraping-Based Drug Interaction Extractor 💊
A Python-based tool for extracting drug interaction data from Drugs.com using web scraping. This tool supports multiprocessing for efficient batch processing and includes checkpointing to resume interrupted tasks.

Features
🕸️ Web scraping for drug interaction data

🔄 Checkpointing to resume interrupted tasks

🚀 Multiprocessing for efficient batch processing

📦 CSV input/output for easy data handling

🧩 Modular and extensible codebase

Project Structure
Copy
drug-interaction-extractor/
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── scraper.py
│   ├── utils.py
│   └── main.py
├── data/
│   ├── input/
│   │   └── updated_drug_data.csv
│   ├── output/
│   │   ├── drug_interactions.csv
│   │   └── selected_drug_ids.csv
│   └── logs/
│       └── scraper.log
├── config/
│   └── .env.example
└── tests/
    ├── __init__.py
    ├── test_scraper.py
    └── test_utils.py
Installation
Clone the repository:

bash
Copy
git clone https://github.com/yourusername/drug-interaction-extractor.git
cd drug-interaction-extractor
Install dependencies:

bash
Copy
pip install -r requirements.txt
Set up environment variables:

Copy the .env.example file to .env:

bash
Copy
cp config/.env.example .env
Update the .env file with any required credentials or configurations.

Usage
Input Data Format
Ensure your input CSV file (updated_drug_data.csv) is in the following format:

Drug Name	Drug ID
5-hydroxytryptophan/melatonin/pyridoxine	4479-0
A-Methapred	1607-1956
A-Phedrin	1966-7245
ACT Fluoride Rinse	1110-10594
Running the Script
Navigate to the src directory:

bash
Copy
cd src
Run the main script:

bash
Copy
python main.py
By default, the script will:

Read drug data from data/input/updated_drug_data.csv.

Write interaction data to data/output/drug_interactions.csv.

Save checkpoint data to data/output/selected_drug_ids.csv.

(Optional) Customize file paths:
You can modify the file paths in main.py to use custom input/output locations.

Configuration
Environment Variables
Create a .env file in the config directory with the following variables (if needed):

Copy
# Example environment variables
LOG_LEVEL=INFO
REQUEST_TIMEOUT=10
MAX_RETRIES=3
Logging
Logs are saved to data/logs/scraper.log. You can adjust the logging level in the .env file.

API Reference
extract_interactions(drug1, drug2)
Extracts interaction data for a pair of drugs.

Parameters
drug1: A dictionary containing drug_name, drug_id, and unique_id for the first drug.

drug2: A dictionary containing drug_name, drug_id, and unique_id for the second drug.

Returns
A dictionary containing:

interaction_level: The severity of the interaction (Major, Moderate, Minor, or Unknown).

drugs_involved: The names of the drugs involved.

description: A description of the interaction.

process_drug_pair(pair, output_csv, processed_pairs, checkpoint_csv)
Processes a single drug pair and writes the interaction data to the output CSV.

Parameters
pair: A tuple containing two drug dictionaries.

output_csv: The path to the output CSV file.

processed_pairs: A list of already processed drug pairs.

checkpoint_csv: The path to the checkpoint CSV file.

create_interactions_csv(input_csv, output_csv, checkpoint_csv)
Main function to create the interactions CSV.

Parameters
input_csv: The path to the input CSV file containing drug data.

output_csv: The path to the output CSV file for interaction data.

checkpoint_csv: The path to the checkpoint CSV file.

Examples
Analyzing Drug Interactions
python
Copy
from src.scraper import extract_interactions

drug1 = {
    "drug_name": "A-Methapred",
    "drug_id": "1607-1956",
    "unique_id": "1"
}

drug2 = {
    "drug_name": "A-Phedrin",
    "drug_id": "1966-7245",
    "unique_id": "2"
}

interaction_data = extract_interactions(drug1, drug2)
print(interaction_data)
Batch Processing
python
Copy
from src.main import create_interactions_csv

input_csv = "data/input/updated_drug_data.csv"
output_csv = "data/output/drug_interactions.csv"
checkpoint_csv = "data/output/selected_drug_ids.csv"

create_interactions_csv(input_csv, output_csv, checkpoint_csv)
Contributing
Fork the repository.

Create a new branch (git checkout -b feature/YourFeature).

Commit your changes (git commit -m 'Add some feature').

Push to the branch (git push origin feature/YourFeature).

Open a pull request.

License
This project is licensed under the Apache 2.0 License. See the LICENSE file for details.

Author
Sasidharan B

Acknowledgments
Thanks to Drugs.com for providing drug interaction data.

Built with Python, requests, and lxml.
