"""Script for the new method of vectorization. This utilizes a pre-trained model from the sentence-transformers library.
Note: Based on implementation taken from https://medium.com/@ahmedmellit/text-similarity-implementation-using-bert-embedding-in-python-1efdb5194e65
"""
from sentence_transformers import SentenceTransformer
import pandas as pd

model = SentenceTransformer('sentence-transformers/all-mpnet-base-v2')
dataset = pd.read_csv("../res/full-dataset.csv")
lyrics_list = []
for lyrs in dataset.get('lyrics'):
    lyrics_embeddings = model.encode(lyrs)
    lyrics_list.append([lyrics_embeddings])

dataset['lyrics_vec'] = lyrics_list


# print(dataset)
dataset.to_pickle('newest_dataset.pkl')
