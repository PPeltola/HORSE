import pandas as pd
import os
import datetime

#HORSE_FOLDER = "data/horses2/"
HORSE_FOLDER = "data/testdata/feature_test/" # Test config

#s_time = time.time()
horses = [x[:-4] for x in os.listdir(HORSE_FOLDER)]

n = str(len(horses))
i = 0

# -------- UTILITY --------

def applyRowOper(df, ind, opers):
    #fs = [(x[0], x[1], x[2], []) for x in fpn]
    ops = [(o, []) for o in opers]
    
    for row in df.itertuples():
        for (o, vals) in ops:
            state, val = o['func'](row, ind, (o['state'], o['params']))
            o['state'] = state
            vals.append(val)

    for (o, vals) in ops:
        df[o['name']] = vals

# --------------------------



# -------- FEATURES --------

def cameNthRow(row, ind, ps):
    #state = ps[0]
    n = ps[1][0]

    trsInd = ind.get_loc("toteResultString") + 1
    numInd = ind.get_loc("startNumber") + 1

    posits = row[trsInd].split("-")
    hNum = str(row[numInd])

    if len(posits) <= n:
        val = False
    elif ',' in posits[n].strip("()"):
        nths = posits[n].strip("()").split(',')
        val = hNum in nths
    else:
        nth = posits[n].strip()
        val = nth == hNum

    return None, val

def restSinceLastRow(row, ind, ps):
    lastTime = ps[0]

    timeInd = ind.get_loc("currentRaceStartTime") + 1

    currTime = datetime.datetime.fromtimestamp(int(row[timeInd] / 1000))
    if lastTime == None:
        val = None
    else:
        val = currTime - lastTime
    
    return currTime, val

def xFinishesInLastN(row, ind, ps):
    finishes = ps[0]
    x = ps[1][0]
    n = ps[1][1]

    a, res = cameNthRow(row, ind, [None, [x]])

    val = sum(finishes)

    if len(finishes) == n:
        del finishes[0]
    
    state = finishes
    state.append(res)

    return state, val

# --------------------------

for horse in horses:
    df = pd.read_csv(HORSE_FOLDER + horse.replace("/", "_") + ".csv")
    df = df.sort_values(by=['currentRaceStartTime'])
    index = df.columns

    rowOpers = []
    rowOpers.extend([
        {
            'func': cameNthRow,
            'params': [0],
            'name': 'cameFirst',
            'state': None
        },
        {
            'func': cameNthRow,
            'params': [1],
            'name': 'cameSecond',
            'state': None
        },
        {
            'func': cameNthRow,
            'params': [2],
            'name': 'cameThird',
            'state': None
        },
        {
            'func': restSinceLastRow,
            'params': [],
            'name': 'restSinceLast',
            'state': None
        },
        {
            'func': xFinishesInLastN,
            'params': [0, 5],
            'name': 'firstFinishesIn5',
            'state': []
        },
        {
            'func': xFinishesInLastN,
            'params': [1, 5],
            'name': 'secondFinishesIn5',
            'state': []
        },
        {
            'func': xFinishesInLastN,
            'params': [2, 5],
            'name': 'thirdFinishesIn5',
            'state': []
        },
        {
            'func': xFinishesInLastN,
            'params': [0, 3],
            'name': 'firstFinishesIn3',
            'state': []
        },
        {
            'func': xFinishesInLastN,
            'params': [1, 3],
            'name': 'secondFinishesIn3',
            'state': []
        },
        {
            'func': xFinishesInLastN,
            'params': [2, 3],
            'name': 'thirdFinishesIn3',
            'state': []
        }
    ])

    applyRowOper(df, index, rowOpers)

    df.to_csv(HORSE_FOLDER + horse.replace("/", "_") + "_test.csv")


