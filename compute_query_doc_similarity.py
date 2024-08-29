import pandas as pd
import numpy as np
from collections import Counter
import json
from datetime import datetime


def convert_date(date_str):
    # Parse the input date string using the format DDMMYYYY
    date_obj = datetime.strptime(date_str, "%d%m%Y")
    # Convert it to the desired format: Month, DD, YYYY
    formatted_date = date_obj.strftime("%B %d, %Y")
    return formatted_date


def cosine_similarity(vec1, vec2):
    dot_product = np.dot(vec1, vec2)
    magnitude1 = np.sqrt(np.dot(vec1, vec1))
    magnitude2 = np.sqrt(np.dot(vec2, vec2))
    if magnitude1 == 0 or magnitude2 == 0:
        return 0
    return dot_product / (magnitude1 * magnitude2)


def retrieve_docs(query_tokens):
    # Step 1: Load the Term-Document Matrix
    term_doc_matrix = pd.read_csv("term_document_matrix.csv", index_col=0)

    # Step 2: Extract Vocabulary and Initialize Query Vector
    vocabulary = term_doc_matrix.index.tolist()
    query_vector = np.zeros(len(vocabulary))

    # Step 3: Calculate TF-IDF for Query Terms
    query_term_freq = Counter(query_tokens)
    N = len(term_doc_matrix.columns)  # Number of documents

    for term, freq in query_term_freq.items():
        if term in vocabulary:
            term_index = vocabulary.index(term)
            df = (term_doc_matrix.loc[term] > 0).sum()  # Document frequency of the term
            idf = np.log(N / (1 + df))  # Compute IDF
            query_vector[term_index] = freq * idf  # TF-IDF for the term in the query

    # Transpose the matrix so that each row represents a document vector
    doc_vectors = term_doc_matrix.values.T

    # Step 4: Compute Cosine Similarity
    # Calculate cosine similarity between the query vector and each document vector
    cosine_similarities = []
    for doc_id, doc_vector in enumerate(doc_vectors):
        similarity = cosine_similarity(query_vector, doc_vector)
        cosine_similarities.append((doc_id, similarity))

    # Sort the documents by similarity score in descending order
    ranked_docs = sorted(cosine_similarities, key=lambda x: x[1], reverse=True)

    # Step 5: Compute document locations for the top 10 ranked documents
    top_docs = ranked_docs[:10]
    doc_locations = []
    for doc_id, score in top_docs:
        # Assuming doc_id is in the format 01022023 (date)
        doc_id_str = str(doc_id).zfill(8)  # Ensure doc_id is 8 digits
        document_location = f"tig_corpus (pdf)/haddas_eritra_{doc_id_str}.pdf"
        doc_locations.append(
            {
                "doc_title": f"{convert_date(doc_id)} - Haddas Eritrea",
                "doc_location": document_location,
            }
        )

    # Return the document locations in JSON format
    return json.dumps(doc_locations, indent=4)


# Example usage:
# query_tokens = ["example", "query", "terms"]
# doc_locations_json = retrieve_docs(query_tokens)
# print(doc_locations_json)

# print(convert_date("01022023"))
