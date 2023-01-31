import numpy as np
import pandas as pd
import json
import os
import time
import math

pd.options.mode.chained_assignment = None

"""
# ---- ELO config: elo8 ---- initial run, naming differs for this one
INITIAL_K = 45
EXPERIENCED_K = 25
HIGH_ELO_K = 15 # WIP

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1000 # wipwipwip # oh shit this was wrong

INITIAL_ELO = 1000
DIVISOR = 400 # very much WIP

# final_elo_dump.json
# 
# --------------------------


# ---- ELO config: B ----
INITIAL_K = 25
EXPERIENCED_K = 17
HIGH_ELO_K = 10 # WIP

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1600 # wipwipwip

INITIAL_ELO = 1000
DIVISOR = 200 # very much WIP
# -------------------


# ---- ELO config: flat15 ----
INITIAL_K = 15
EXPERIENCED_K = 15
HIGH_ELO_K = 15 # WIP

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 4000 # wipwipwip

INITIAL_ELO = 2000
DIVISOR = 200 # very much WIP
# -------------------

# ---- ELO config: fixed8_2 ---- 
INITIAL_K = 45
EXPERIENCED_K = 25
HIGH_ELO_K = 15 

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1800 

INITIAL_ELO = 1000
DIVISOR = 400 
# --------------------------

# ---- ELO config: flat25 ---- # featuring dynamic initial elo! 
INITIAL_K = 25                 # which turned out to be a bad idea (??)
EXPERIENCED_K = 25
HIGH_ELO_K = 25 

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 4000

INITIAL_ELO = None
BEDROCK_ELO = 2000
DIVISOR = 200 
# --------------------------

# ---- ELO config: alt8 ----  
INITIAL_K = 40
EXPERIENCED_K = 20
HIGH_ELO_K = 15 

BURN_IN_RACE_AMOUNT = 10
HIGH_ELO_THRESHOLD = 1500

INITIAL_ELO = None
BEDROCK_ELO = 1000
DIVISOR = 200 
# --------------------------

# ---- ELO config: new8_2 ---- # FOLDER TROUBLE, UNUSABLE FOR NOW 
INITIAL_K = 40
EXPERIENCED_K = 20
HIGH_ELO_K = 10 

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1800

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------

# ---- ELO config: new_flat15 ----
INITIAL_K = 15
EXPERIENCED_K = 15
HIGH_ELO_K = 15 # WIP

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 4000 # doesn't matter for flat configs

INITIAL_ELO = 2000
BEDROCK_ELO = None
DIVISOR = 200 # very much WIP
# -------------------

# ---- ELO config: new8_3 ---- 
INITIAL_K = 45
EXPERIENCED_K = 25
HIGH_ELO_K = 15

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1800

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------

# ---- ELO config: new9 ---- 
INITIAL_K = 40
EXPERIENCED_K = 20
HIGH_ELO_K = 10

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1800

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------

# ---- ELO config: new10 ---- 
INITIAL_K = 40
EXPERIENCED_K = 20
HIGH_ELO_K = 10

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 2600

INITIAL_ELO = 2000
BEDROCK_ELO = None
DIVISOR = 600
# --------------------------

# ---- ELO config: new11 ---- 
INITIAL_K = 40
EXPERIENCED_K = 25
HIGH_ELO_K = 15

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1200

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------

# ---- ELO config: new12 ---- 
INITIAL_K = 45
EXPERIENCED_K = 25
HIGH_ELO_K = 15

BURN_IN_RACE_AMOUNT = 10
HIGH_ELO_THRESHOLD = 1400

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------
"""
# ---- ELO config: new13 ---- 
INITIAL_K = 50
EXPERIENCED_K = 30
HIGH_ELO_K = 20

BURN_IN_RACE_AMOUNT = 20
HIGH_ELO_THRESHOLD = 1600

INITIAL_ELO = 1000
BEDROCK_ELO = None
DIVISOR = 400
# --------------------------


RUN_NAME = "new13"
PREV_RUN_NAME = "new12"

# -------------------

RACE_FOLDER = "/home/pp/Documents/HORSE_DATA/data/runners/"

#ALL_RACES_DF = "/home/pp/Documents/HORSE_DATA/data/fintracks_putsis.csv" # for finnish-only elo: felo
ALL_RACES_DF = "/home/pp/Documents/HORSE_DATA/data/races3_horsed3.csv"

all_races_df = pd.read_csv(ALL_RACES_DF)

# ---- functions ----

def rawEloChange(aElo, bElo, result):
    # result = did 'a' win, draw or lose    
    # return: aElo change, additive inverse for bElo change # CHANGED woah

    x = 1/(1 + 10 ** ((bElo - aElo) / DIVISOR))
    if result == 'win':
        return (1 - x)
    elif result == 'draw':
        return (0.5 - x)
    elif result == 'lose':
        return (0 - x)
    else:
        return "oops, this shouldn't happen"

def calibratedEloChange(raw, K):
    return int(round(K * raw))

def parseName(n):
    if not isinstance(n, str):
        return "[UNDEFINED]"

    name = n.lower().replace("*", "")

    if name[-1] == ')':
        return parseName(name[:-5])
    
    return name

def horseString(row):
    return parseName(row['horseName']) + " | " + parseName(row['sire']) + " | " + parseName(row['dam'])

def parseResultToJson(results, runnerNs):
    positions = results.replace(" ", "").split("-")
    ret = {}
    remaining = list(map(str, runnerNs.tolist()))

    for p in positions:
        pos = p.replace("(", "").replace(")", "").replace("/", ",")
        
        if ',' in pos:
            posits = pos.split(',')
            posits_x = posits.copy()[:-1]
            rem_x = remaining.copy()
            
            for px in posits:
                rem_x.remove(px)
            
            if len(rem_x) > 0:
                ret[posits[-1]] = [{'result': 'win',
                                    'to': rem_x.copy()}]
            
            for px in posits_x:
                pos_res = []
                posits.remove(px)
                pos_res.append({'result': 'draw',
                                'to': posits.copy()})
                if len(rem_x) > 0:
                    pos_res.append({'result': 'win',
                                    'to': rem_x.copy()})
                ret[px] = pos_res

            remaining = rem_x
        else:
            pos_res = []
            try:
                remaining.remove(pos)
            except:
                print("!!!!!!!!")
                print()
                print(results)
                print()
                print(p)
                print()
                print(pos)
            pos_res.append({'result': 'win',
                            'to': remaining.copy()})
            ret[pos] = pos_res

    rem = remaining.copy()[:-1]

    for r in rem:
        remaining.remove(r)
        ret[r] = [{'result': 'draw',
                   'to': remaining.copy()}]

    return ret

def getElo(horseString, elos, strings):
    if horseString in elos.keys():
        return elos[horseString]

    else:
        if INITIAL_ELO == None:
            hS = strings.copy()
            hS.remove(horseString)
            some_ranked = False
            other_elos = []

            for s in hS:
                if s in elos.keys():
                    some_ranked = True
                    other_elos.append(elos[s])

            if some_ranked:
                elo = round(np.mean(other_elos))
                elos[horseString] = elo
                return elo

            else:
                elos[horseString] = BEDROCK_ELO
                return BEDROCK_ELO

        else: 
            elos[horseString] = INITIAL_ELO
            return INITIAL_ELO

def getPrevRaceAmt(horseString, rAmts):
    if horseString in rAmts.keys():
        return rAmts[horseString]
    else:
        rAmts[horseString] = 0
    return 0

def getK(horseString, Ks):
    if horseString in Ks.keys():
        return Ks[horseString]
    else:
        Ks[horseString] = INITIAL_K
    return INITIAL_K

def updateAmts(hStrings, amts):
    for hS in hStrings:
        amts[hS] = getPrevRaceAmt(hS, amts) + 1

def updateKs(hStrings, Ks, amts, elos):
    for hS in hStrings:
        K = getK(hS, Ks)
        amt = getPrevRaceAmt(hS, amts)
        elo = getElo(hS, elos, hStrings)

        if amt <= BURN_IN_RACE_AMOUNT:
            continue
        elif elo >= HIGH_ELO_THRESHOLD and K != HIGH_ELO_K:
            Ks[hS] = HIGH_ELO_K
        elif K != EXPERIENCED_K:
            Ks[hS] = EXPERIENCED_K

def computeEloChanges(df, resStr, current_elos, current_amts, current_Ks, new_df_name, result_dump_name):
    ELO_BEFORE_RACE = RUN_NAME + "_eloBeforeRace"
    K_BEFORE_RACE = RUN_NAME + "_kBeforeRace"

    df = df[df['scratched'] == False]

    hStrings = []
    hString_by_number = {}
    for i, row in df.iterrows():
        hs = horseString(row)
        hStrings.append(hs)
        hString_by_number[str(row['startNumber'])] = hs
    
    #df['horseString'] = hStrings
    
    
    old_elos = [getElo(hS, current_elos, hStrings) for hS in hStrings]
    df[ELO_BEFORE_RACE] = old_elos.copy()

    old_amts = [getPrevRaceAmt(hS, current_amts) for hS in hStrings]

    #df['previousFinishesAmount'] = old_amts.copy()

    old_Ks = [getK(hS, current_Ks) for hS in hStrings]
    
    df[K_BEFORE_RACE] = old_Ks

    result_json = parseResultToJson(resStr, df['startNumber'])
    #print(json.dumps(result_json, indent=2))
    #print(hString_by_number)

    #for hNum in result_json.keys():
    #    for res in result_json[hNum]:
    #        return 

    #elo_change = {}
    #for hS in hStrings:
    #    elo_change[hS] = 

    elo_change = {
        hStrings[i]: {
            'oldElo': old_elos[i],
            'totalChange': 0,
            'oldAmt': old_amts[i],
            'oldK': old_Ks[i]
            } for i in range(len(hStrings))
    }

    for i, row in df.iterrows():
        aString = row['horseString']
        aNum = str(row['startNumber'])
        aElo = row[ELO_BEFORE_RACE]
        aK = row[K_BEFORE_RACE]

        if aNum in result_json.keys():
            for res in result_json[aNum]:
                result = res['result']
                for oper in res['to']:
                    bString = hString_by_number[oper]
                    bElo = elo_change[bString]['oldElo']
                    bK = elo_change[bString]['oldK']
                    
                    raw_change = rawEloChange(aElo, bElo, result)

                    elo_change[aString]['totalChange'] += calibratedEloChange(raw_change, aK)
                    elo_change[bString]['totalChange'] -= calibratedEloChange(raw_change, bK)

    #print(json.dumps(elo_change, indent=2))
    #print("\n--------\n")

    df.to_csv(new_df_name)

    #with open(result_dump_name, "w") as outfile:
    #    json.dump(result_json, outfile, indent=4)

    updateAmts(hStrings, current_amts)
    updateKs(hStrings, current_Ks, current_amts, current_elos)

    return elo_change
    
def applyEloChanges(state, change):
    for hs in change.keys():
        state[hs] = change[hs]['oldElo'] + change[hs]['totalChange']

def resultHorsesFoundInRunners(row, df, resultStr):
    df = df[df['scratched'] == False]

    resultHorses = resultStr.replace(" ", "").replace("(", "").replace(")", "").replace("/", "-").replace(",", "-")
    rs = resultHorses.split("-")
    nums = list(map(str, df['startNumber'].values.tolist()))

    if len(set(rs)) != len(rs):
        print("SAME HORSE PLACED TWICE (SOMEHOW): " + str(row["raceId"]))
        return False

    for r in rs:
        if r not in nums:
            print("BAD STRING: " + str(row["raceId"]))
            return False
    
    return True

def requiredColsExist(df, rCols, rid):
    for r in rCols:
        if r not in df.columns:
            print("BAD DF: " + r + " NOT IN RACE ID: " + str(rid))
            return False
        
    return True



# 4-( 2, 8)- 1


# -------------------

elo_state = {}
prev_race_amount_state = {}
K_state = {}

bad_results_rids = []

n = str(len(all_races_df))
i = 0
s_time = time.time()



for i, row in all_races_df.iterrows():
    cid = row['cardId']
    rid = row['raceId']

    if str(row['heppaAdjustedResults']) == "nan":
        resultString = row['toteResultString']
        #race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/alt8_elo/" + str(rid) + "_elo.csv")
    else: 
        resultString = str(row['heppaAdjustedResults'])
        #race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "/" + str(rid) + "_heppa.csv")

    #race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + str(rid) + ".csv")
    #race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "_elo/" + str(rid) + "_elo.csv")
    #race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "/" + str(rid) + "_heppa.csv")

    #if os.path.exists(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "_elo/" + str(rid) + "_elo.csv"):
    race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/" + PREV_RUN_NAME + "_elo/" + str(rid) + "_elo.csv")
    #else:
    #    print(rid)
    #    race_df = pd.read_csv(RACE_FOLDER + str(cid) + "/alt8_elo/" + str(rid) + "_elo.csv")


    if not resultHorsesFoundInRunners(row, race_df, resultString):
        bad_results_rids.append(rid)
        continue

    if not requiredColsExist(race_df, ['startNumber', 'horseName', 'sire', 'dam'], rid):
        bad_results_rids.append(rid)
        continue

    NEW_DIR_PATH = RACE_FOLDER + str(cid) + "/" + RUN_NAME + "_elo"

    if not os.path.exists(NEW_DIR_PATH):
        os.mkdir(NEW_DIR_PATH)

    new_df_name = NEW_DIR_PATH + "/" + str(rid) + "_elo" + ".csv"
    result_dump_name = NEW_DIR_PATH + "/" + str(rid) + "_result_dump" + ".json"
    
    elo_change = computeEloChanges(race_df, resultString,
                                   elo_state, prev_race_amount_state, 
                                   K_state, new_df_name,
                                   result_dump_name)

    applyEloChanges(elo_state, elo_change)

    i += 1
    if i % 1000 == 0:
        print(str(i) + "/" + n)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()

#print(json.dumps(elo_state, indent=2))

STATS_DIR = "/home/pp/Documents/HORSE_DATA/data/" +  RUN_NAME + "_elo_stats"
os.mkdir(STATS_DIR)

STAT_PREFIX = STATS_DIR + "/" + RUN_NAME
with open(STAT_PREFIX + "_final_elo_dump.json", "w") as outfile:
    json.dump(elo_state, outfile, indent=4)

with open(STAT_PREFIX + "_final_amt_dump.json", "w") as outfile:
    json.dump(prev_race_amount_state, outfile, indent=4)

with open(STAT_PREFIX + "_final_K_dump.json", "w") as outfile:
    json.dump(K_state, outfile, indent=4)

with open(STAT_PREFIX + "_bad_races.txt", "w") as outfile:
    for rid in bad_results_rids:
        outfile.write(str(rid) + "\n")

#print()
#print("4-( 2, 8)- 1".replace(" ", "").split("-"))
#parseResultString("4-( 2, 8)- 1", np.array([1, 2, 3, 4, 5, 6, 7, 8]))


# Different country suffix => different horse! (even if shared name 
# [Queen of Victory (SE) =/= Queen Of Victory (SA)])

