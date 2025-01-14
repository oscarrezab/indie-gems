"""
The song recommendation script. Its aim is to compute a song's similarities with the other songs in the dataset in order to recommend
those with the highest scores.

Created: January 2025 by Oscar Reza B.
"""

import pandas as pd
import numpy as np
from Song import Song

full_ds = pd.read_pickle('workable-dataset.pkl')

test_song = full_ds.iloc[358]
test_object = Song(test_song['song_id'], test_song['title'], test_song['artist'], test_song['album'], test_song['album_image'], 
                    test_song['BPM'], test_song['Camelot'], test_song['lyrics_vec'])

# Initialize similarity list
similarities = {}
comp_3s = []

# Get song similarities
for song in full_ds.iloc:
    curr_song = Song(song['song_id'], song['title'], song['artist'], song['album'], song['album_image'], 
                        song['BPM'], song['Camelot'], song['lyrics_vec'])
    curr_sim = test_object.similarity_to(curr_song)
    similarities[curr_song.to_string()] = curr_sim

    comp_3 = curr_sim[2]
    comp_3s.append(comp_3)

# Compute and print recommendation scores
print(f"Songs similar to {test_object.to_string()}:")
for key in similarities.keys():
    scores = similarities.get(key)
    rec_score = (scores[0] + scores[1] + scores[2]) / 3
    if rec_score > 0.75:
        print(f"{key} ({np.round(rec_score*100, 2)}%)")
        print(f"-- similarity breakdown: (bpm: {scores[0]}  key: {scores[1]}  lyrics: {scores[2]})")

