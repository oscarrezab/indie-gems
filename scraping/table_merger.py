'''
Info for recommendation:
- Song name, artist, and album cover
- Lyrics
- Camelot (in place of key)
- BPM

Info for evaluation (other data that might be interesting)
- Popularity
- Energy
- Acousticness
- Album Date
'''

import pandas as pd

# Load csv files
song_list_one = pd.read_csv("res/indie-test-1.csv")
song_list_two = pd.read_csv("res/indie-test-2.csv")

lyrics_list_one = pd.read_csv("res/indie-test-1-lyrics.csv")
lyrics_list_two = pd.read_csv("res/indie-test-2-lyrics.csv")

chosic_list_one = pd.read_csv("res/indie-test-1-chosic.csv")
chosic_list_two = pd.read_csv("res/indie-test-2-chosic.csv")

titles = pd.concat([song_list_one.get('title'), song_list_two.get('title')], ignore_index=True)
artists = pd.concat([song_list_one.get('artist'), song_list_two.get('artist')], ignore_index=True)
albums = pd.concat([song_list_one.get('album'), song_list_two.get('album')], ignore_index=True)
album_imgs = pd.concat([song_list_one.get('album_image'), song_list_two.get('album_image')], ignore_index=True)
bpms = pd.concat([chosic_list_one.get('BPM'), chosic_list_two.get('BPM')], ignore_index=True)
camelots = pd.concat([chosic_list_one.get('Camelot'), chosic_list_two.get('Camelot')], ignore_index=True)
lyrics = pd.concat([lyrics_list_one.get('lyrics'), lyrics_list_two.get('lyrics')], ignore_index=True)

merged_df = pd.concat([titles, artists, albums, album_imgs, bpms, camelots, lyrics], axis=1)

merged_df.to_csv("full-dataset.csv")
# print(merged_df)

