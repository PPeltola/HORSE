import pandas as pd
import time

# Add card data to races.csv

RACE_CSV = "data/races.csv"
CARD_CSV = "data/cards.csv"

print("reading existing data...")
s_time = time.time()
race_df = pd.read_csv(RACE_CSV)
card_df = pd.read_csv(CARD_CSV)
print("existing data read!")
print("\ttime elapsed: " + str(time.time() - s_time) + "\n")
s_time = time.time()

card_vals = {
    'cancelled': [],
    'country': [],
    'currentRaceNumber': [],
    'currentRaceStatus': [],
    'lunchRaces': [],
    'meetDate': [],
    'priority': [],
    'raceType': [],
    'trackAbbreviation': [],
    'trackName': [],
    'trackNumber': [],
    'mainPerformance': [],
    'date': [],
    'lastRaceOfficial': [],
    'currentRaceStartTime': [],
    'firstRaceStart': []
}

n = str(len(race_df))
i = 0
for cid in race_df['cardId']:
    card = card_df.query('cardId == ' + str(cid))

    for (val, arr) in card_vals.items():
        arr.append(card[val].values[0])

    i += 1
    if i % 1000 == 0:
        print(str(i) + "/" + n)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

for (val, arr) in card_vals.items():
    race_df.insert(len(race_df.columns), val, arr)

race_df.to_csv("data/races2.csv")