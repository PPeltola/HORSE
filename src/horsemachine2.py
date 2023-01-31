import pandas as pd
import os
import time

RACE_CSV = "data/races.csv"
CARD_CSV = "data/cards.csv"
DATA_FOLDER = "data/horses/"
SAVE_FOLDER = "data/horses2/"

#ODDS_FOLDER = "data/odds/"
#MOCK_HORSES = ["Estelle Brodda* (SE)"]

# This script will combine the invidual horse data (i. e. recorded races)
# with the race + card data (i. e. location, results, date, etc.) of the races

print("reading existing data...")
s_time = time.time()
existing_horses = [x[:-4] for x in os.listdir(DATA_FOLDER)]
race_df = pd.read_csv(RACE_CSV)
card_df = pd.read_csv(CARD_CSV)
print("existing data read!")
print("\ttime elapsed: " + str(time.time() - s_time) + "\n")
s_time = time.time()

n = str(len(existing_horses))
i = 0

for horse in existing_horses:
#for horse in MOCK_HORSES:
    df = pd.read_csv(DATA_FOLDER + horse.replace("/", "_") + ".csv")

    race_vals = {
        'cardId': [],
        'number': [],
        'name': [],
        'seriesSpecification': [],
        'raceStatus': [],
        'startType': [],
        'monte': [],
        'firstPrize': [],
        'startTime': [],
        'toteResultString': [],
        'raceClass': [],
        'raceRider': [],
        'trackProfile': [],
        'trackSurface': [],
        'distance': [],
        'breed': [],
        'intermediateTimesString': [],
        'reserveHorsesOrder': []
    }

    card_vals = {
        'cancelled': [],
        'country': [],
        'currentRaceNumber': [], #
        'currentRaceStatus': [], #
        'lunchRaces': [],
        'meetDate': [],
        'priority': [],
        'raceType': [],
        'trackAbbreviation': [],
        'trackName': [],
        'trackNumber': [],
        'mainPerformance': [], # Huh?
        'date': [],
        'lastRaceOfficial': [], #
        'currentRaceStartTime': [], #
        'firstRaceStart': [] #
    }

    for rid in df['raceId'].values:
        race = race_df.query('raceId == ' + str(rid))
        card = card_df.query('cardId == ' + str(race['cardId'].values[0]))

        for (val, arr) in race_vals.items():
            arr.append(race[val].values[0])
        
        for (val, arr) in card_vals.items():
            arr.append(card[val].values[0])

    for (val, arr) in race_vals.items():
        # Race column name swaps:
        # number -> raceNumber
        # name -> raceName
        # distance -> raceDistance

        if val == "number":
            key = "raceNumber"
        elif val == "name":
            key = "raceName"
        elif val == "distance":
            key = "raceDistance"
        else:
            key = val

        df.insert(len(df.columns), key, arr)

    for (val, arr) in card_vals.items():
        df.insert(len(df.columns), val, arr)
    
    df.to_csv(SAVE_FOLDER + horse.replace("/", "_") + ".csv")

    i += 1
    if i % 1000 == 0:
        print(str(i) + "/" + n)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()