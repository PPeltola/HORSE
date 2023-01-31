import pandas as pd
import json
import os
import requests

RACE_DATA_FOLDER = "data/races/"
CARD_DATA_FOLDER = "data/cards/"
CARDS_CSV = "data/cards.csv"

URL_STUMP = "https://www.veikkaus.fi/api/toto-info/v1/card/"

print("reading existing data...")
cards = pd.read_csv(CARDS_CSV)['cardId']
existing_races = [x.split('.')[0] for x in os.listdir(RACE_DATA_FOLDER)]
print("existing data read!")

i = 0
for card in cards:
    if card not in existing_races:
        get = requests.get(URL_STUMP + str(card) + "/races")
        parsed = json.loads(get.text)
        df = pd.DataFrame(parsed['collection'])
        df.to_csv(RACE_DATA_FOLDER + str(card) + ".csv")
    i += 1
    if i % 200 == 0:
        print(str(i) + "/" + str(len(cards)))
    
print("Wow! it really is finally done!")