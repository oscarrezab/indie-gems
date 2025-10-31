'''
Set of functions to extract lyrics and song metadata using `lyricsgenius` to access the
Genius API.

Pre-requisites: 
- A developer account for the GEnius API. In this code, the authentication variable is
GENIUS_KEY.

Docs for `lyricsgenius` library: https://lyricsgenius.readthedocs.io/en/master/index.html

Created: October 2025 by Oscar Reza B.
'''

from lyricsgenius import Genius
from lyricsgenius.types import Song
import pandas as pd

from constants import GENIUS_KEY

def get_songs_from_artist(genius: Genius, artist_name: str) -> list[Song]:
    '''
    Gets the list of songs from a given artist, searching in the Genius API

    :param lyricsgenius.Genius genius: the initialized Genius object from the lyricsgenius library
    :param str artist_name: the name of the artist to get the songs from
    :return: list of artist songs
    :rtype: list[Song]
    '''
    artist = genius.search_artist(artist_name=artist_name, max_songs=2)
    assert artist is not None

    return artist.songs

def songs_to_csv(songs: list[Song], output_csv: str) -> None:
    '''
    Saves the input list of song objects into the given csv path.

    :param list[Song] songs: the list of song objects to save into a csv
    :param str output_csv: the path to the output_csv
    '''
    song_data = []  # array to load data

    for song in songs:
        # Load album separately to handle special cases
        album = song.album
        album_name = album.get('name') if album is not None else song.artist  # handle undefined album
        # Load data into the array
        song_data.append({
            "title": song.title,
            "artist": song.artist,
            "album": album_name,
            "album_image": song.header_image_url,
            "lyrics": song.lyrics,
        })

    # Put data into dataframe
    df = pd.DataFrame(data=song_data)
    # Save to csv. A file with headers should already exist
    df.to_csv(output_csv, index=False, mode='a', header=False)

    # Confirmation messages
    print(f"Data has been saved in {output_csv}")
    print(f"Successfylly extracted {len(df.index)} songs")

if __name__ == "__main__":
    # Test with ALEXSUCKS and Surf Curse
    artists: list[str] = ["ALEXSUCKS", "Surf Curse"]
    # Initialize Genius API using access token
    genius = Genius(GENIUS_KEY)

    for artist in artists:
        # Get the list of songs from a given artist
        songs = get_songs_from_artist(genius, artist)
        # Load all artist's songs into a CSV
        songs_to_csv(songs, "res/alexsucks_and_surf_curse_genius_test_oct_30.csv")