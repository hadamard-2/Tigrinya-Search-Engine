import os
import json
import math
import csv
from collections import defaultdict, Counter


def compute_tf(tokens):
    term_count = Counter(tokens)
    total_terms = len(tokens)
    tf = {term: count / total_terms for term, count in term_count.items()}
    return tf


def compute_idf(documents):
    N = len(documents)
    idf = defaultdict(lambda: 0)

    for tokens in documents.values():
        unique_terms = set(tokens)
        for term in unique_terms:
            idf[term] += 1

    idf = {term: math.log(N / count) for term, count in idf.items()}
    return idf


def compute_tf_idf(tf, idf):
    tf_idf = {term: tf_val * idf[term] for term, tf_val in tf.items()}
    return tf_idf


def build_tf_idf_matrix(folder_path):
    documents = {}
    tf_matrix = {}

    # Read documents and compute TF for each
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            file_path = os.path.join(folder_path, filename)
            with open(file_path, "r", encoding="utf-8") as file:
                data = json.load(file)
                document_id = data["document_id"]
                tokens = data["tokens"]
                documents[document_id] = tokens
                tf_matrix[document_id] = compute_tf(tokens)

    # Compute IDF for all terms
    idf = compute_idf(documents)

    # Compute TF-IDF matrix
    tf_idf_matrix = {}
    for document_id, tf in tf_matrix.items():
        tf_idf_matrix[document_id] = compute_tf_idf(tf, idf)

    return tf_idf_matrix, sorted(idf.keys())


def save_tf_idf_matrix(tf_idf_matrix, terms, output_file):
    with open(output_file, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)

        # Write header
        header = ["Document ID"] + terms
        writer.writerow(header)

        # Write TF-IDF rows
        for document_id, tf_idf in tf_idf_matrix.items():
            row = [document_id] + [tf_idf.get(term, 0.0) for term in terms]
            writer.writerow(row)


if __name__ == "__main__":
    folder_path = "tig_corpus (json)"
    output_file = "tf_idf_matrix.csv"

    # Build the TF-IDF matrix
    tf_idf_matrix, terms = build_tf_idf_matrix(folder_path)

    # Save the TF-IDF matrix to a CSV file
    save_tf_idf_matrix(tf_idf_matrix, terms, output_file)

    print(f"TF-IDF matrix saved to {output_file}")
