import pandas as pd
import os
import datetime

#HORSE_FOLDER = "data/horses2/"
HORSE_FOLDER = "data/testdata/feature_test/" # Test config

horses = [x[:-4] for x in os.listdir(HORSE_FOLDER)]
