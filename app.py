from flask import Flask, render_template, url_for, redirect, request, session, make_response
import xlrd, datetime
from forms import ZoekenForm, VolgendeWeekForm, SaveForm, KlassenForm
import pandas as pd
import numpy as np
from datetime import timedelta
from datetime import date
from sharepoint import SharePointSite, basic_auth_opener

from functies2 import *
import mysql.connector as mysql

app = Flask(__name__)

app.permanent_session_lifetime = datetime.timedelta(days=31)
pd.options.mode.chained_assignment = None

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

def data_uit_db(vakken, begin_week, eind_week, klas):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    onderwerp = {}
    toets_deadline = {}
    weekopdracht = {}
    for vak in vakken:
        onderwerp[vak] = []
        weekopdracht[vak] = []
        toets_deadline[vak] = []
        for week in range(begin_week, eind_week):

            sql = "SELECT waarde FROM dataUitExcel WHERE klas = %s and vak = %s and week_nummer = %s"
            val = (klas, vak, week, )
            c.execute(sql, val)
            excel_data = c.fetchall()

            datas = []
            for data in excel_data:
                datas.append(data[0])
            onderwerp[vak].append(datas[0])
            weekopdracht[vak].append(datas[1])
            toets_deadline[vak].append(datas[2])
    c.close()
    conn.close()
    return onderwerp, weekopdracht, toets_deadline

def belangrijk_uit_db(begin_week, eind_week, klas):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    belangrijk = []
    for week in range(begin_week, eind_week):
        sql = "SELECT * FROM belangrijk WHERE klas = %s AND week = %s"
        val = (klas, week, )
        c.execute(sql, val)
        excel_data = c.fetchall()
        datas = []
        for data in excel_data:
            datas.append(data[1])
        belangrijk.append(datas[0])
    c.close()
    conn.close()
    return belangrijk

def volg_week(vakken, eind_week, klas):
    onderwerp, weekopdracht, toets_deadline = volg_data_db(vakken, eind_week, klas)
    weken = [begin_week, begin_week+1, begin_week+2]
    return onderwerp, weekopdracht, toets_deadline

def vorg_week(vakken, eind_week, klas):
    onderwerp, weekopdracht, toets_deadline = vorg_data_db(vakken, begin_week, klas)
    weken = [begin_week, begin_week+1, begin_week+2]
    return onderwerp, weekopdracht, toets_deadline

def datum(weken):
    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()
    datums = []
    for week in weken:
        sql = "SELECT datum FROM datums WHERE week = %s"
        val = (week, )
        c.execute(sql, val)
        excel_data = c.fetchall()
        datums.append(excel_data[0])
    c.close()
    conn.close()
    return datums

@app.route('/invullen', methods=['GET', 'POST'])
def vakken():
    form = KlassenForm()
    try:
        klas = session['klas']
    except:
        klas = ""

    if request.method == 'POST':
        if request.form['submit_button'] == 'Bevestig keuze':
            gekozen_vakken = request.form.getlist('vakken_kiezen')
            print(gekozen_vakken)
            vakken = []
            for gekozen_vak in gekozen_vakken:
                nieuw_vak = gekozen_vak.replace("_", " ")
                vakken.append(nieuw_vak)
            print(vakken)
            session.clear()
            session['vakken'] = vakken
            session['klas'] = klas
            session.permanent = True
            return redirect(f"/")
        elif request.form['submit_button'] == 'Bevestig klas':
            klas = form.klas.data
            session.clear()
            session['klas'] = klas
            session['invullen'] = True
            return redirect(f"/invullen")
    if klas == "":
        vakken = []
    else:
        vakken = vakken_uit_db(klas)
    return render_template('zoeken.html', title='Login', form=form, vakken=vakken, klas=klas)

@app.route('/', methods=['GET', 'POST'])
def rooster():
    form = VolgendeWeekForm()
    form2 = SaveForm()

    conn = mysql.connect(host=HOST, database=DATABASE, user=USER, password=PASSWORD)
    c = conn.cursor()

    try:
        klas = session['klas']
        vakken = session['vakken']
    except:
        return redirect(f"/invullen")
    c.execute("SELECT week FROM weken")
    week_data = c.fetchall()
    c.close()
    conn.close()
    gegevens = []
    for data in week_data:
        gegevens.append(data[0])
    eerste_week = gegevens[0]
    laatste_week = gegevens[1]

    if request.method == 'GET':
        session['begin_week'] = begin_week = date.today().isocalendar()[1]
        session['eind_week'] = eind_week = date.today().isocalendar()[1] + 3
    else:
        begin_week = session['begin_week']
        eind_week = session['eind_week']
    if request.method == 'POST':
        if request.form.get("save"):
            return redirect(f"/invullen")

        elif request.form.get("vorige"):
            begin_week -= 1
            eind_week -= 1
            if begin_week == eerste_week - 1:
                begin_week = laatste_week - 2
                eind_week = laatste_week + 1
            elif begin_week == 0:
                begin_week = 50
                eind_week = 53
        elif request.form.get("volgende"):
            begin_week += 1
            eind_week += 1
            tussen_week = begin_week + 1
            if eind_week == laatste_week + 2:
                begin_week = eerste_week
                eind_week = eerste_week + 3
        else:
            begin_week = date.today().isocalendar()[1]
            eind_week = date.today().isocalendar()[1] + 3


    try:
       onderwerp, weekopdracht, toets_deadline = data_uit_db(vakken, begin_week, eind_week, klas)
    except:
       begin_week = 1
       eind_week = 4
       onderwerp, weekopdracht, toets_deadline = data_uit_db(vakken, begin_week, eind_week, klas)
    weken = [begin_week, begin_week+1, begin_week+2]
    datums = datum(weken)
    belangrijk = belangrijk_uit_db(begin_week, eind_week, klas)
    session['begin_week'] = begin_week
    session['eind_week'] = eind_week
    return render_template('rooster.html', form=form, form2=form2, title='Login', datums=datums, begin_week=begin_week, eind_week=eind_week, klas=klas, vakken=vakken, onderwerp=onderwerp, weekopdracht=weekopdracht, toets_doets_deadline=toets_deadline, weken=weken, belangrijk=belangrijk)

if __name__ == "__main__":
    app.run(host='0.0.0.0')
