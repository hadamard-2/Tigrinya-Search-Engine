import re
import json


def load_txt_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        return file.read().splitlines()


def load_json_file(filepath):
    with open(filepath, "r", encoding="utf-8") as file:
        collection_map = json.load(file)
    return collection_map


transliteration_table = load_json_file("SERA_transliteration.json")
transcription_table = {value: key for key, value in transliteration_table.items()}
vowels = ["e", "u", "i", "a", "E", "", "o"]


def transliterate(word: str) -> str:
    """
    Transliteration of word written in Ethiopic script using Latin alphabet.
    """
    if not all(char in transliteration_table.keys() for char in word):
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
        return

    transcription = ""
    unit = ""
    i = 0
    while i < len(word):
        unit += word[i]
        # if it's a vowel
        if unit[-1] in vowels:
            transcription += transcription_table[unit]
            unit = ""
        # if it's a consonant
        elif unit[-1] not in {"`", "W"}:
            # if it's the last letter in the word or the next letter is a consonant or a single quote
            if i == len(word) - 1 or word[i + 1] not in set(vowels).union({"W"}):
                try:
                    transcription += transcription_table[unit]
                    unit = ""
                except:
                    print(f"Unit: {unit}")
        i += 1

    return transcription


def main():
    print(transcribe("nKulu"))


if __name__ == "__main__":
    main()

