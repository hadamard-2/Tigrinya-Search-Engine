from backend.preprocessing import TigMorphPreprocess
import os
import json
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(
    filename="json_conversion2.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)

# Define the source and target directories
source_folder = "tig_corpus (txt)"
target_folder = "tig_corpus (json)"
documents_folder = "tig_corpus (pdf)"

# Ensure target folder exists
os.makedirs(target_folder, exist_ok=True)


# Function to extract document_id from file name
def extract_document_id(file_name):
    base_name = Path(file_name).stem  # Remove extension
    parts = base_name.split("_")
    return parts[-1]  # Return the last part as the document_id


# Process each file in the source folder
for file_name in os.listdir(source_folder):
    if file_name.endswith(".txt"):
        # Construct full file path
        file_path = os.path.join(source_folder, file_name)

        # Load the text file
        with open(file_path, "r", encoding="utf-8") as file:
            text = file.read().replace("\n", " ")

        # Preprocess the text
        psr = TigMorphPreprocess(text)
        psr.tokenize().normalize().remove_stopwords().stem()
        tokens = psr.get_result()

        # Prepare JSON data
        document_id = extract_document_id(file_name)
        document_location = os.path.join(
            documents_folder, file_name.replace(".txt", ".pdf")
        )

        json_data = {
            "document_id": document_id,
            "document_location": document_location,
            "tokens": tokens,
        }

        # Save JSON data
        json_file_name = file_name.replace(".txt", ".json")
        json_file_path = os.path.join(target_folder, json_file_name)

        with open(json_file_path, "w", encoding="utf-8") as json_file:
            json.dump(json_data, json_file, ensure_ascii=False, indent=4)

        logging.info(f"Processed and saved file: {file_name} as {json_file_name}")

print("Preprocessing and saving completed.")
