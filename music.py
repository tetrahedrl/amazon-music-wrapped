import pandas
import numpy as np

def first_str (series):
    for element in series:
        if isinstance(element,str):
            return element
    return None

def get_genres (df):
    genres = []
    for index, row in df[['asin','artistAsin']].iterrows():
        if row['asin'] in song_genre_dict:
            genres.append(song_genre_dict[row['asin']])
            continue
        elif row['asin'] in album_genre_dict:
            genres.append(album_genre_dict[row['asin']])
            continue
        elif row['artistAsin'] in artist_album_genre_dict and artist_album_genre_dict[row['artistAsin']] is not None:
            genres.append(artist_album_genre_dict[row['artistAsin']])
        else:
            genres.append(artist_song_genre_dict.get(row['artistAsin']))
    return genres

def pick_primary (series):
    mode = series.mode()
    if not len(mode):
        return None
    return mode[0]
        
df = pandas.read_csv('Amazon-Music/listening.csv')
df = df[['2023' in timestamp for timestamp in df.timestamp.values]]    
df = df.groupby(by='asin',as_index=False).agg({
    'title': first_str,
    'artistAsin': first_str,
    'consumptionDurationMs':'sum',
    'terminationReason': lambda x: dict(x.value_counts(sort=False))
})
library_df = pandas.read_csv('Amazon-Music/library.csv')
artists_dict = {row['artistAsin']:row['artistName'] for i,row in library_df.iterrows()}
song_genre_dict = {row['asin']:row['primaryGenre'] for i,row in library_df.iterrows() if not ((not isinstance(row['primaryGenre'],str)) and np.isnan(row['primaryGenre']))}
album_genre_dict = {row['asin']:row['albumPrimaryGenre'] for i,row in library_df.iterrows() if not ((not isinstance(row['albumPrimaryGenre'],str)) and np.isnan(row['albumPrimaryGenre']))}
artist_song_genre_dict = library_df.groupby(by='artistAsin').agg({'primaryGenre':pick_primary}).to_dict()['primaryGenre']
artist_album_genre_dict = library_df.groupby(by='artistAsin').agg({'albumPrimaryGenre':pick_primary}).to_dict()['albumPrimaryGenre']
df = df.assign(
    genre=get_genres(df),
    artist=[artists_dict.get(asin) for asin in df.artistAsin],
    starts=[sum(reason_dict.values()) for reason_dict in df.terminationReason],
    finishes=[reason_dict.get('trackFinished') for reason_dict in df.terminationReason]
    )
df = df.sort_values(by='consumptionDurationMs')
df[['title','artist','genre','consumptionDurationMs','starts','finishes']].to_csv('out/top_songs.csv')
sum_by_artist = df.groupby(by='artist',as_index=False).agg({
    'consumptionDurationMs':'sum'
})
sum_by_artist.sort_values(by='consumptionDurationMs').to_csv('out/top_artists.csv')
sum_by_genre = df.groupby(by='genre',as_index=False).agg({
    'consumptionDurationMs':'sum'
})
sum_by_genre.sort_values(by='consumptionDurationMs').to_csv('out/top_genres.csv')
print('total listening time: {}ms'.format(df.consumptionDurationMs.sum()))