from Dia import fetchDb
import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

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

def fetchFechDb(conn):
    fDb = {}
    for i in range(1,13):
        df = fetchFechSheet(conn, i)
        #remove values without date
        df = df.loc[df['Data'].notnull()]
        #remove nulls
        df = df.replace({None:'',})
        #Date conversion
        df['Data'] = pd.to_datetime(df['Data'])
        #write to dictionary
        fDb[invMonthDict[i]]=df

    return fDb

#create connection fechamento
connF = st.connection("gsheets2", type=GSheetsConnection)
st.session_state['connF'] = connF

dfDict = fetchFechDb(connF)
fullDb = pd.DataFrame()
for month in monthsDict:
    fullDb = pd.concat([fullDb,dfDict[month]]) 

chartDf = pd.DataFrame()
totalList = []
monthList = []
for month in monthsDict:
    totalList.append(dfDict[month]['comp_soma'].sum())
    monthList.append(month)
chartDf['Mês'] = monthList
chartDf['Total'] = totalList
chart = alt.Chart(chartDf).mark_bar().encode(
    x=alt.X('Mês',sort=list(monthsDict.keys())),
    y='Total')
st.altair_chart(chart,use_container_width=True)

fullDb['Month'] = fullDb['Data'].dt.month
dfGroupMonth = fullDb.groupby('Month')['comp_soma','comp_din','comp_cartao','Ana','Lucia','Marina'].sum().reset_index()

fig, ax = plt.subplots()
ax.bar(dfGroupMonth['Month'],dfGroupMonth['comp_din'])
ax.bar(dfGroupMonth['Month'],dfGroupMonth['comp_cartao'],bottom=dfGroupMonth['comp_din'])
st.pyplot(fig)
#chart2 = alt.Chart(dfGroupMonth).mark_bar().encode(
#    x='Month',
#    y='comp_soma')
#st.altair_chart(chart2,use_container_width=True)