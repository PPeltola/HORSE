import pandas as pd
import os

DATA_FOLDER = "data/cards/"

frames = []

for card in os.listdir(DATA_FOLDER):
    c = pd.read_csv(DATA_FOLDER + card)
    c['date'] = card[:10]
    frames.append(c)

df = pd.concat(frames)
df.to_csv("cards.csv")