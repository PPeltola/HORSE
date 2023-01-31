import pandas as pd
import json
import requests
import time

DATA_FOLDER = "data/cards/"

START_DATE = "2004-02-24"
URL_STUMP = "https://www.veikkaus.fi/api/toto-info/v1/cards/date/"

def getfor(date):
    s_time = time.time()
    get = requests.get(URL_STUMP + date)
    parsed = json.loads(get.text)
    prev = parsed['previous'][-10:]
    df = pd.DataFrame(parsed['collection'])
    df.to_csv(DATA_FOLDER + date + ".csv")
    print(date + " got, time elapsed: " +  str(time.time() - s_time))

    getfor(prev)

getfor(START_DATE)

# 1: START_DATE = "2022-11-01" -> 2020-03-01
# 2: START_DATE = "2020-03-01" -> 2017-06-30
# 3: START_DATE = "2017-06-30" -> 2014-10-29
# 4: START_DATE = "2014-10-29" -> 2012-02-27
# 5: START_DATE = "2012-02-27" -> 2009-06-27
# 6: START_DATE = "2009-06-27" -> 2006-10-26
# 7: START_DATE = "2006-10-26" -> 2004-02-24
# 8: START_DATE = "2004-02-24" -> 2003-01-02