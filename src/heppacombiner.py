import numpy as np
import pandas as pd
import os
import time
from bs4 import BeautifulSoup

df = pd.read_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_linked.csv")
#df = pd.read_csv("/home/pp/Documents/HORSE_DATA/broken/fintracks_broken1.csv")
#df = pd.read_csv("data/heppatest.csv")

def clean_result_frame(frame):
    horses = []
    drivers = []
    distances = []
    lanes = []

    data = frame.rename(columns={"Hevonen / Ohjastaja": "Sijoitus",
                                 "Hevonen / Ohjastaja.1": "Numero", 
                                 "Unnamed: 4": "hylk_koodit"})

    for i, row in data.iterrows():
        x = row['Hevonen / Ohjastaja.2'].split("/")
        horses.append(x[0].strip())
        drivers.append(x[1].strip())

        y = row['Matka:rata']
        if isinstance(y, str) and ":" in y:
            y = y.split(":")
            distances.append(y[0])
            lanes.append(y[1])
        else:
            distances.append(pd.NA)
            lanes.append(pd.NA)

    data["Hevonen"] = horses
    data["Ohjastaja"] = drivers
    data["Matka"] = distances
    data["Rata"] = lanes

    data.drop(columns=['Hevonen / Ohjastaja.2', 'Matka:rata', 'Unnamed: 8'], inplace=True)

    return data
        
def get_race_frames(n, betdatas):
    ret = {}
    active = False

    for bd in betdatas:
        if bd.find('h3') != None:
            parts = bd.find('h3').getText().strip().split(' ')

            if parts[0] == str(n) + '.':
                #print(n)
                active = True
            elif active:
                if 'penalties' not in ret.keys():
                    ret['penalties'] = pd.DataFrame(index=["Henkilo", "Hevonen", "Rangaistus", "Sakko", "Kilpailukielto", "Rangaistuksen_syy"])
                return ret

        if bd.find('table', {'class': 'raceResultTable'}) != None:
            if active:
                result = pd.read_html(bd.find('table', {'class': 'raceResultTable'}).prettify())[0]
                ret['result'] = clean_result_frame(result)
            continue
        
        if bd.find('label', text="Väliajat:") != None:
            continue

        if bd.find('h4') != None:
            if bd.find('h4').getText().strip() == "Lähdön toto-tiedot":
                if active:
                    bet_data = bd.find_all('table')
                    ret['games'] = pd.read_html(bet_data[0].prettify())[0].dropna(how='all')
                    ret['toto'] = pd.read_html(bet_data[1].prettify())[0].dropna(how='all')
                continue

            elif bd.find('h4').getText().strip() == "Lähdön rangaistukset":
                if active:
                    ret['penalties'] = pd.read_html(bd.find('table').prettify())[0]
                    
        if active:
            if 'penalties' not in ret.keys():
                ret['penalties'] = pd.DataFrame(index=["Henkilo", "Hevonen", "Rangaistus", "Sakko", "Kilpailukielto", "Rangaistuksen_syy"])
            return ret

def handle_penalties(frame, penalties):
    pens = {}
    
    if penalties.empty:
        frame["Rangaistukset"] = pd.Series(dtype='str')
        return
    
    for i, row in penalties.iterrows():
        h = row['Hevonen']
        if h in pens.keys():
            pens[h].append(row.to_string())
        else:
            pens[h] = [row.to_string()]
    
    for i, row in frame.iterrows():
        h = row['Hevonen']
        if h in pens.keys():
            frame.loc[i, "Rangaistukset"] = str(pens[h])

def find_data_from_blocks(datablocks, text):
    for db in reversed(datablocks):
        if db.find('h4') != None:
            content = db.find('h4').getText().strip()
            if content == text:
                return db.find('table')


RUNNER_PATH = "/home/pp/Documents/HORSE_DATA/data/runners/"
ELO_FOLDER = "alt8"
RUN_NAME = "heppa5"

k = 0
s_time = time.time()

for i, row in df.iterrows():
    rid = str(row['raceId'])
    cid = str(row['cardId'])
    
    #if os.path.exists(RUNNER_PATH + cid + "/" + RUN_NAME + "/" + rid + "_heppa.csv"):
    #    k += 1
    #    continue

    file_path = "/home/pp/Documents/HORSE_DATA/data/heppa/" + row['heppaCode'] + "_" + str(row['timestamp']) + ".html"
    
    file = open(file_path, "r")
    html = file.read()
    soup = BeautifulSoup(html, 'html.parser')

    n = row['number']
    bet_datas = soup.find_all('div', {'class': 'datablock'})
    frames = get_race_frames(n, bet_datas)
    
    if frames is None:
        print("!!!\t" + str(i) + "\t" + file_path)
        continue

    #print(str(i) + "\t" + file_path)

    if 'games' not in frames.keys():
        print("!!!GAMES\t" + str(i) + "\t" + file_path)
    elif not frames['games'].empty:
        for i2, r2 in frames['games'].iterrows():
            df.loc[i, r2['Peli'] + "_kertoimet"] = r2['Kertoimet']
            df.loc[i, r2['Peli'] + "_vaihdot"] = r2['Vaihdot']
    
    if 'toto' not in frames.keys():
        print("!!!TOTO\t" + str(i) + "\t" + file_path)
    elif not frames['toto'].empty:
        for i2, r2 in frames['toto'].iterrows():
            df.loc[i, r2['Peli'] + "_voitto-osuudet"] = r2['Voitto-osuudet']
            df.loc[i, r2['Peli'] + "_vaihdot"] = r2['Vaihdot']

    #dt = pd.read_html(bet_datas[-1].table.prettify())
    #if len(dt) > 0:
    #    df.loc[i, 'drugtested'] = str(list(pd.read_html(bet_datas[-1].table.prettify())[0][0].values))
    #else:
    #    df.loc[i, 'drugtested'] = pd.NA
    
    day_toto = find_data_from_blocks(bet_datas, "Ravipäivän toto-tiedot")

    df.loc[i, 'yleisoa'] = day_toto.find_all('tr')[-4].find('td', align='right').getText()#bet_datas[-1].table.find_all('tr')[-4].find('td', align='right').getText()
    df.loc[i, 'lampotila'] = day_toto.find_all('tr')[-3].find('td', align='right').getText() #bet_datas[-1].table.find_all('tr')[-3].find('td', align='right').getText()
    df.loc[i, 'radan_kunto'] = day_toto.find_all('tr')[-2].p.getText() #bet_datas[-1].table.find_all('tr')[-2].p.getText()
    
    handle_penalties(frames['result'], frames['penalties'])

    # ----

    """
    race_df = pd.read_csv(RUNNER_PATH + cid + "/" + ELO_FOLDER + "_elo/" + rid + "_elo.csv")
    combo = race_df.join(frames['result'].set_index('Numero'), on='startNumber')
    
    new_path = RUNNER_PATH + cid + "/heppa5"
    if not os.path.exists(new_path):
        os.mkdir(new_path)

    combo.to_csv(new_path + "/" + rid + "_heppa.csv")
    """

    k += 1
    if k % 1000 == 0:
        print(k)
        print("\ttime elapsed: " + str(time.time() - s_time))
        s_time = time.time()
        
df.to_csv("/home/pp/Documents/HORSE_DATA/data/fintracks_comboed2.csv")
