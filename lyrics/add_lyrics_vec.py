import pandas as pd
import numpy as np

lyrics_df = pd.read_csv('res/vectorized-lyrics.csv')
lyrics_np = lyrics_df.to_numpy()
gems_df = pd.read_csv('res/indie-gems.csv')

gems_df['lyrics_vec'] = [lyrics_np[i] for i in range(len(gems_df.index))]

fixed_df = gems_df.drop('Unnamed: 0',axis=1).drop('lyrics',axis=1)  # remove the lyrics column and the other extra column 
fixed_df.insert(0, 'song_id', fixed_df.index)

print(type(fixed_df.get('lyrics_vec')[0]))

# print(fixed_df)
# fixed_df.to_csv('workable-dataset.csv', index=False)  # this saves the final csv
fixed_df.to_pickle('workable-dataset.pkl')  # this saves the final pickle