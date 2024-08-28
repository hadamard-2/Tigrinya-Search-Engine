from collections import Counter
import numpy as np
import re

from backend.helper_functions import *
from backend.girma_stemmer import TigrinyaStemmer
# from helper_functions import *
# from girma_stemmer import TigrinyaStemmer


class TigMorphPreprocess:
    """
    Class for doing Tigrinya specific morphological preprocessing.
    Works for both large text corpus and single words.
    """

    def __init__(self, corpus):
        self.corpus = corpus

    def handle_contraction(self):
        """
        Input: corpus (string)
        Output: corpus (list)

        Operates on word level.
        Removes single quotes along with succeeding portions of
        """
        quote_vars = [
            "\u0027",
            "\u2018",
            "\u2019",
            "\u2032",
            "\u02BC",
            "\u0060",
            "\u00B4",
        ]
        split_corpus = self.corpus.split()
        remove_contraction = lambda word: next(
            (word.split(char)[0] for char in word if char in quote_vars), word
        )

        self.corpus = " ".join(list(map(remove_contraction, split_corpus)))

    def filter_text(self):
        """
        Removes English & Ethiopic punctuation marks.
        Removes words containing a non-alphabetic character.
        """

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
        filtered_corpus0 = re.sub(eng_pattern, "", self.corpus)

        eth_pattern = r"[\u1361-\u1368]+"
        filtered_corpus1 = re.sub(eth_pattern, "", filtered_corpus0)

        ethiopic_letters = load_json_file("SERA_transliteration.json")

        # remove any word containing a non-alphabetic character
        # think hard about why we removed punctuations first
        filtered_corpus_final = []
        for word in filtered_corpus1.split():
            if all(char in ethiopic_letters.keys() for char in word):
                filtered_corpus_final.append(word)

        self.corpus = " ".join(filtered_corpus_final)

    # NOTE - keeping dates is not worth the added complexity, as a result we have decided to remove them
    # Task 1
    def tokenize(self):
        """
        Handles Tigrinya specific contractions.
        Removes words containing non-alphabet characters from corpus.
        """
        self.handle_contraction()
        self.filter_text()

        return self

    def normalize_helper(self, list1: list, list2: list):
        for i in range(len(list1)):
            self.corpus = self.corpus.replace(list1[i], list2[i])

    # REVIEW - Normalization of Tigrinya text can be further enhanced by...
    # converging Tigrinya-specific abbreviations of different form.
    # (eg. ገ/ስላሴ --> ገብረስላሴ)
    # Task 2
    def normalize(self):
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

        exp1 = ["ጓ", "ቋ"]
        exp2 = ["ጏ", "ቇ"]

        self.normalize_helper(h2, h1)
        self.normalize_helper(h3, h1)
        self.normalize_helper(s2, s1)
        self.normalize_helper(q2, q1)
        self.normalize_helper(a2, a1)
        self.normalize_helper(ts2, ts1)
        self.normalize_helper(exp2, exp1)

        return self

    # Task 3
    def remove_stopwords(self):
        """
        Removes
        - predefined stopwords from the corpus
        """
        stopwords = load_txt_file("lists/stopword_list.txt")

        for stopword in stopwords:
            self.corpus = self.corpus.replace(stopword, "")

        return self

    # Task 4
    def stem(self):
        """
        Stems words in corpus
        Removes
        - tokens with length < 3
        - tokens with frequencies below the given percentile threshold
        """

        prefix_suffix_pairs = [
            ("መ", "ቲ"),
            ("መ", "ያ"),
            ("መ", "ኢ"),
            ("መ", "ታ"),
            ("መ", "ት"),
        ]
        prefix_list = load_txt_file("lists/prefix_list.txt")
        suffix_list = load_txt_file("lists/suffix_list.txt")

        stemmer = TigrinyaStemmer(prefix_suffix_pairs, prefix_list, suffix_list)
        tokens = list(map(stemmer.stem, self.corpus.split()))

        percentile_threshold = 10

        # Calculate the frequency of each word in the corpus
        word_freq = Counter(tokens)

        # Determine the frequency threshold based on the given percentile
        frequencies = list(word_freq.values())
        threshold_value = np.percentile(frequencies, percentile_threshold)

        # Filter out words with length < 3 and those below the frequency threshold
        filtered_tokens = [
            token
            for token in tokens
            if len(token) >= 3 and word_freq[token] >= threshold_value
        ]

        self.corpus = filtered_tokens

        return self

    def get_result(self):
        return self.corpus

def main():
    corpus = """
    ቤተ - መንግስቲ ዋይት ሃውስ ኣብ ዘውጸኦ መግለጺ ፡ “ዋና ኣኽባር ሕጊ ሳሊ ያትስ ንምምሕዳር ትራምፕ ከዲዓቶ” ብምባል ስራሕ ደው ከተብል ተወሲኑ ምህላዉ ኣፍሊጡ ።
    ፕረዚደንት ትራምፕ ፡ ኣብዚ ሰሙን’ዚ ዜጋታት ኢራን ፡ ሊብያ ፡ ሶማል ፡ ሱዳን ፡ የመን ፡ ዒራቕን ሶርያን ናብ ኣመሪካ ከይኣትዉ ዝኽልክል ትእዛዝ ከም ዘመሓላለፈ ዝፍለጥ እዩ ።
    መራሕቲ ሃገራት ኣፍሪቃ ኣብ ዘካየድዎ መስርሕ ምድማጽ ፡ ሞሮኮ ዳግማይ ናብ ኣፍሪቃዊ ሕብረት ክትጽንበር ደጊፎም ።
    ኣብ መበል 28 ዋዕላ መራሕቲ ሃገራት ኣፍሪቃ ኣብ ዝተኻየደ መስርሕ ምርጫ ፡ ካብ 54 ሃገራት እተን 39 ንጠለብ ሞሮኮ ብምቕባል ፡ እታ ሃገር ምሉእ ኣባልነት ክትረክብ ከምዝደገፋ ምንጭታት ዜና ሓቢሮም ።
    ሞሮኮ ፡ ውድብ ሓድነት ኣፍሪቃ ንምዕራብ ሰሃራ ኣፍልጦ ብምሃቡ ፡ ኣብ 1984 ካብ ኣባልነት ናይ’ቲ ውድብ ከምዘንሰሓበት ይፍለጥ ።
    ሞሮኮ ኣብ 1991 ምዕራብ ሰሃራ ረፈረንደም ከተካይድ ተሰማሚዓ’ኳ እንተነበረት ፡ ኣብ መንነት ኣድመጽቲ ብዝተላዕለ ዘይምቅዳው ፡ እቲ ረፈረንደም ክካየድ ከምዘይከኣለ ጸብጻባት የመልክቱ ።
    ኣብ 1975 መግዛእቲ ስጳኛ ካብ ምዕራብ ሰሃራ ምስ ወጽአ ፡ ሞሮኮ ብኡ ንብኡ ነቲ ከባቢ ከም ዝተቖጻጸረቶ ይግለጽ ።
    ሞሮኮ ድሕሪ 33 ዓመት ናብ ሕብረት ኣፍሪቃ ምምላሳ ፡ ንጉዳይ ምዕራብ ሰሃራ ሰላማዊ ፍታሕ ኣብ ምንዳይ ሓጋዚ ክኸውን ከም ዝኽእል ፕረዚደንት ሰኔጋል ማኪ ሳል ንጋዜጠኛታት ሓቢሩ ።
    ተወሳኺ ቻይናዊ ወተሃደር ዋንግ ቺ ፡ ምስታ ኣብ ዶብ ህንዲ ዝዓስከረት ኣሃዱ ካብ ዝጽንበር ነዊሕ ኣይገበረን ።
    ሓደ ረፍዲ ‘ክናፈስ’ ብምባል ካብ መዓስከሩ ብዝወጸ ፡ ብኡ ንብኡ’ዩ ኣብ ኢድ ወተሃደራት ህንዲ ዝወደቐ ።
    “ኣብ ሓለዋ እንከለኹ መገዲ ተደናጊረ” ይብል ንሱ ።
    ምልክት ቀይሕ መስቀል ዝነበራ መኪና ክትሓልፍ እንከላ ንመራሒ መኪና ክማልኦ ሓተቶ ።
    ሽዑ እቲ መራሕ መኪና ትኽ ኣቢሉ ናብ ወተሃደራት ህንዲ ከም ዘስተለሞ ዋንግ ቺ ይዝክር ።
    እዚ ፍጻመ ኣብ 1963 እዩ ኣጋጢሙ ።
    ካብኡ ጀሚሩ ድማ እነሆ ኣብ ህንዲ 50 ዓመት ተቐሚጡ ።
    ዋንግ ቺ ከምዝብሎ ፡ ኣብ ህንዲ ናይ ፈለማ ሸውዓተ ዓመት ኣብ ቤት - ማእሰርቲ እዩ ኣሕሊፍወን ።
    ድሒሩ’ኳ እንተተፈትሐ ፡ ዝኾነ ሕጋዊ መንቀሳቐሲ ስለዘይተዋህቦ ፡ ንሓምሳ ዓመት ዝኣክል ናብ ሃገሩ ኣይተመልሰን ።
    እቲ ካብ ‘ቲሮዲ’ ዝተባህለት ንእሽቶ ዓዲ ክወጽእ ብሕጊ ዝተኸልከለ ቻይናዊ ፡ ናብ ዓዱ ክምለስ ንኣመሓደርቲ ናይ’ቲ ከባቢ ብተደጋጋሚ ዘቕረቦ ሕቶ ተቐባልነት ከም ዘይረኸበ ሓቢሩ ።
    ኣብ ህንዲ ትሑት ደረጃ መነባብሮ ክመርሕ ከም እተገደደ ድማ ኣረዲኡ ።
    እቲ ቻይናዊ ቅኑዕን ጻዕራምን ምዃኑ ጐረባብቱ ይምስክርሉ ።
    """

    psr = TigMorphPreprocess(corpus)
    psr.tokenize().normalize().remove_stopwords().stem()
    tokens = psr.get_result()

    print(" ".join(tokens))

if __name__ == "__main__":
    main()