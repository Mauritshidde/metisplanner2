import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import date
from sharepoint import SharePointSite, basic_auth_opener

from excel_files import get_all_files

import schedule
import time

import mysql.connector as mysql

conn = mysql.connect(
   host=HOST, database=DATABASE, user=USER, password=PASSWORD
)
c = conn.cursor()
klassen = ["4V", "5V", "6V", "3H", "4H", "5H"]

def vakken_uit_db(klas):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    sql = "SELECT vak FROM vakken WHERE klas = %s"
    val = (klas,)
    c.execute(sql, val)
    vakken_db = c.fetchall()
    vakken = []
    for vak in vakken_db:
        vakken.append(vak[0])
    c.close()
    conn.close()
    return vakken

def weken_uit_excel():
    locatie = "excelfiles/4V planner.xlsx"
    df2 = (pd.read_excel(locatie, skiprows=1, engine ='openpyxl').dropna(how='all', axis=0))
    dataframe_weken = df2.iloc[[1]]
    aantal_keer = len(df2.axes[1])
    aantal_keer = aantal_keer//3
    weken_aantal = 1
    datum_aantal = 2
    raw_weken = []
    for data_weken in dataframe_weken:
        raw_weken.append(data_weken)

    datums = []
    weken = []
    for keren in range(aantal_keer):
        weken.append(int(raw_weken[weken_aantal]))
        datums.append(raw_weken[datum_aantal])
        weken_aantal += 3
        datum_aantal += 3
    return weken, datums

def weken_in_db():
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    c.execute("DELETE FROM datums")
    c.execute("DELETE FROM weken")
    weken, datums = weken_uit_excel()

    eerste_week = weken[0]
    laatste_week = weken[-1]
    c.execute("INSERT INTO weken (week) VALUES (%s)", (eerste_week,))
    c.execute("INSERT INTO weken (week) VALUES (%s)", (laatste_week,))
    conn.commit()
    for i in range(len(weken)):
        c.execute("INSERT INTO datums (datum, week) VALUES (%s, %s)", (datums[i], weken[i],))
        conn.commit()
    c.close()
    conn.close()

def data_uit_excel(klassen):
    onderwerp = {}
    weekopdracht = {}
    toets_deadline = {}
    for klas in klassen:
        locatie = "excelfiles/"+klas+" planner.xlsx"
        vakken = vakken_uit_db(klas)
        onderwerp[klas] = []
        weekopdracht[klas] = []
        toets_deadline[klas] = []
        vakken_onderwerp = {}
        vakken_weekopdracht = {}
        vakken_toets_deadline = {}
        for vak_je in vakken:
            try:
                vak = vak_je.replace("_", " ")
                df = (pd.read_excel(locatie, skiprows=4, engine ='openpyxl').dropna(how='all', axis=0))
                df.set_index("filter", inplace=True)
                data = df.loc[vak]
                data.fillna(value = "niks", inplace = True)
                weken, datum = weken_uit_excel()
                aantal_keer2 = len(df.axes[1])
                aantal_keer = aantal_keer2//3
                onderwerp_aantal = 1
                weekopdracht_aantal = 2
                toets_deadline_aantal = 3
                vakken_onderwerp[vak] = []
                vakken_weekopdracht[vak] = []
                vakken_toets_deadline[vak] = []
                for keren in range(aantal_keer):
                    onderwerp_aantalstr = str(onderwerp_aantal)
                    weekopdracht_aantalstr =  str(weekopdracht_aantal)
                    toets_deadline_aantalstr = str(toets_deadline_aantal)
                    deel_onderwerp = data.loc["Unnamed: " +onderwerp_aantalstr]
                    deel_weekopdracht = data.loc["Unnamed: " +weekopdracht_aantalstr]
                    deel_toets_deadline = data.loc["Unnamed: " +toets_deadline_aantalstr]
                    vakken_onderwerp[vak].append(deel_onderwerp)
                    vakken_weekopdracht[vak].append(deel_weekopdracht)
                    vakken_toets_deadline[vak].append(deel_toets_deadline)
                    onderwerp_aantal += 3
                    weekopdracht_aantal += 3
                    toets_deadline_aantal += 3
            except:
                pass

        onderwerp[klas].append(vakken_onderwerp)
        weekopdracht[klas].append(vakken_weekopdracht)
        toets_deadline[klas].append(vakken_toets_deadline)
    return onderwerp, weekopdracht, toets_deadline

def data_from_excel_to_db():
    weken, datum = weken_uit_excel()
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    conn.commit()
    onderwerp, weekopdracht, toets_deadline = data_uit_excel(klassen)
    for klas in klassen:
        onderwerp_klas = onderwerp[klas][0]
        weekopdracht_klas = weekopdracht[klas][0]
        toets_deadline_klas = toets_deadline[klas][0]
        vakken = vakken_uit_db(klas)
        for new_vak in vakken:
            vak = new_vak.replace("_", " ")
            try:
                onderwerp_vak = onderwerp_klas[vak]
                weekopdracht_vak = weekopdracht_klas[vak]
                toets_deadline_vak = toets_deadline_klas[vak]
                for keren in range(len(weken)):
                    onderwerp_voor_db = onderwerp_vak[keren]
                    weekopdracht_voor_db = weekopdracht_vak[keren]
                    toets_deadline_voor_db = toets_deadline_vak[keren]
                    week = weken[keren]
                    try:
                        sql = "SELECT * FROM dataUitExcel WHERE klas = %s AND vak = %s AND week_nummer = %s"
                        val = (klas, vak, week, )
                        c.execute(sql, val)
                        result = c.fetchall()
                        if result:
                            sql1 = "UPDATE dataUitExcel SET waarde = %s WHERE type = %s AND klas = %s AND vak = %s AND week_nummer = %s"
                            val1 = (onderwerp_voor_db, "onderwerp", klas, vak, week, )
                            c.execute(sql1, val1)

                            sql2 = "UPDATE dataUitExcel SET waarde = %s WHERE type = %s AND klas = %s AND vak = %s AND week_nummer = %s"
                            val2 = (weekopdracht_voor_db, "weekopdracht", klas, vak, week, )
                            c.execute(sql2, val2)

                            sql3 = "UPDATE dataUitExcel SET waarde = %s WHERE type = %s AND klas = %s AND vak = %s AND week_nummer = %s"
                            val3 = (toets_deadline_voor_db, "toets", klas, vak, week, )
                            c.execute(sql3, val3)

                            conn.commit()
                        else:
                            c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("onderwerp", onderwerp_voor_db, klas, vak>
                            c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("weekopdracht", weekopdracht_voor_db, kla>
                            c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("toets", toets_deadline_voor_db, klas, va>
                            conn.commit()
                    except:
                        c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("onderwerp", onderwerp_voor_db, klas, vak, we>
                        c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("weekopdracht", weekopdracht_voor_db, klas, v>
                        c.execute("INSERT INTO dataUitExcel (type, waarde, klas, vak, week_nummer) VALUES (%s,%s,%s,%s,%s)", ("toets", toets_deadline_voor_db, klas, vak, w>
                        conn.commit()
            except:
                pass
    c.close()
    conn.close()

def vakken_uit_excel(klas):
    locatie = "excelfiles/"+klas+" planner.xlsx"
    df = (pd.read_excel(locatie, skiprows=4, engine ='openpyxl').dropna(how='all', axis=0))
    df.fillna(value = "niks", inplace = True)
    vakken_list = []
    data = True
    locatie = 0
    while data:
        try:
            vak = df.iloc[locatie].iloc[0]
            locatie += 1
            if vak == "niks":
                pass
            else:
                nieuw_vak = vak.replace(" ", "_")
                vakken_list.append(nieuw_vak)
        except:
            data = False
    return vakken_list

def vakken_in_db(vakken):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    for klas in klassen:
        vakken_klas = vakken[klas]
        for vak in vakken_klas:
            sql = "SELECT * FROM vakken WHERE vak = %s AND klas = %s"
            val = (vak, klas)
            c.execute(sql, val)
            result = c.fetchall()
            if result:
                pass
            else:
                c.execute("INSERT INTO vakken (vak, klas) VALUES (%s,%s)", (vak, klas))
                conn.commit()
    c.close()
    conn.close()

def vakken_uit_excel_in_db():
    vakken = {}
    for klas in klassen:
        vakken[klas] = []
        vakken_list = vakken_uit_excel(klas)
        for vak in vakken_list:
            vakken[klas].append(vak)
    vakken_in_db(vakken)

def belangrijke_uit_excel(klas):
    locatie = "excelfiles/"+klas+" planner.xlsx"
    df = (pd.read_excel(locatie, skiprows=1, engine ='openpyxl').dropna(how='all', axis=0))
    df.set_index("week", inplace=True)
    df.fillna(value = "niks", inplace = True)
    vakken_list = []
    data = True
    locatie = 0
    weken, datum = weken_uit_excel()
    belangrijke_data = []
    for i in range(len(weken)):
        data = df.iloc[0].iloc[locatie]
        belangrijke_data.append(data)
        locatie +=3
    return belangrijke_data

def belangrijke_in_db(belangrijke_data):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    weken, datum = weken_uit_excel()
    for klas in klassen:
        data_klas = belangrijke_data[klas]
        for i in range(len(weken)):
            data = data_klas[i]
            week = weken[i]
            sql = "SELECT * FROM belangrijk WHERE data = %s AND klas = %s AND week = %s"
            val = (data, klas, week)
            c.execute(sql, val)
            result = c.fetchall()
            if result:
                pass
            else:
                c.execute("INSERT INTO belangrijk (data, klas, week) VALUES (%s,%s,%s)", (data, klas, week,))
                conn.commit()
    c.close()
    conn.close()

def belangrijke_uit_excel_in_db():
    belangrijke_data = {}
    for klas in klassen:
        belangrijke_data[klas] = []
        data_list = belangrijke_uit_excel(klas)
        for data in data_list:
            belangrijke_data[klas].append(data)
    belangrijke_in_db(belangrijke_data)

def totaal():
    get_all_files()
    vakken_uit_excel_in_db()
    weken_in_db()
    belangrijke_uit_excel_in_db()
    data_from_excel_to_db()
    print("5")

schedule.every(600).minutes.do(totaal)

while True:
    schedule.run_pending()
    time.sleep(3)
