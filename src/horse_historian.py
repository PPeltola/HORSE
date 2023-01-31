import pandas as pd
import os
import time

#RACE_CSV = "/home/pp/Documents/HORSE_DATA/data/fintracks_putsis.csv"
#RACE_CSV = "/home/pp/Documents/HORSE_DATA/data/fintracks_sample4.csv"
RUNS_CSV = "/home/pp/Documents/HORSE_DATA/data/fintracks_runners.csv"

RACE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/runners/"

#SAVE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/horses_test"
SAVE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/horses3"

PREV_RUN_NAME = "new13"



#all_races_df = pd.read_csv(RACE_CSV)

all_runs = pd.read_csv(RUNS_CSV)
all_horses = []

with open("/home/pp/Documents/HORSE_DATA/data/heppalista.txt", "r") as f:
    for h in f.readlines():
        all_horses.append(h.strip())

j = 0
s_time = time.time()

for horse in all_horses:
    if os.path.exists(SAVE_FOLDER + "/" + horse + ".csv"):
        continue

    horse_df = all_runs[all_runs['horseString'] == horse]
    horse_df.to_csv(SAVE_FOLDER + "/" + horse + ".csv")

    j += 1
    if j % 1000 == 0:
        print(j)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()


"""
for i, row in all_races_df.iterrows():
    cid = row['cardId']
    rid = row['raceId']

    race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "_elo/" + str(rid) + "_elo.csv")

    #for hs in race_df['horseString'].values:
    #    all_horses.add(hs)

    j += 1
    if j % 10000 == 0:
        print(j)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

"""