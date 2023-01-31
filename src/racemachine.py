import pandas as pd
import os

RUNNER_DATA_FOLDER = "data/testdata/vermo_19_10_22/test/"
CARD_DATA_FOLDER = "data/races/"

card_ids = os.listdir(RUNNER_DATA_FOLDER)

for cid in card_ids:
    RACE_FOLDER = RUNNER_DATA_FOLDER + str(cid) + "/"
    card_df = pd.read_csv(CARD_DATA_FOLDER + str(cid) + ".csv")
    
    if not os.path.exists(RACE_FOLDER + "combined"):
        os.mkdir(os.path.join(RACE_FOLDER, "combined"))

    for i, row in card_df.iterrows():
        runner_df = pd.read_csv(RACE_FOLDER + str(row['raceId']) + ".csv")
        runner_df['seriesSpecification'] = row['seriesSpecification']
        runner_df['breed'] = row['breed']
        runner_df['origDistance'] = row['distance']
        runner_df['raceNumber'] = row['number']
        runner_df['raceStatus'] = row['raceStatus']
        runner_df['startType'] = row['startType']
        runner_df['monte'] = row['monte']
        runner_df['firstPrize'] = row['firstPrize']
        runner_df['startTime'] = row['startTime']
        runner_df['toteResultString'] = row['toteResultString']
        runner_df['reserveHorsesOrder'] = row['reserveHorsesOrder']
        runner_df['raceRider'] = row['raceRider']
        runner_df['trackProfile'] = row['trackProfile']
        runner_df['trackSurface'] = row['trackSurface']
        #runner_df[] = row[]
    
        runner_df.to_csv(RACE_FOLDER + "/combined/" + str(row['raceId']) + "_combined.csv")

