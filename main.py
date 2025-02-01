import requests
import csv
from lxml import html
import itertools
from multiprocessing import Pool, cpu_count, Manager
import os
from functools import partial

# Function to load processed pairs from the checkpoint CSV
def load_processed_pairs(checkpoint_csv):
    if not os.path.exists(checkpoint_csv):
        return []
    processed_pairs = []
    with open(checkpoint_csv, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if len(row) == 2:
                processed_pairs.append(tuple(sorted(row)))
    return processed_pairs

# Function to save processed pairs to the checkpoint CSV
def save_processed_pairs(processed_pairs, checkpoint_csv):
    with open(checkpoint_csv, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerows(processed_pairs)

# Function to extract interaction data
def extract_interactions(drug1, drug2):
    base_url = "https://www.drugs.com/interactions-check.php?drug_list="
    interaction_url = base_url + f"{drug1['drug_id']},{drug2['drug_id']}"

    try:
        response = requests.get(interaction_url)
        response.raise_for_status()
        tree = html.fromstring(response.content)
        interaction_wrappers = tree.xpath('//div[@class="interactions-reference-wrapper"]')

        if not interaction_wrappers:
            return None

        interaction_level_text = "Unknown"
        drugs_involved_text = ""

        for wrapper in interaction_wrappers:
            header = wrapper.xpath('.//div[@class="interactions-reference-header"]')
            if not header:
                continue

            header = header[0]
            major = header.xpath('.//span[@class="ddc-status-label status-category-major"]/text()')
            moderate = header.xpath('.//span[@class="ddc-status-label status-category-moderate"]/text()')
            minor = header.xpath('.//span[@class="ddc-status-label status-category-minor"]/text()')

            if major:
                interaction_level_text = "Major"
            elif moderate:
                interaction_level_text = "Moderate"
            elif minor:
                interaction_level_text = "Minor"

            drugs_involved = header.xpath('.//h3/text()')
            drugs_involved_text = ''.join(drugs_involved).strip() if drugs_involved else ""

            if "food" in drugs_involved_text.lower() or "Nonsteroidal anti-inflammatories" in drugs_involved_text:
                return None

            description = wrapper.xpath('.//p[1]/text()')
            description_text = ''.join(description).strip() if description else "No description available."

            return {
                'interaction_level': interaction_level_text,
                'drugs_involved': drugs_involved_text,
                'description': description_text
            }
    except requests.exceptions.RequestException:
        return None

# Worker function to process one drug pair
def process_drug_pair(pair, output_csv, processed_pairs, checkpoint_csv):
    drug1, drug2 = pair
    current_pair = tuple(sorted([drug1['unique_id'], drug2['unique_id']]))
    
    if current_pair in processed_pairs:
        print(f"Skipping pair: {drug1['drug_name']} and {drug2['drug_name']} (already processed)")
        return

    interaction_data = extract_interactions(drug1, drug2)
    
    if interaction_data:
        with open(output_csv, mode='a', newline='') as out_file:
            writer = csv.DictWriter(out_file, fieldnames=[
                'Drug 1 Name', 'Drug 1 Unique ID', 'Drug 2 Name', 'Drug 2 Unique ID', 
                'Interaction Level', 'Interaction'
            ])
            writer.writerow({
                'Drug 1 Name': drug1['drug_name'],
                'Drug 1 Unique ID': drug1['unique_id'],
                'Drug 2 Name': drug2['drug_name'],
                'Drug 2 Unique ID': drug2['unique_id'],
                'Interaction Level': interaction_data['interaction_level'],
                'Interaction': interaction_data['description']
            })
    
    processed_pairs.append(current_pair)
    save_processed_pairs(processed_pairs, checkpoint_csv)

# Main function to create the interactions CSV
def create_interactions_csv(input_csv, output_csv, checkpoint_csv):
    processed_pairs = load_processed_pairs(checkpoint_csv)
    manager = Manager()
    processed_pairs = manager.list(processed_pairs)

    drugs = []
    with open(input_csv, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            drugs.append({
                'unique_id': row['Unique ID'],
                'drug_name': row['Drug Name'],
                'drug_id': row['Drug ID']
            })

    if not os.path.exists(output_csv):
        with open(output_csv, mode='w', newline='') as out_file:
            fieldnames = ['Drug 1 Name', 'Drug 1 Unique ID', 'Drug 2 Name', 'Drug 2 Unique ID', 
                          'Interaction Level', 'Interaction']
            writer = csv.DictWriter(out_file, fieldnames=fieldnames)
            writer.writeheader()

    drug_pairs = itertools.combinations(drugs, 2)
    pool = Pool(cpu_count())
    process_with_output = partial(process_drug_pair, output_csv=output_csv, processed_pairs=processed_pairs, checkpoint_csv=checkpoint_csv)

    try:
        pool.map(process_with_output, drug_pairs)
    except Exception as e:
        print(e)
    finally:
        pool.close()
        pool.join()

    save_processed_pairs(processed_pairs, checkpoint_csv)
    print(f"Interaction data has been written to output CSV")

if __name__ == "__main__":
    input_csv = "input.csv"
    output_csv = "output.csv"
    checkpoint_csv = "checkpoint.csv"
    create_interactions_csv(input_csv, output_csv, checkpoint_csv)
