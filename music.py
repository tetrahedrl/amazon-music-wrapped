import pandas
import csv
with open('Amazon-Music/listening.csv','r',encoding="utf8") as f:
    reader = csv.reader(f)
    listening = {}
    artists = {}
    count = {}
    reader.__next__()
    for row in reader:
        try:
            if row[1] not in listening:
                if len(row[10]) == 0:
                    continue
                listening[row[1]] = 0
                artists[row[1]] = row[10]
                count[row[1]] = 0
            if '2023' in row[0]:
                listening[row[1]] += int(row[3])
                count[row[1]] += 1
        except Exception as e:
            print(e)
with open('Amazon-Music/library.csv','r',encoding='utf-8') as f:
    reader = csv.reader(f)
    artists_dict = {row[16]:row[15] for row in reader}
    genre_dict = {row[5]:row[19] for row in reader}
dictionary = {'name':[song for song in listening],'artist':[artists[song] for song in listening],'listeningms':[listening for listening in listening.values()],'count':[count for count in count.values()]}
df = pandas.DataFrame(dictionary).sort_values(by='listeningms')
df.artist = df.artist.apply(lambda x: artists_dict[x] if x in artists_dict else None)
df.assign(genre=genre_dict[df.asin])
print(df)
print(df.sort_values(by='count'))
a = df.groupby(by='artist')['listeningms'].sum().sort_values()
print(a.keys())