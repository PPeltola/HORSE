import numpy as np
import pandas as pd

#new_df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fiseno_fix1.csv") # old results used this
#new_df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/races3_horsed3.csv") # new all_races, this a bit shite
#new_df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_frankenhorse.csv") # new fin_races
new_df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_putsis.csv") # newnew fin_races

N = len(new_df)

def posN(results, N):
    positions = results.replace(" ", "").split("-")

    if len(positions) <= N:
        return []

    p = positions[N]
    pos = p.replace("(", "").replace(")", "").replace("/", ",")

    if ',' in pos:
        return pos.split(',')
    return [pos]

ELO_TOP = 0
PLACEMENT = [1]

ELO_USED = "new13" + "_eloBeforeRace"
FILE_USED = "new13"

def sa_acc(sa_did, sa_didnt):
    keys = set(list(sa_did.keys()) + list(sa_didnt.keys()))
    adj_acc = 0.0
    n = len(PLACEMENT)
    
    for k in keys:
        tot = sa_did.get(k, 0) + sa_didnt.get(k, 0)
        adj_acc += (tot / N) * ((sa_did.get(k, 0) / tot) - (n / k))

    return adj_acc

did = 0
didnt = 0

#size_adjusted_did = {}
#size_adjusted_didnt = {}

#n = len(new_df)
#tot_hs = 0

for i, row in new_df.iterrows():
    cid = row['cardId']
    rid = row['raceId']
    resultString = row['toteResultString']
    
    placements = []

    for p in PLACEMENT:
        placements = placements + posN(resultString, p)
    
    df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/runners/" + str(cid) + "/" + FILE_USED + "_elo/" + str(rid) + "_elo.csv")
    df = df[df['scratched'] == False]

    #print("/home/pp/Documents/HORSE_DATA/data/runners/" + str(cid) + "/" + FILE_USED + "_elo/" + str(rid) + "_elo.csv")

    elos = df.sort_values(by=[ELO_USED], ascending=False)
    runner_amt = len(elos)

    if runner_amt <= ELO_TOP:
        print("\nhuh?\n" + str(rid) + "\n\n")
        continue

    placed = elos.iloc[ELO_TOP]

    #tot_hs += len(df)
    
    if str(placed['startNumber']) in placements:
        did += 1
        #size_adjusted_did[runner_amt] = size_adjusted_did.get(runner_amt, 0) + 1

    else:
        didnt += 1
        #size_adjusted_didnt[runner_amt] = size_adjusted_didnt.get(runner_amt, 0) + 1
        
    if (int(i) + 1) % 50000 == 0:
        print()
        print(did)
        print(didnt)
        print()
        print(did / (did + didnt))
        #print()
        #print(tot_hs / (did + didnt))
        print("****")
        
print("--------" + ELO_USED + "--------") 
print("ELO_TOP = " + str(ELO_TOP))
print("PLACEMENT = " + str(PLACEMENT))
print()
print("did = " + str(did))
print("didnt = " + str(didnt))
print("accuracy = " + str(did / (did + didnt)))

#print()
#print("adjusted accuracy = " + str(sa_acc(size_adjusted_did, size_adjusted_didnt)))

#print()
#print(size_adjusted_did)
#print(size_adjusted_didnt)


#print()
#print("total_horses = " + str(tot_hs))
#print("total_races = " + str(n))
#print("avg_n_horses = " + str(tot_hs / n))
