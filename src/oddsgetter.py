import pandas as pd
import json
import os
import requests
import time

RACE_URL_STUMP = "https://www.veikkaus.fi/api/toto-info/v1/race/"
POOL_URL_STUMP = "https://www.veikkaus.fi/api/toto-info/v1/pool/"
RUNNER_FILE = "data/runners.csv"
DATA_FOLDER = "data/odds/"

s_time = time.time()
print("reading existing data...")
df = pd.read_csv(RUNNER_FILE)
races = df.raceId.unique()
n = str(len(races))
existing_odds_data = [f[:-4] for f in os.listdir(DATA_FOLDER)]
print("existing data read!")
print("\ttime elapsed: " + str(time.time() - s_time))

i = 0
s_time = time.time()
for race in races:
    race_string = str(race)
    if race_string not in existing_odds_data:
        pools = requests.get(RACE_URL_STUMP + race_string + "/pools")
        parsed = json.loads(pools.text)
        

        if 'collection' not in parsed.keys():
            print("SHITS FUCKED: " + race_string)
        else:
            poolsdf = pd.DataFrame(parsed['collection'])
            if 'poolId' in poolsdf:
                odds_arr = []
                timestamp_arr = []
                for pid in poolsdf.poolId.values:
                    odds = requests.get(POOL_URL_STUMP + str(pid) + "/odds")
                    odds_parsed = json.loads(odds.text)
                    odds_arr.append(str(odds_parsed['odds']))
            
                poolsdf['odds_dump'] = odds_arr
                poolsdf.to_csv(DATA_FOLDER + race_string + ".csv")
            else:
                print("no pools: " + race_string)

    i += 1
    if i % 1000 == 0:
        print(str(i) + "/" + n)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()
