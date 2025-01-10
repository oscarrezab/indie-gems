"""
Script to pre-process lyrics before tokenizing.

Usage: Just run the main script and it should identify the files to merge. It is currently set to work with the specific files
of indie test 1 and 2, so changes must be made for further development.

Created: January 2025 by Oscar Reza Bautista
Note: This script was adapted from the author's final project for COMP 394: Natural Language Processing, 
Fall 2024 at Macalester College
"""

import nltk
import re
import pandas as pd
nltk.download('punkt')

class LyricsPreprocessor:
    """Class to pre-process text. It prints output to the terminal, which can be copied into the desired txt file."""

    def get_text_from_csv(filepath):
        loaded_csv = pd.read_csv(filepath)
        lyrics = loaded_csv.get('lyrics')
        
        return lyrics.to_list()

    def preprocess_text(text : str) -> str:
        # Make lowercase
        text = text.lower()

        # Tokenize
        tokens = nltk.word_tokenize(text)

        # Remove special characters
        tokens = [re.sub(r'[^a-zA-Z0-9\'.,]', '', token) for token in tokens]
        tokens = [token for token in tokens if token]  # Remove empty tokens

        # Join tokens back into a cleaned string
        cleaned_text = ' '.join(tokens)

        return cleaned_text


if __name__ == "__main__":
    all_lyrics = LyricsPreprocessor.get_text_from_csv("full-dataset.csv")
    # print(type(all_lyrics[0]))
    preprocessed_lyrics = [LyricsPreprocessor.preprocess_text(lyric) for lyric in all_lyrics]
    # print(preprocessed_lyrics[56])

    # Load full dataset and create copy (just to be safe lol)
    all_data = pd.read_csv("full-dataset.csv")
    data_copy = all_data
    original_lyrics = all_data.get('lyrics')

    # Replace original lyrics with their respective preprocessed version
    for original, preprocessed in zip(original_lyrics, preprocessed_lyrics):
        data_copy = data_copy.replace(original, preprocessed)

    # print(data_copy.drop('Unnamed: 0',axis=1))
    data_copy.drop('Unnamed: 0',axis=1).to_csv("full-dataset-with-preprocessing.csv")  # Remove extra column and save csv
