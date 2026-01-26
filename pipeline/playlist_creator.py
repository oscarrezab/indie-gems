'''
Create a playlist with all songs from all artist of interest in Spotify.

Pre-requisites: 
- A developer account for the Spotify Web API. In this code, the authentication variables are 
REDIRECT_URI, SPOTIFY_CLIENT, SPOTIFY_SECRET, and SPOTIFY_USER.
- A dictionary that maps the names of artist of interest and their respective Spotify
ID. In this case, this variable is called ARTIST_OF_INTEREST.

Docs for the `spotipy` library: https://spotipy.readthedocs.io/

Created: October 2025 by Oscar Reza B.
'''

from constants import ARTISTS_OF_INTEREST, REDIRECT_URI, SPOTIFY_CLIENT, SPOTIFY_SECRET, SPOTIFY_USER
import spotipy
from spotipy.oauth2 import SpotifyOAuth


def get_albums(sp: spotipy.Spotify, artist_id: str) -> list[str]:
    '''
    Get all albums for a given artist.

    :param spotipy.Spotify sp: the authenticated spotipy client.
    :param str artist_id: the Spotify ID for the given artist
    :return: the list of IDs for all albums by the given artist
    :rtype: list[str]
    '''
    res = sp.artist_albums(artist_id)
    assert res is not None
    artist_albums = res['items']
    album_ids = []
    for album in artist_albums:
        # Fetch only albums that were directly published by the artist of interest (i.e., not 'appears on')
        if album['album_group'] != 'appears_on':
            album_ids.append(album['id'])
    return album_ids


def get_songs_from_album(sp: spotipy.Spotify, album_id: str) -> list[str]:
    '''
    Get all songs for a given album.

    :param spotipy.Spotify sp: the authenticated spotipy client.
    :param str album_id: the Spotify ID for the given album
    :return: the list of IDs for all songs in the given album
    :rtype: list[str]
    '''
    res = sp.album_tracks(album_id)
    assert res is not None
    tracks = res['items']
    track_ids = []
    for track in tracks:
        track_ids.append(track['id'])
    return track_ids


def create_playlist(sp: spotipy.Spotify, playlist_name: str, playlist_description: str= "") -> tuple[str, str]:
    '''
    Creates an empty Spotify playlist with the given name and description.

    :param spotipy.Spotify sp: the authenticated spotipy client.
    :param str playlist_name: the name of the playlist to create
    :param str playlist_description: the description of the playlist to create (defaults to empty string)
    :return: a tuple (playlist_id, playlist_name)
    :rtype: tuple[str,str]
    '''
    sp.user_playlist_create(user= SPOTIFY_USER, 
                            name=playlist_name, 
                            public=True, 
                            collaborative=False, 
                            description=playlist_description)
    res = sp.user_playlists(SPOTIFY_USER, limit=2)
    assert res is not None
    user_playlists: list[dict] = res["items"]
    for playlist in user_playlists:
        if playlist.get('name') == playlist_name:
            playlist_id = playlist.get('id')
            assert playlist_id is not None
            return playlist_id, playlist_name
    return "Failed to create playlist", "Failed to create playlist"


def add_songs(sp: spotipy.Spotify, playlist_id: str, song_ids: list[str]) -> None:
    '''
    Adds the given list of songs to a Spotify playlist.

    :param spotipy.Spotify sp: the authenticated spotipy client.
    :param str playlist_id: the Spotify ID for the playlist to add songs to
    :param list[str] song_ids: the list of IDs of songs to add to the playlist
    '''
    sp.playlist_add_items(playlist_id, song_ids)
    print(f"Added {len(song_ids)} songs to the playlist {playlist_id}")
    
    
if __name__ == "__main__":
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id= SPOTIFY_CLIENT,
                                                client_secret= SPOTIFY_SECRET,
                                                redirect_uri= REDIRECT_URI,
                                                scope="playlist-modify-public"))
    # Create empty playlist
    created_playlist_id, created_playlist_name = create_playlist(sp, "all-test-auto", "for testing purposes")
    assert created_playlist_id is not None

    print(f"Created playlist {created_playlist_name} with id {created_playlist_id}")  # success message

    # Get artist albums
    for artist in ARTISTS_OF_INTEREST.keys():
        artist_id = ARTISTS_OF_INTEREST[artist]
        artist_albums = get_albums(sp, artist_id) 

        # Loop through every album id
        for album_id in artist_albums:
            # Get track ids in album
            track_ids = get_songs_from_album(sp, album_id)
            # Add songs to playlist
            add_songs(sp, created_playlist_id, track_ids)
        
        print(f"Added all songs from {artist} into {created_playlist_name}")  # success message



