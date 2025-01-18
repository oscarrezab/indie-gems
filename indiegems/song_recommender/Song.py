"""
Class for the Song object, for use in the song recommender.

Created: January 2025 by Oscar Reza B.
"""

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

        lyric_pearson = pearson_correlation(self.lyrics, other.lyrics)  # compute pearson coefficient between the vectorial representations of each song's lyrics
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

def pearson_correlation(x, y):
    # Ensure the inputs are numpy arrays
    x = np.array(x)
    y = np.array(y)
    
    # Compute the mean of x and y
    mean_x = np.mean(x)
    mean_y = np.mean(y)
    
    # Compute the covariance (numerator)
    covariance = np.sum((x - mean_x) * (y - mean_y))
    
    # Compute the standard deviations (denominator)
    std_x = np.sqrt(np.sum((x - mean_x)**2))
    std_y = np.sqrt(np.sum((y - mean_y)**2))
    
    # Pearson correlation coefficient
    if std_x > 0 and std_y > 0:
        r = covariance / (std_x * std_y)
    else:
        r = 0  # Handle cases where variance is zero to avoid division by zero
    
    return r