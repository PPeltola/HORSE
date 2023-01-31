import pandas as pd
import os
import time

DATA_FOLDER = "data/runners/"

races = os.listdir(DATA_FOLDER)

def combinerace(raceid):
    starts = os.listdir(DATA_FOLDER + raceid)
    frames = []
    for s in starts:
        frames.append(pd.read_csv(DATA_FOLDER + raceid + "/" + s))
    return pd.concat(frames)

#init = races[0]
#df = combinerace(init)

frames = []

i = 1
s_time = time.time()
for race in races:
    #df = pd.concat([df, combinerace(race)])
    frames.append(combinerace(race))

    i += 1
    if i % 200 == 0:
        print(str(i) + "/" + str(len(races)))
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

print("combining frames...")
s_time = time.time()
df = pd.concat(frames)
print("\ttime elapsed: " + str(time.time() - s_time))
df.to_csv("runners.csv")