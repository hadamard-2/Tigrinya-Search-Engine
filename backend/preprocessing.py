from helper_functions import *


class TigMorphPreprocess:
    """
    Class for doing Tigrinya specific morphological preprocessing.
    Works for both large text corpus and single words.
    """

    def __init__(self, corpus):
        self.corpus = corpus

    def handle_contraction(self):
        """
        Operates on word level.
        Removes single quotes along with succeeding portions of 
        """
        quote_vars = ["\u0027", "\u2018", "\u2019", "\u2032", "\u02BC", "\u0060", "\u00B4"]
        split_corpus = self.corpus.split()
        remove_contraction = lambda word: next((word.split(char)[0] for char in word if char in quote_vars), word)

        self.corpus = list(map(remove_contraction, split_corpus))

    def filter_text(self):
        english_punctuation = "".join(
            [
                "\u002E",  # Period.
                "\u002C",  # Comma.
                "\u0021",  # Exclamation Mark.
                "\u003F",  # Question Mark.
                "\u003A",  # Colon.
                "\u003B",  # Semicolon.
                "\u0027",  # Apostrophe.
                "\u0022",  # Double Quotation Mark.
                "\u201C",  # Left Double Quotation Mark.
                "\u201D",  # Right Double Quotation Mark.
                "\u2018",  # Left Single Quotation Mark.
                "\u2019",  # Right Single Quotation Mark.
                "\u2010",  # Hyphen.
                "\u2013",  # En Dash.
                "\u2014",  # Em Dash.
                "\u0028",  # Left Parenthesis.
                "\u0029",  # Right Parenthesis.
                "\u005B",  # Left Square Bracket.
                "\u005D",  # Right Square Bracket.
                "\u007B",  # Left Curly Bracket.
                "\u007D",  # Right Curly Bracket.
                "\u2026",  # Ellipsis.
                "\u002F",  # Slash
                "\u005C",  # Backslash
                "\u0026",  # Ampersand
                "\u002A",  # Asterisk
            ]
        )
        eng_pattern = f"[{re.escape(english_punctuation)}]"
        filtered_corpus0 = list(map(lambda word: re.sub(eng_pattern, "", word), self.corpus))

        eth_pattern = r"[\u1361-\u1368]+"
        filtered_corpus1 = list(map(lambda word: re.sub(eth_pattern, "", word), filtered_corpus0))

        ethiopic_letters = load_json_file("SERA_transliteration.json")

        # remove any word containing a non-alphabetic character
        # think hard about why we removed punctuations first
        filtered_corpus_final = []
        for word in filtered_corpus1:
            if all(char in ethiopic_letters.keys() for char in word):
                filtered_corpus_final.append(word)

        self.corpus = filtered_corpus_final

    # NOTE - keeping dates is not worth the added complexity, as a result they get removed.
    def tokenize(self) -> str:
        """
        Handles Tigrinya specific contractions.
        Removes words containing non-alphabet characters from corpus.
        """
        self.handle_contraction()
        self.filter_text()

    def normalize_helper(self, list1: list, list2: list):
        for i in range(len(list1)):
            self.corpus = self.corpus.replace(list1[i], list2[i])

    # REVIEW - Normalization of Tigrinya text can be further enhanced by considering abbreviations.
    # (eg. ገ/ስላሴ --> ገብረስላሴ)
    def normalize(self) -> str:
        """
        Converges similar sounding characters.
        """
        h1 = ["ሐ", "ሑ", "ሒ", "ሓ", "ሔ", "ሕ", "ሖ", "ሗ", "ሗ"]
        h2 = ["ሀ", "ሁ", "ሂ", "ሃ", "ሄ", "ህ", "ሆ", "ሗ", "ሗ"]
        h3 = ["ኀ", "ኁ", "ኂ", "ኃ", "ኄ", "ኅ", "ኆ", "ኇ", "ኋ"]

        s1 = ["ሰ", "ሱ", "ሲ", "ሳ", "ሴ", "ስ", "ሶ", "ሷ"]
        s2 = ["ሠ", "ሡ", "ሢ", "ሣ", "ሤ", "ሥ", "ሦ", "ሧ"]

        q1 = ["ቀ", "ቁ", "ቂ", "ቃ", "ቄ", "ቅ", "ቆ", "ቈ", "ቊ", "ቋ", "ቌ", "ቍ"]
        q2 = ["ቐ", "ቑ", "ቒ", "ቓ", "ቔ", "ቕ", "ቖ", "ቘ", "ቚ", "ቛ", "ቜ", "ቝ"]

        a1 = ["አ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"]
        a2 = ["ዐ", "ዑ", "ዒ", "ዓ", "ዔ", "ዕ", "ዖ"]

        ts1 = ["ጸ", "ጹ", "ጺ", "ጻ", "ጼ", "ጽ", "ጾ", "ጿ"]
        ts2 = ["ፀ", "ፁ", "ፂ", "ፃ", "ፄ", "ፅ", "ፆ", "ጿ"]

        self.normalize_helper(h2, h1)
        self.normalize_helper(h3, h1)
        self.normalize_helper(s2, s1)
        self.normalize_helper(q2, q1)
        self.normalize_helper(a2, a1)
        self.normalize_helper(ts2, ts1)

    def remove_stopwords(self):
        """
        Removes 
        - a predefined stopwords from the corpus
        - tokens with length < 3 
            (# NOTE - I don't feel like such words add much meaning if any.)
        """
        stopwords = load_txt_file("stopword_list.txt")

        for stopword in stopwords:
            self.corpus = self.corpus.replace(stopword, "")
        
        return [token for token in self.corpus.split() if len(token) >= 3]


# def main():
#     with open("tig_corpus.txt", "r", encoding="utf-8") as file:
#         raw_corpus = file.read()

#     preprocessor = TigMorphPreprocess(raw_corpus)
#     preprocessor.normalize()
#     preprocessor.tokenize()
#     preprocessor.remove_stopwords()

#     with open("processed_tig_corpus.txt", "w", encoding="utf-8") as file:
#         file.write(preprocessor.corpus)


# if __name__ == "__main__":
#     main()

# single_quote_variations = ["\u0027", "\u2018", "\u2019", "\u2032", "\u02BC", "\u0060", "\u00B4"]
# for i in single_quote_variations:
#     print(i)


psr = TigMorphPreprocess("ዘለዎም’ዩ ሳላ'ቶም ህንጸት'ቲ")
psr.tokenize()
print(psr.corpus)