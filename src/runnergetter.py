import pandas as pd
import json
import os
import requests
import time

RACE_DATA_FOLDER = "data/races/"
RUNNER_DATA_FOLDER = "data/runners/"

URL_STUMP = "https://www.veikkaus.fi/api/toto-info/v1/race/"

print("reading existing data...")
races = [x.split('.')[0] for x in os.listdir(RACE_DATA_FOLDER)]
existing_runner_data = os.listdir(RUNNER_DATA_FOLDER)
print("existing data read!")

i = 0
s_time = time.time()
for race in races:
    if race not in existing_runner_data:
        df = pd.read_csv(RACE_DATA_FOLDER + race + ".csv")
        os.mkdir(os.path.join(RUNNER_DATA_FOLDER, race))

        for rid in df.raceId.values:
            get = requests.get(URL_STUMP + str(rid) + "/runners")
            parsed = json.loads(get.text)
            rdf = pd.DataFrame(parsed['collection'])
            rdf.to_csv(RUNNER_DATA_FOLDER + race + "/" + str(rid) + ".csv")
            
    i += 1
    if i % 200 == 0:
        print(str(i) + "/" + str(len(races)))
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()
