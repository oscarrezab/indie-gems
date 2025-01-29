"""
The song recommendation script. Its aim is to compute a song's similarities_map with the other songs in the dataset in order to recommend
those with the highest scores.

Created: January 2025 by Oscar Reza B.
"""

import pandas as pd

from .Song import Song

class SongRecommendation():
    def __init__(self, song_id: int, dataset_path: str = 'song_recommender/newest_dataset.pkl'):
        self.dataset =  pd.read_pickle(dataset_path)
        self.song = self.song_object_from_id(song_id)
        self.similar_songs = self.compute_recommendations()

    def get_source_song(self):
        return self.song
    
    def get_similar_songs(self):
        return self.similar_songs
    
    def song_object_from_id(self, song_id):
        song_in_ds = self.dataset.iloc[song_id]  # Assumes the song id is equal to its index in the dataset
        song_object = Song(song_in_ds['song_id'], song_in_ds['title'], song_in_ds['artist'], song_in_ds['album'], song_in_ds['album_image'], 
                            song_in_ds['BPM'], song_in_ds['Camelot'], song_in_ds['lyrics_vec'])       
        
        return song_object

    def compute_recommendations(self):
        # Initialize similarity map and recommendations list
        similarities_map = {}  # maps {song object : list of similarity scores}
        recommendations = []

        # Get song similarities
        for song in self.dataset.iloc:
            curr_song = Song(song['song_id'], song['title'], song['artist'], song['album'], song['album_image'], 
                                song['BPM'], song['Camelot'], song['lyrics_vec'])
            if curr_song.to_string() != self.song.to_string():
                curr_sim = self.song.similarity_to(curr_song)
                similarities_map[curr_song] = curr_sim

        # Compute recommendation scores
        for song in similarities_map.keys():
            scores = similarities_map.get(song)
            overall_score = (scores[0] + scores[1] + scores[2]) / 3  # computes the overall score
            if overall_score > 0.80:
                song.set_similarity(round(overall_score*100, 2))
                recommendations.append(song)  # add the song object, alongside its overall score

        # Return the recommendations as a response
        return recommendations
    
    def get_all_songs_and_ids(self):
        song_map = {}
        for i in range(len(self.dataset.index)):
            song = self.song_object_from_id(i)
            song_map[song.to_string()] = i
        return song_map
    

# if __name__ == "__main__":
#     recommender = SongRecommendation(0)
#     for title in recommender.get_all_songs_and_ids().values():
#         print(title)