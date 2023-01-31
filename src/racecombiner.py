import pandas as pd
import os

DATA_FOLDER = "data/races/"

frames = []

n = str(len(os.listdir(DATA_FOLDER)))

i = 0
for race in os.listdir(DATA_FOLDER):
    r = pd.read_csv(DATA_FOLDER + race)
    frames.append(r)

    i += 1
    if i % 200 == 0:
        print(str(i) + "/" + n)

df = pd.concat(frames)
df.to_csv("races.csv")
