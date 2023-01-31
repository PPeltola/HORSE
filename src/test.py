import numpy as np
import pandas as pd
import json
import os
import requests
import time
import shutil

"""
RACE_CSV = "data/races2_sorted+pruned.csv"

df = pd.read_csv(RACE_CSV)

print(df['startType'].unique())

print(len(df[df['startType'] == 'OFFICIAL']))
print(len(df[df['startType'] == 'HURDLES']))
print(len(df[df['startType'] == 'FLAT']))
print(len(df[df['startType'] == 'UNKNOWN']))
print(len(df[df['startType'] == 'JUMPS']))

df['startType'].replace(['OFFICIAL', 'HURDLES', 'JUMPS', 'UNKNOWN'], np.nan, inplace=True)
df.dropna(subset=['startType'], inplace=True)

print(df['startType'].unique())

df.to_csv("data/races2_sorted+pruned2.csv")
#print(df[df['startType'] == 'OFFICIAL'])
"""

#print("2-1-3/9".replace("/", ","))
#print("2-(1,3)".strip("()"))
#print("2-(1,3)".replace(")", "").replace("(", ""))

#data = json.load(open("final_elo_dump.json"))
#print(type(data.values()))

"""
N = 200663
a = {3: 22, 4: 175, 5: 685, 6: 1564, 7: 2761, 8: 4090, 9: 5534, 10: 8015, 11: 10820, 12: 10878, 13: 2293, 14: 2835, 15: 2786, 16: 1146, 17: 1, 18: 0, 19: 1, 20: 1, 22: 0, 29: 0, 30: 1}
b = {3: 17, 4: 235, 5: 944, 6: 2519, 7: 5100, 8: 8311, 9: 12560, 10: 20397, 11: 30353, 12: 32687, 13: 7809, 14: 10445, 15: 10946, 16: 4728, 17: 0, 18: 1, 19: 0, 20: 1, 22: 1, 29: 1, 30: 0}

r = 0.0


for i in a.keys():
    if i >= 17:
        continue

    t = a[i] + b[i]
    #print(str(i) + ": " + str(t) + "\t" + str(a[i] / t) + "\t" + str(t/N) + "\t" + str((t/N) * (a[i] / t)))
    #r += (t / N) * ((i - 1) / i)
    r += (t/N) * (3 / i)

print()
print(r)
"""

# remove useless data from runner folders

"""
#df = pd.read_csv("data/races2_sorted+pruned5.csv")
df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed3.csv")

tobedeleted = ['alt8_elo', 'new8_2_elo', 'new8_3_elo', 'new8_elo', 'new9_elo', 'new10_elo', 'new11_elo', 'new12_elo', 'new_flat15_2_elo', 'new_flat15_elo']

for i, row in df.iterrows():
    cid = row['cardId']
    rid = row['raceId']
    
    for d in tobedeleted:
        p = "/home/pp/Documents/HORSE_DATA/data/runners/" + str(cid) + "/" + d
        if os.path.exists(p):
            shutil.rmtree(p)
            
    if int(i) % 10000 == 0:
        print(str(i))
"""


# drop bad fin races (mostly dupes)
"""
stein = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_frankenhorse.csv")
bigone = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races2_sorted+pruned5.csv")

fins = bigone[bigone['country'].str.lower() == 'fi']
fin_rejects = fins[~fins['raceId'].isin(stein['raceId'])]

#print(fin_rejects.shape)
#fin_rejects.to_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_rejects.csv")

#print(bigone.shape)
bigone = bigone[~bigone['raceId'].isin(fin_rejects['raceId'])]
#print(bigone.shape)

bigone.to_csv("/home/pp/Documents/HORSE_DATA/data/races3.csv")
"""

# join heppa merged df to the big one
"""
stein = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_frankenhorse.csv")
bigone = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3.csv")

combo = bigone.join(stein.set_index('raceId'), on='raceId', rsuffix='_fs')

combo.to_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed.csv")
"""

# drop cols from big frame
"""
df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed.csv")
print(df.shape)

to_drop = ['Unnamed: 0.13', 'Unnamed: 0.6', 'Unnamed: 0.5', 'Unnamed: 0.4', 
'Unnamed: 0.3', 'Unnamed: 0.2', 'Unnamed: 0.1', 'Unnamed: 0', 'Unnamed: 0.12', 
'Unnamed: 0.11', 'Unnamed: 0.10', 'Unnamed: 0.9', 'Unnamed: 0.8', 'Unnamed: 0.7', 
'Unnamed: 0.6_fs', 'Unnamed: 0.5_fs', 'Unnamed: 0.4_fs', 'Unnamed: 0.3_fs', 
'Unnamed: 0.2_fs', 'Unnamed: 0.1_fs', 'Unnamed: 0_fs', 'cardId_fs', 'number_fs', 
'name_fs', 'seriesSpecification_fs', 'raceStatus_fs', 'startType_fs', 'monte_fs', 
'firstPrize_fs', 'startTime_fs', 'toteResultString_fs', 'raceRecord_fs', 'raceClass_fs', 
'raceRider_fs', 'trackProfile_fs', 'trackSurface_fs', 'distance_fs', 'breed_fs', 
'intermediateTimesString_fs', 'reserveHorsesOrder_fs', 'refererRace_fs', 'cancelled_fs', 
'country_fs', 'currentRaceNumber_fs', 'currentRaceStatus_fs', 'lunchRaces_fs', 'meetDate_fs', 
'priority_fs', 'raceType_fs', 'trackAbbreviation_fs', 'trackName_fs', 'trackNumber_fs', 
'mainPerformance_fs', 'date_fs', 'lastRaceOfficial_fs', 'currentRaceStartTime_fs', 'firstRaceStart_fs']

df = df.drop(columns=to_drop)
print(df.shape)
df.to_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed2.csv")



#df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races.csv")
df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed2.csv")
df['heppaAdjustedResults'] = df['heppaAdjustedResults'].astype(str)
print(sum(df['heppaAdjustedResults'] == "nan"))

rej_df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_rejects.csv")
print(sum(df['raceId'].isin(rej_df['raceId'])))
# so these were already removed after all

#for i, row in df.iterrows():
#    print(type(row['heppaAdjustedResults']))
"""

"""
df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed2.csv")
#sample_df = df.sample(5)
#sample_df.to_csv("horsed_sample5.csv")
df['heppaAdjustedResults'] = df['heppaAdjustedResults'].astype(str)
df['heppaOriginalResults'] = df['heppaOriginalResults'].astype(str)

df.to_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed3.csv")
#import math

#print(math.isnan("hello"))

df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed3.csv")
print(df.shape)
df.dropna(subset=['heppaAdjustedResults'], inplace=True)
df.to_csv("fintracks_putsis.csv")
"""

#df2 = pd.read_csv("fintracks_runners_2.csv")
#df1 = pd.read_csv("fintracks_runners1_fixed.csv")
#df = pd.concat([df1, df2])

#print(df1['coachNameInitials'].unique())
#df.to_csv("fintracks_runners_fixed.csv")

"""
inds = []
for i, row in df1.iterrows():
    
    if isinstance(row['coachNameInitials'], float):
        inds.append(i)
        print("\t" + str(i))

    if i % 100000 == 0:
        print(i)


print(inds)
xdf = pd.DataFrame(df1.iloc[inds])
#print(df1.iloc[[1, 2]])
#print(xdf)
ndf = df1.drop(inds)
ndf.to_csv('not_faulty2.csv')
xdf.to_csv('faulty2.csv')
"""

df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_runners_fixed.csv")
df.sort_values(by=['timestamp', 'raceId', 'startNumber'], inplace=True)
df.to_csv("fintracks_runners_sorted.csv")
print(df.shape)


#df2 = pd.read_csv("fintracks_runners_2.csv")

#df = pd.concat([df1, df2])