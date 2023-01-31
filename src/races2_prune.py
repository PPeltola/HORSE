import numpy as np
import pandas as pd
#import time

RACE_CSV = "data/races2_sorted+pruned4.csv"

BAD_RACES = "huh.txt"



df = pd.read_csv(RACE_CSV)

"""
bad_rids = []

with open(BAD_RACES) as f:
    for rid in f:
        bad_rids.append(int(rid))

bads = df[df['raceId'].isin(bad_rids)]
goods = df[~df['raceId'].isin(bad_rids)]

goods.to_csv("data/races2_sorted+pruned4.csv")
#bads.to_csv("data/bad_short_res.csv")
"""
# --------



#df.sort_values(by=['date', 'trackName', 'number'], inplace=True)


l = len(df)
print("Initial df length:")
print(l)
print()



l = len(df)
#print(df['refererRace'])
#bdf = df[~df['refererRace'].isna()]
#bdf.to_csv("referers.csv")

df = df[df['refererRace'].isna()]
#df.dropna(subset=['toteResultString'], inplace=True)

#print("Amount of empty results dropped:")
print(l - len(df))
l = len(df)

#df.drop_duplicates(subset=["date", "breed", "country", "toteResultString", "firstPrize", "distance"], inplace=True)
df.drop_duplicates(subset=["date", "breed", "country", "toteResultString", "firstPrize", "distance", "startType", "monte", "raceRider", "trackSurface", "trackProfile"], inplace=True)

print("Amount of duplicates dropped:")
print(l - len(df))
print()

#xdf = df[df.duplicated(subset=["date", "breed", "country", "toteResultString", "firstPrize", "distance", "startType", "monte", "raceRider", "trackSurface", "trackProfile"])]
#xdf.to_csv("duplicates.csv")

df.to_csv("data/races2_sorted+pruned5.csv")