from .helper_functions import *


class TigrinyaStemmer:
    """
    The corpus is assumed to have gone through morphological preprocessing.
    """

    # NOTE - never use replace method to remove prefix and suffix of any kind!!

    # vowels = ["ኧ", "ኡ", "ኢ", "ኣ", "ኤ", "እ", "ኦ"]
    vowels = ["e", "u", "i", "a", "E", "o"]

    def __init__(self, prefix_suffix_pairs, prefix_list, suffix_list):
        self.prefix_suffix_pairs = prefix_suffix_pairs
        self.prefix_list = prefix_list
        self.suffix_list = suffix_list

    def count_radicals(self, word=""):
        """Count the number of radicals (consonants) in a word."""
        return len(self.extract_root(word))

    def extract_root(self, word=""):
        return "".join(
            [char for char in word if char not in set(self.vowels).union({"'", "W"})]
        )

    def remove_prefix_suffix_pair(self, word=""):
        """
        Prefix-suffix pairs are usually used to derive nouns from verbs.
        """
        stemmed_word = transliterate(word)
        prefix_suffix_pairs = [
            (transliterate(pair[0]), transliterate(pair[1]))
            for pair in self.prefix_suffix_pairs
        ]

        i = 0
        while self.count_radicals(stemmed_word) > 3 and i < len(prefix_suffix_pairs):
            prefix = prefix_suffix_pairs[i][0]
            suffix = prefix_suffix_pairs[i][1]
            if (
                stemmed_word.startswith(prefix)
                and stemmed_word.endswith(suffix)
                and self.count_radicals(word) - self.count_radicals(prefix + suffix)
                >= 3
            ):
                prefix_removed = stemmed_word[len(prefix) :]
                suffix_removed = prefix_removed[: -len(suffix)]
                stemmed_word = suffix_removed
            i += 1

        try:
            return transcribe(stemmed_word)
        except:
            print(f"Word: {word}\nStemmed Word: {stemmed_word}\b")
            return word

    def remove_double_reduplication(self, word=""):
        if self.count_radicals(word) < 5:
            return word

        stemmed_word = word
        for i in range(len(stemmed_word) - 3):
            if stemmed_word[i : i + 2] == stemmed_word[i + 2 : i + 4]:
                return stemmed_word[: i + 2] + stemmed_word[i + 4 :]
        return stemmed_word

    def remove_prefix(self, word=""):
        stemmed_word = transliterate(word)

        prefix_list = [transliterate(prefix) for prefix in self.prefix_list]
        i = 0
        while self.count_radicals(stemmed_word) > 3 and i < len(prefix_list):
            if stemmed_word.startswith(prefix_list[i]) and (
                self.count_radicals(stemmed_word) - self.count_radicals(prefix_list[i])
                >= 3
            ):
                stemmed_word = stemmed_word[len(prefix_list[i]) :]
            i += 1

        try:
            return transcribe(stemmed_word)
        except:
            print(f"Word: {word}\nStemmed Word: {stemmed_word}\b")
            return word

    def remove_suffix(self, word=""):
        stemmed_word = transliterate(word)

        suffix_list = [transliterate(suffix) for suffix in self.suffix_list]
        i = 0
        while self.count_radicals(stemmed_word) > 3 and i < len(suffix_list):
            if stemmed_word.endswith(suffix_list[i]) and (
                self.count_radicals(stemmed_word) - self.count_radicals(suffix_list[i])
                >= 3
            ):
                stemmed_word = stemmed_word[: -len(suffix_list[i])]
            i += 1

        try:
            return transcribe(stemmed_word)
        except:
            print(f"Word: {word}\nStemmed Word: {stemmed_word}\b")
            return word

    def remove_single_reduplication(self, word=""):
        if self.count_radicals(word) < 4:
            return word

        stemmed_word = word
        for i in range(len(stemmed_word) - 1):
            consonant1 = self.extract_root(transliterate(stemmed_word[i]))
            consonant2 = self.extract_root(transliterate(stemmed_word[i + 1]))
            if consonant1 == consonant2:
                return stemmed_word[:i] + stemmed_word[i + 1 :]

        return stemmed_word

    def stem(self, word=""):
        """
        For simplicity implementation is done assuming the method gets called passing a word.
        In practice, stem method should run on corpus.
        """

        stemmed_word = word

        stemmed_word0 = self.remove_prefix_suffix_pair(stemmed_word)
        stemmed_word1 = self.remove_double_reduplication(stemmed_word0)
        stemmed_word2 = self.remove_prefix(stemmed_word1)
        stemmed_word3 = self.remove_suffix(stemmed_word2)
        stemmed_word4 = self.remove_single_reduplication(stemmed_word3)

        return stemmed_word4


def main():
    prefix_suffix_pairs = [("መ", "ቲ"), ("መ", "ያ"), ("መ", "ኢ"), ("መ", "ታ"), ("መ", "ት")]
    prefix_list = load_txt_file("lists/prefix_list.txt")
    suffix_list = load_txt_file("lists/suffix_list.txt")

    stemmer = TigrinyaStemmer(prefix_suffix_pairs, prefix_list, suffix_list)
    preprocessor = TigMorphPreprocess()

    # ps_words = ["መቅበሪ", "መንግስቲ", "መወርወሪ", "መድሓኒት", "መጀመርታ"]
    # dlp_words = ["ገልጠምጠም"]
    # p_words = ["ንሰላም"]
    # s_words = ["ማዕከላት"]
    # dlp_words2 = ["ሰባቢሩ", "ቆራሪጹ"]
    # for word in dlp_words2:
    #     preprocessed_word0 = preprocessor.normalize(word)
    #     preprocessed_word1 = preprocessor.remove_stopwords(preprocessed_word0)
    #     if preprocessed_word1 == "":
    #         print(
    #             f"The word you provided ({word}) was removed during the preprocessing stage!"
    #         )
    #     else:
    #         stemmed_word = stemmer.stem(preprocessed_word)
    #         print(f"{word} --> {stemmed_word}")

    word = "ቆራሪጹ"
    preprocessed_word0 = preprocessor.normalize(word)
    preprocessed_word1 = preprocessor.remove_stopwords(preprocessed_word0)
    if preprocessed_word1 == "":
        print(
            f"The word you provided ({word}) was removed during the preprocessing stage!"
        )
    else:
        stemmed_word = stemmer.stem(preprocessed_word)
        print(f"{word} --> {stemmed_word}")


if __name__ == "__main__":
    main()
