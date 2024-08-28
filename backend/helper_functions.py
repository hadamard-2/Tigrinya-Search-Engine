import json
import os


current_dir = os.path.dirname(os.path.abspath(__file__))


def load_txt_file(file_name):
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def load_json_file(file_name):
    file_path = os.path.join(current_dir, file_name)
    with open(file_path, "r", encoding="utf-8") as file:
        collection_map = json.load(file)
    return collection_map


transliteration_table = load_json_file("SERA_transliteration.json")
transcription_table = {value: key for key, value in transliteration_table.items()}
vowels = ["e", "u", "i", "a", "E", "o"]


def transliterate(word: str) -> str:
    """
    Transliteration of word written in Ethiopic script using Latin alphabet.
    """
    if not all(char in transliteration_table.keys() for char in word):
        raise Exception(f"Found non-Ethiopic during transliteration")
        return
    return "".join([transliteration_table[letter] for letter in word])


def transcribe(word: str) -> str:
    """
    Converts transliterated word back to its original form.
    """

    processed_word = word
    for item in sorted(list(transcription_table.keys()), key=lambda item: -len(item)):
        processed_word = processed_word.replace(item, "")
    if processed_word != "":
        raise Exception(f"Found non-Ethiopic during transcription")
        return

    transcription = ""
    unit = ""
    i = 0
    while i < len(word):
        unit += word[i]

        # an exception
        if i != len(word) - 1 and unit + word[i + 1] == "ea":
            i += 1
            continue
        # if it's a vowel
        elif unit[-1] in vowels:
            try:
                transcription += transcription_table[unit]
                unit = ""
            except:
                raise Exception("Transcription is not working!")
        # if it's a consonant
        elif unit[-1] != "`":
            # if it's the last letter in the word or the next letter is a consonant or a single quote
            if i == len(word) - 1 or word[i + 1] not in set(vowels).union({"W"}):
                try:
                    transcription += transcription_table[unit]
                    unit = ""
                except:
                    raise Exception("Transcription is not working!")
        i += 1

    return transcription


import random


def generate_random_str(length: int, lst: list) -> str:
    random_str = ""

    for i in range(length):
        rand_int = random.randint(0, len(lst) - 1)
        random_str += lst[rand_int]

    return random_str


def normalize_helper(word, list1: list, list2: list):
    for i in range(len(list1)):
        word = word.replace(list1[i], list2[i])

    return word


def normalize(word):
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

    word = normalize_helper(word, h2, h1)
    word = normalize_helper(word, h3, h1)
    word = normalize_helper(word, s2, s1)
    word = normalize_helper(word, q2, q1)
    word = normalize_helper(word, a2, a1)
    word = normalize_helper(word, ts2, ts1)
    word = normalize_helper(word, exp2, exp1)

    return word


# NOTE - testing my methods
def main():
    for i in range(500):
        original_str = normalize(
            generate_random_str(5, list(transliteration_table.keys()))
        )
        transliterated_str = transliterate(original_str)
        transcribed_str = transcribe(transliterated_str)

        if original_str != transcribed_str:
            print(f"Error")
            print(f"Original String: {original_str}")
            print(f"Transliterated String: {transliterated_str}")
            print(f"Transcribed String: {transcribed_str}")
    print("Done!")


if __name__ == "__main__":
    main()
