"""Script for the new method of vectorization. This utilizes a pre-trained model from the sentence-transformers library.
Note: Based on implementation taken from https://medium.com/@ahmedmellit/text-similarity-implementation-using-bert-embedding-in-python-1efdb5194e65
"""
import re
import pandas as pd
from sentence_transformers import SentenceTransformer
import nltk
from torch import Tensor
nltk.download('punkt')

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')

def get_lyrics_from_csv(input: str | pd.DataFrame) -> list[str]:
    '''
    Reads the given csv and returns the list of lyrics as a list[str]

    :param str | DataFrame input: either (1) the filepath for the csv to read 
    or (2) the pandas DataFrame itself
    :return: the list of lyrics as a list of strings
    :rtype: list[str]
    '''
    loaded_csv = pd.read_csv(input) if isinstance(input, str) else input
    lyrics = loaded_csv.get('lyrics')
    assert lyrics is not None
    lyrics = lyrics.to_list()
    
    return lyrics

def preprocess_lyrics(lyrics : str) -> str:
    '''
    Take in the lyrics (or any string of text) to make lowercase and remove special characters.

    :param str lyrics: a string of song lyrics
    :return: a string of the preprocessed lyrics
    :rtype: str
    '''
    # Make lowercase
    lyrics = str(lyrics).lower()

    # Remove headers such as [Chorus] and [Verse 1]
    no_headers = re.sub(r'\[.*?\]', '', lyrics)

    # Tokenize
    tokens = nltk.word_tokenize(no_headers)

    # Remove special characters
    tokens = [re.sub(r'[^a-zA-Z0-9\'.,]', '', token) for token in tokens]
    tokens = [token for token in tokens if token]  # Remove empty tokens

    # Join tokens back into a cleaned string
    cleaned_lyrics = ' '.join(tokens)

    return cleaned_lyrics


def preprocess_lyrics_list(lyrics_list: list[str]) -> list[str]:
    '''
    Take in a list of lyrics (or of any string of text) to make lowercase and remove special characters.

    :param str lyrics_list: a list of strings of song lyrics
    :return: a list of strings of the preprocessed lyrics
    :rtype: list[str]
    '''
    return [preprocess_lyrics(lyrics) for lyrics in lyrics_list]


def vectorize_lyrics(lyrics: str) -> Tensor:
    '''
    Vectorize lyrics (or any string) using the sentence-transformers model.

    :param str lyrics: the pre-processed lyrics as a string
    '''
    

    lyrics_embeddings = model.encode(lyrics)

    return lyrics_embeddings


def vectorize_lyrics_list(lyrics_list: list[str]) -> list[Tensor]:
    '''
    Vectorize a list of lyrics (or of any string) using the sentence-transformers model.

    :param list[str] lyrics_list: a list of pre-processed lyrics as a list of strings
    '''
    count = 0
    vectorized = []
    for lyrics in lyrics_list:
        vectorized.append(vectorize_lyrics(lyrics))
        if count % 50 == 0:
            print(f"-- Vectorized lyrics for {count} songs so far")
        count += 1
    return vectorized

def create_vectorized(dataset_path: str) -> pd.DataFrame:
    '''
    Vectorize the lyrics from an input csv file representing the song dataset.

    :param str dataset_path: the path for the dataset csv
    :return: a pandas DataFrame with the full dataset and vectorized lyrics
    :rtype: pd.DataFrame
    '''
    # Load the csv
    lyrics_df = pd.read_csv(dataset_path)
    # Get the list of lyrics
    lyrics_list = get_lyrics_from_csv(lyrics_df)
    # Preprocess these lyrics
    lyrics_preprocessed = preprocess_lyrics_list(lyrics_list)
    # Vectorize the lyrics
    lyrics_vectorized = vectorize_lyrics_list(lyrics_preprocessed)
    # Replace text lyrics with their vectorized version
    lyrics_df['lyrics'] = lyrics_vectorized
    
    return lyrics_df


if __name__ == "__main__":
    vectorized_df = create_vectorized("res/new_pipeline/all_songs_test_oct_31.csv")

    vectorized_df.to_csv("res/new_pipeline/vectorized_all_songs_test_oct_31.csv")

    




    