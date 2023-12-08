import pandas
import csv
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
with open('Amazon-Music/library.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    artists_dict = {row[16]:row[15] for row in reader}
    genre_dict = {row[5]:row[19] for row in reader}
df = df.assign(genre=[genre_dict.get(asin) for asin in df.asin],artist=[artists_dict.get(asin) for asin in df.artistAsin])
df = df.sort_values(by='consumptionDurationMs')
print(df[['title','artist','genre','consumptionDurationMs']])