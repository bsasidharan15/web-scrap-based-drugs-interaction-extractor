# 🚀 Web Scraping-Based Drug Interaction Extractor 💊

A Python-based tool for extracting drug interaction data from Drugs.com using web scraping. This tool supports multiprocessing for efficient batch processing and includes checkpointing to resume interrupted tasks.

## 🌟 Features

- 🕸️ **Web Scraping**: Extracts drug interaction data from Drugs.com.
- 🔄 **Checkpointing**: Saves progress to allow resuming from the last processed point.
- 🚀 **Multiprocessing**: Utilizes CPU cores for faster processing.
- 📦 **CSV Input/Output**: Easy handling of large datasets.
- 🧩 **Modular Design**: Well-structured functions for extensibility.

## 📥 Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/drug-interaction-extractor.git
   cd drug-interaction-extractor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## ⚡ Usage

### 📑 Input Data Format

The input CSV file should contain the following columns:

| 🆔 Unique ID | 💊 Drug Name | 🏷️ Drug ID |
|-------------|-------------|-----------|
| 1           | Drug A      | 1234      |
| 2           | Drug B      | 5678      |
| ...         | ...         | ...       |

### ▶️ Running the Script

Execute the main script:
```bash
python main.py
```

The script will:
- 📥 Read drug data from the input CSV file.
- 🔄 Process all possible drug pairs.
- 📤 Save interaction data in an output CSV file.
- 📌 Maintain a checkpoint file to track processed pairs.

### ⚙️ Customizing File Paths

Modify `main.py` to set custom file paths for:
- 📂 `input_csv`: Input drug data file.
- 📂 `output_csv`: Output file storing interactions.
- 📂 `checkpoint_csv`: Checkpoint file for tracking progress.

## 🛠️ Code Breakdown

### 1️⃣ Load and Save Processed Pairs

- **`load_processed_pairs(checkpoint_csv)`** 📝
  - Reads previously processed drug pairs from the checkpoint file.
  - Ensures that already processed pairs are skipped.

- **`save_processed_pairs(processed_pairs, checkpoint_csv)`** 💾
  - Writes updated processed pairs to the checkpoint file.

### 2️⃣ Extract Drug Interactions

- **`extract_interactions(drug1, drug2)`** 🔬
  - Scrapes interaction data from Drugs.com.
  - Parses the severity level (`Major`, `Moderate`, `Minor`).
  - ❌ Ignores food interactions.
  - ✅ Returns interaction details if found.

### 3️⃣ Process Drug Pairs

- **`process_drug_pair(pair, output_csv, processed_pairs, checkpoint_csv)`** 🔄
  - Checks if a drug pair was already processed.
  - Calls `extract_interactions()` to retrieve data.
  - 📤 Writes results to the output CSV if interactions exist.
  - ✅ Updates the checkpoint file.

### 4️⃣ Multiprocessing Execution

- **`create_interactions_csv(input_csv, output_csv, checkpoint_csv)`** ⚡
  - 📥 Loads drug data from CSV.
  - 🔄 Generates all possible drug combinations.
  - 🚀 Uses multiprocessing to process pairs efficiently.
  - 📌 Saves progress to a checkpoint file.

## 🔍 Example

### 🧐 Extracting Interactions for a Pair of Drugs

```python
from scraper import extract_interactions

drug1 = {"drug_name": "Drug A", "drug_id": "1234", "unique_id": "1"}
drug2 = {"drug_name": "Drug B", "drug_id": "5678", "unique_id": "2"}

interaction_data = extract_interactions(drug1, drug2)
print(interaction_data)
```

### 📊 Batch Processing All Drug Pairs

```python
from main import create_interactions_csv

input_csv = "input.csv"
output_csv = "output.csv"
checkpoint_csv = "checkpoint.csv"

create_interactions_csv(input_csv, output_csv, checkpoint_csv)
```

## 🤝 Contributing

1. 🍴 Fork the repository.
2. 🌱 Create a new branch (`git checkout -b feature/YourFeature`).
3. 📝 Commit your changes (`git commit -m 'Add new feature'`).
4. 📤 Push to the branch (`git push origin feature/YourFeature`).
5. 🔄 Open a pull request.

## 📜 License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🎉 Thanks to [Drugs.com](https://www.drugs.com) for providing drug interaction data.
- 🐍 Built with Python, `requests`, and `lxml`.
