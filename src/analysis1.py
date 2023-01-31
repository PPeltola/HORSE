import numpy as np
import pandas as pd
import time

df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_putsis.csv")

handicap_races = 0
non_hc_races = 0

#handicap races vs non-handicap races
#41829 vs 62580: ~40%

RACE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/runners/"
LATEST_RUNNER_FOLDER = "new11"

s_time = time.time()
tot_time = time.time()

handicaps = {}
handicap_placement_sums = {}

for i, row in df.iterrows():
    cid = row['cardId']
    rid = row['raceId']

    race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + LATEST_RUNNER_FOLDER + "_elo/" + str(rid) + "_elo.csv")

    min_d = np.min(race_df['Matka'])
    max_d = np.max(race_df['Matka'])

    if min_d != max_d:
        handicap_races += 1
        
        for j, r2 in race_df.iterrows():
            amt = r2['Matka'] - min_d
            placement = r2['Sijoitus']
            #if amt > 0:
            if not np.isnan(placement):
                handicaps[amt] = handicaps.get(amt, 0) + 1
                handicap_placement_sums[amt] = handicap_placement_sums.get(amt, 0) + placement

    else:
        non_hc_races += 1


    if (int(i)) % 10000 == 0:
        print(i)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()


print(handicap_races)
print(non_hc_races)
print()
print(handicaps)
print(handicap_placement_sums)
print()

for k in handicaps.keys():
    print(k)
    print(handicap_placement_sums[k] / handicaps[k])
    print()

print("\n\ttotal time: " + str(time.time() - tot_time))