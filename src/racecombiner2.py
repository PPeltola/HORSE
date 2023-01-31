import pandas as pd
import os
import time

RACE_CSV = "/home/pp/Documents/HORSE_DATA/data/fintracks_putsis.csv"
#RACE_CSV = "/home/pp/Documents/HORSE_DATA/data/fintracks_sample4.csv"

RACE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/runners/"

#SAVE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/horses_test"
#SAVE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/horses3"

PREV_RUN_NAME = "new13"

race_vals = [
    "name",
    "seriesSpecification",
    "raceStatus",
    "startType",
    "monte",
    "firstPrize",
    "distance",
    "breed",
    "reserveHorsesOrder",
    "lunchRaces",
    "meetDate",
    "priority",
    "trackAbbreviation",
    "trackName",
    "trackNumber",
    "mainPerformance",
    "date",
    "timestamp",
    "heppaLink",
    "Voittaja_kertoimet",
    "Voittaja_vaihdot",
    "Sija_kertoimet",
    "Sija_vaihdot",
    "Kaksari_kertoimet",
    "Kaksari_vaihdot",
    "Lähtövaihto_kertoimet",
    "Lähtövaihto_vaihdot",
    "yleisoa",
    "lampotila",
    "radan_kunto",
    "V4_kertoimet",
    "V4_vaihdot",
    "Päivän duo_kertoimet",
    "Päivän duo_vaihdot",
    "Troikka_kertoimet",
    "Troikka_vaihdot",
    "[RACERESULTSTEXT_NELIVETO]_kertoimet",
    "[RACERESULTSTEXT_NELIVETO]_vaihdot",
    "V75_kertoimet",
    "V75_vaihdot",
    "V5_kertoimet",
    "V5_vaihdot",
    "Toto5_voitto-osuudet",
    "Toto5_vaihdot",
    "Toto4_voitto-osuudet",
    "Toto4_vaihdot",
    "heppaOriginalResults",
    "heppaAdjustedResults"
]

all_races_df = pd.read_csv(RACE_CSV)
frames = []

i = 0
s_time = time.time()

for j, row in all_races_df.iterrows():
    if i <= 50000:
        i += 1
        continue

    cid = row['cardId']
    rid = row['raceId']
    race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "_elo/" + str(rid) + "_elo.csv")

    for k in race_vals:
        race_df[k] = row[k]

    frames.append(race_df)

    i += 1
    if i % 1000 == 0:
        print(i)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

print("combining frames...")
s_time = time.time()
df = pd.concat(frames)
df.to_csv("fintracks_runners_2.csv")
print("\ttime elapsed: " + str(time.time() - s_time))
