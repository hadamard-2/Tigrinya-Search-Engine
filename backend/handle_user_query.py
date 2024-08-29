from flask import Flask, request, jsonify

from .preprocessing import TigMorphPreprocess

app = Flask(__name__)


@app.route("/search", methods=["POST"])
def search_query():
    data = request.json
    query = data.get("query")

    if not query:
        return jsonify({"error": "No query provided"}), 400

    # Instantiate and preprocess the query
    # psr = TigMorphPreprocess([query])
    # tokens = psr.tokenize().normalize().remove_stopwords().stem().get_result()

    # use the tokens to retrieve documents and return them ranked in the following way
    # [
    #     {
    #         "document_title:" "1st_document_title",
    #         "document_location:" "1st_document_location",
    #     },
    #     {
    #         "document_title": "2nd_document_title",
    #         "document_location": "2nd_document_location",
    #     },
    #     {
    #         "document_title": "3rd_document_title",
    #         "document_location": "3rd_document_location",
    #     },
    # ]

    return jsonify({"it": "works!"})


if __name__ == "__main__":
    app.run(debug=True)
