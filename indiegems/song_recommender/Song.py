"""
Class for the Song object, for use in the song recommender.

Created: January 2025 by Oscar Reza B.
"""

import numpy as np
from scipy import stats

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
        bpm_diff = abs(self.bpm - other.bpm)
        if bpm_diff == 0: component_1 = 1
        elif bpm_diff < 15: component_1 = 0.75
        elif bpm_diff < 25: component_1 = 0.5
        else: component_1 = 0
        # component_1 = 1 if np.isclose(self.bpm, other.bpm, atol=5) else 0  # 1 if bpm is within 5 beats, 0 otherwise
        
        component_2 = 1 if self.camelot == other.camelot else 0  # 1 if camelot integer is equal, 0 otherwise

        lyric_pearson = stats.pearsonr(self.lyrics, other.lyrics)[0]  # compute pearson coefficient between the vectorial representations of each song's lyrics
        if np.isclose(lyric_pearson, 1, atol=0.0001): component_3 = 1
        elif lyric_pearson > 0.98: component_3 = 0.8
        elif lyric_pearson > 0.96: component_3 = 0.6
        elif lyric_pearson > 0.94: component_3 = 0.4
        elif lyric_pearson > 0.92: component_3 = 0.2
        elif lyric_pearson > 0.90: component_3 = 0.1
        else: component_3 = 0
        # component_3 = stats.pearsonr(self.lyrics, other.lyrics)[0]  

        return [component_1, component_2, component_3]
    
    def set_similarity(self, score):  
        self.similarity_score = score

    def to_string(self):
        '''Get the song in the format {title} by {artist}'''
        return f"'{self.title}' by {self.artist}"
