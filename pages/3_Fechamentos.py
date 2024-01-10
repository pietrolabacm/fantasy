from Dia import fetchDb
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
import datetime as dt

st.set_page_config(page_title='Big Fantasy', page_icon=':bar_chart:',
                   layout='wide')

monthsDict = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,
        'julho':7,'agosto':8, 'setembro':9, 'outubro':10, 'novembro':11,
        'dezembro':12}

invMonthDict = {v: k for k, v in monthsDict.items()}

def fetchFechSheet(conn, month):
    df = conn.read(
    worksheet=month,
    usecols=[0,1,2,3,4,5,6,7,8,9,10,11,12],
    skiprows=2,
    #ttl='10m',
    )

    #db clean
    dfColumns = ['Data','Dia','comp_soma','comp_din','comp_cartao','diferenca',
                 'real_soma','real_din','real_cartao','real_vale','Ana',
                 'Lucia','Marina']
    df.columns=dfColumns
    return df

def fetchFechDb(conn, month):
    df = fetchFechSheet(conn, month)
    #remove values without date
    df = df.loc[df['Data'].notnull()]
    #remove nulls
    df = df.replace({None:'',})
    #Date conversion
    df['Data'] = pd.to_datetime(df['Data'])
    return df


nowTimetuple = dt.datetime.now().timetuple()
targetDay = nowTimetuple.tm_mday
targetMonth = invMonthDict[nowTimetuple.tm_mon][:3]

#create connection fechamento 2024
connF = st.connection("gsheets2", type=GSheetsConnection)
st.session_state['connF24'] = connF
db2024 = fetchFechDb(connF, targetMonth)
db2024 = db2024.loc[(db2024['Data'].dt.day > targetDay-3) & 
                    (db2024['Data'].dt.day < targetDay+3)]

#create connection fechamento 2023
connF = st.connection("gsheets3", type=GSheetsConnection)
st.session_state['connF23'] = connF
db2023 = fetchFechDb(connF, targetMonth)
db2023 = db2023.loc[(db2023['Data'].dt.day > targetDay-3) & 
                    (db2023['Data'].dt.day < targetDay+3)]

#dataframe format
drawColumns = ['Data','Dia','comp_soma']
colConfigDict = {
    'Data':st.column_config.DateColumn(format='DD/MM/YY'),
    'comp_soma':st.column_config.NumberColumn(format='R$ %.2f'),
    }

#draw
col1, col2 = st.columns(2)
col1.write('2024')
col1.dataframe(db2024[drawColumns],use_container_width=True,
             column_config=colConfigDict, hide_index=True)
col2.write('2023')
col2.dataframe(db2023[drawColumns],use_container_width=True,
             column_config=colConfigDict, hide_index=True)