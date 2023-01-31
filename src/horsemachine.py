import pandas as pd
import os
import time

RUNNER_CSV = "data/runners.csv"
DATA_FOLDER = "data/horses/"

print("reading existing data...")
s_time = time.time()
existing_horses = [x[:-4] for x in os.listdir(DATA_FOLDER)]
df = pd.read_csv(RUNNER_CSV)
print("existing data read!")
print("\ttime elapsed: " + str(time.time() - s_time) + "\n")
s_time = time.time()

n = str(len(df.horseName.unique()))
i = 0
for horsename in df.horseName.unique():
    if horsename not in existing_horses:
        horseframe = df[df['horseName'] == horsename]
        horseframe.to_csv(DATA_FOLDER + horsename.replace("/", "_") + ".csv")
    
    i += 1
    if i % 200 == 0:
        print(str(i) + "/" + n)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()