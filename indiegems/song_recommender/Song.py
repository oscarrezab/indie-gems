"""
Class for the Song object, for use in the song recommender.

Created: January 2025 by Oscar Reza B.
"""
from sklearn.metrics.pairwise import cosine_similarity

import numpy as np

class Song():
    def __init__(self, id: int, title: str, artist: str, album_name: str, album_img: str, bpm: int, camelot: str, lyrics: np.array):
        '''A song object, containing its relevant metadata.
        '''
        self.id = id
        self.title = title
        self.artist = artist
        self.album_name = album_name
        self.album_img = album_img
        self.bpm = bpm
        self.camelot = camelot
        self.lyrics = lyrics
        self.similarity_score = 0

    def similarity_to(self, other):
        '''Compute this song's similarity with another one.'''
        bpm_diff = abs(self.bpm - other.bpm) / 140  # highest bpm is 204, while lowest is 64, 140 is the highest difference, so we subtract it to get a value between 1 and 0
        component_1 = 1 - bpm_diff * 2  # multiplied diff times 2 to make effect more pronounced
        # component_1 = 1 if np.isclose(self.bpm, other.bpm, atol=5) else 0  # 1 if bpm is within 5 beats, 0 otherwise
        
        component_2 = 1 if self.camelot == other.camelot else 0  # 1 if camelot integer is equal, 0 otherwise
        component_3 = cosine_similarity(self.lyrics, other.lyrics)[0][0]
        
        # component_3 = stats.pearsonr(self.lyrics, other.lyrics)[0]  

        return [component_1, component_2, component_3]
    
    def set_similarity(self, score):  
        self.similarity_score = score

    def to_string(self):
        '''Get the song in the format {title} by {artist}'''
        return f"'{self.title}' by {self.artist}"
