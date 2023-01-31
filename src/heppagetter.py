import numpy as np
import pandas as pd
import requests
import time

df = pd.read_csv("data/fintracks_linked.csv")
links = df['heppaLink'].unique()

for link in links:
    parts = link.split("=")
    track = parts[-2][:-3]
    stamp = parts[-3][2:-3]
    filename = track + "_" + stamp + ".html"

    get = requests.get(link)

    if not get.ok:
        print("OH NO: " + filename)
        continue

    with open("data/heppa/" + filename, "w") as file:
        file.write(get.text)

    time.sleep(1)
    
