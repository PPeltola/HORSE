import pandas as pd
import os
import datetime

df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_runners_fixed.csv")

state_dict = {}


for i, row in df.iterrows():
    continue