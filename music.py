import pandas
import numpy as np
df = pandas.read_csv('Amazon-Music/listening.csv')
df = df[['2023' in timestamp for timestamp in df.timestamp.values]]
def first_str (x):
    strs = x.values[[isinstance(y,str) for y in x.values]]
    if len(strs):
        return strs[0]
    else:
        return None
    
df = df.groupby(by='asin',as_index=False).agg({
    'title': first_str,
    'consumptionDurationMs':'sum',
    'artistAsin': first_str
})
library_df = pandas.read_csv('Amazon-Music/library.csv')
artists_dict = {row['artistAsin']:row['artistName'] for i,row in library_df.iterrows()}
genre_dict = {row['asin']:row['primaryGenre'] for i,row in library_df.iterrows()}
df = df.assign(genre=[genre_dict.get(asin) for asin in df.asin],artist=[artists_dict.get(asin) for asin in df.artistAsin])
df = df.sort_values(by='consumptionDurationMs')
df[['title','artist','genre','consumptionDurationMs']].to_csv('top_songs.csv')
sum_by_artist = df.groupby(by='artist',as_index=False).agg({
    'consumptionDurationMs':'sum'
})
sum_by_artist.sort_values(by='consumptionDurationMs').to_csv('top_artists.csv')
sum_by_genre = df.groupby(by='genre',as_index=False).agg({
    'consumptionDurationMs':'sum'
})
sum_by_genre.sort_values(by='consumptionDurationMs').to_csv('top_genres.csv')