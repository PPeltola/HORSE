import numpy as np
import pandas as pd
import os
import time

#df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/temp_test1.csv")
df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_frankenstein.csv")

def form_res_string(frame):
    data = frame.sort_values(by=['Sijoitus'])
    finishes = {k: [] for k in frame['Sijoitus'].dropna().sort_values().unique()}
    dnf = []

    for i, row in data.iterrows():
        p = row['Sijoitus']
        n = row['startNumber']

        if np.isnan(p):
            dnf.append(str(n))
        else:
            finishes[p].append(str(n))

    res = ""

    for k, fs in finishes.items():
        if len(fs) > 1:
            finishes[k] = "(" + ",".join(fs) + ")"
        elif len(fs) == 1:
            finishes[k] = fs[0]

    res += "-".join(finishes.values())

    if len(dnf) > 1:
        res += "-(" + ",".join(dnf) + ")"
    elif len(dnf) == 1:
        res += "-" + dnf[0]

    return res

def alt_form_res_string(frame):
    frame['parsedPalkinto'] = frame['Palkinto'].map(lambda l: 0 if isinstance(l, float) else int(l[:-2].replace(u'\xa0', "")))
    data = frame.sort_values(by=['parsedPalkinto', 'Sijoitus'], ascending=[False, True])
    
    finishes = {k: {} for k in frame['Sijoitus'].dropna().sort_values().unique()}
    dnf = []

    for i, row in data.iterrows():
        placement = row['Sijoitus']
        num = row['startNumber']
        prize = row['parsedPalkinto']

        if np.isnan(placement):
            dnf.append(str(num))
        else:
            finishes[placement][str(num)] = prize

    res = ""

    for k, fs in finishes.items():
        vals = list(fs.values())
        if len(vals) > 1:
            pzs = vals.copy()
            if all(x == pzs[0] for x in pzs):
                finishes[k] = "(" + ",".join(list(fs.keys())) + ")"

            else:
                legit = []
                for n, pz in fs.items():
                    if pz == 0:
                        dnf.append(str(n))
                    else:
                        legit.append(str(n))

                if len(legit) > 1:
                    finishes[k] = "(" + ",".join(legit) + ")"
                elif len(legit) == 1:
                    finishes[k] = legit[0]
            

        elif len(vals) == 1:
            finishes[k] = str(list(fs.keys())[0])
    
    res += "-".join(finishes.values())

    if len(dnf) > 1:
        res += "-(" + ",".join(dnf) + ")"
    elif len(dnf) == 1:
        res += "-" + dnf[0]

    return res
    
RUNNER_PATH = "/home/pp/Documents/HORSE_DATA/data/runners/"
HEPPA_FOLDER = "heppa5"

k = 0
s_time = time.time()

#df = df.iloc[103000:]

for i, row in df.iterrows():
    #if k < 5000:
    #    k += 1
    #    continue
    
    rid = str(row['raceId'])
    cid = str(row['cardId'])

    if os.path.exists(RUNNER_PATH + cid + "/" + HEPPA_FOLDER + "/" + rid + "_heppa.csv"):
        race_df = pd.read_csv(RUNNER_PATH + cid + "/" + HEPPA_FOLDER + "/" + rid + "_heppa.csv")
        df.loc[i, 'heppaOriginalResults'] = form_res_string(race_df)
        df.loc[i, 'heppaAdjustedResults'] = alt_form_res_string(race_df)
    else:
        print("MISS: " + RUNNER_PATH + cid + "/" + HEPPA_FOLDER + "/" + rid + "_heppa.csv")

    k += 1
    if k % 1000 == 0:
        print(k)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

df.to_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_frankenhorse.csv")