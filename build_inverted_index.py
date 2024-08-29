import os
import json
from collections import defaultdict


def build_inverted_index(source_folder):
    inverted_index = defaultdict(list)

    # Iterate over all files in the folder
    for filename in os.listdir(source_folder):
        if filename.endswith(".json"):
            file_path = os.path.join(source_folder, filename)

            # Open and read the JSON file
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                document_id = data["document_id"]
                tokens = data["tokens"]

                # Build the inverted index
                for token in tokens:
                    if document_id not in inverted_index[token]:
                        inverted_index[token].append(document_id)

    return inverted_index


def save_inverted_index(inverted_index, output_file):
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(inverted_index, file, ensure_ascii=False, indent=4)


if __name__ == "__main__":
    source_folder = "tig_corpus (json)"
    output_file = "inverted_index.json"

    # Build the inverted index
    inverted_index = build_inverted_index(source_folder)

    # Save the inverted index to a file
    save_inverted_index(inverted_index, output_file)

    print(f"Inverted index saved to {output_file}")