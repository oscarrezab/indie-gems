import numpy as np
import pandas as pd
import re
from scipy import stats
import pickle

class Song():
    def __init__(self, id: str, title: str, artist: str, album_name: str, album_img: str, bpm: int, camelot: str, lyrics: np.array):
        self.id = id
        self.title = title
        self.artist = artist
        self.album_name = album_name
        self.album_img = album_img
        self.bpm = bpm
        self.camelot = camelot
        self.lyrics = lyrics

    def similarity_to(self, other):
        component_1 = 1 if np.isclose(self.bpm, other.bpm, atol=5) else 0  # 1 if bpm is within 5 beats, 0 otherwise
        component_2 = 1 if self.camelot == other.camelot else 0  # 1 if camelot integer is equal, 0 otherwise
        component_3 = stats.pearsonr(self.lyrics, other.lyrics)[0]  # compute pearson coefficient between the vectorial representations of each song's lyrics

        return ((component_1*0.3 + component_2*0.3 + component_3*0.3)), component_1, component_2, component_3
    
    def to_string(self):
        return f"'{self.title}' by {self.artist}"

if __name__ == "__main__":
    full_ds = pd.read_pickle('workable-dataset.pkl')

    test_song = full_ds.iloc[371]
    test_object = Song(test_song['song_id'], test_song['title'], test_song['artist'], test_song['album'], test_song['album_image'], 
                      test_song['BPM'], test_song['Camelot'], test_song['lyrics_vec'])

    print(f"Similar songs to {test_object.to_string()}")
    for song in full_ds.iloc:
        curr_song = Song(song['song_id'], song['title'], song['artist'], song['album'], song['album_image'], 
                         song['BPM'], song['Camelot'], song['lyrics_vec'])
        similarity = test_object.similarity_to(curr_song)
        if similarity[0] > 0.85 and curr_song.to_string() != test_object.to_string():
            print(curr_song.to_string(), f"(bpm: {similarity[1]}", f"camelot: {similarity[2]}", f"lyrics: {similarity[3]})")