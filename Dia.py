import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np

monthsDict = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,
        'julho':7,'agosto':8, 'setembro':9, 'outubro':10, 'novembro':11,
        'dezembro':12}

invMonthDict = {v: k for k, v in monthsDict.items()}

drawColumns = ['Data','Empresa','Tipo','Número','Parcela','Valor',
                'Falta Boleta','Fora','Pago']

colConfigDict = {
    'Data':st.column_config.DateColumn(format='DD/MM/YY'),
    'Número':st.column_config.NumberColumn(format='%d'),
    'Valor':st.column_config.NumberColumn(format='R$ %.2f'),
    }

def drawSideBarToday(df):
    with st.sidebar:
        #today filter
        thisDay = dt.datetime.now().timetuple().tm_yday
        daySelection = st.radio('Dia',['Ontem','Hoje','Amanhã'],1)
        dayDict = {'Ontem':thisDay-1, 'Hoje':thisDay,'Amanhã': thisDay+1}
        df = df.loc[(df['Data'].dt.dayofyear==dayDict[daySelection])]

        #type filter
        setTipo = set(df['Tipo'].values)
        tipoSelect = st.multiselect('Tipo', setTipo)
        stmtTipo = ['Tipo=="%s"'%i for i in tipoSelect]
        queryTipo = ' | '.join(stmtTipo)
        if queryTipo:
            df.query(queryTipo, inplace=True)

        #empresa filter
        setEmpresa = set(df['Empresa'].values)
        empresaSelect = st.multiselect('Empresa',setEmpresa)
        stmtEmpresa = ['Empresa=="%s"'%i for i in empresaSelect]
        queryEmpresa = ' | '.join(stmtEmpresa)
        if queryEmpresa:
            df.query(queryEmpresa, inplace=True)

        #number filter
        setNumero = set(df['Número'].loc[df['Número'].notnull().values])
        numeroSelect = st.multiselect('Número',setNumero,
                                      format_func=lambda x:'%d'%x)
        stmtNumero = ['Número==%s'% i for i in numeroSelect]
        queryNumero = ' | '.join(stmtNumero)
        if queryNumero:
            df.query(queryNumero, inplace=True)

        st.session_state['df'] = df       
        return df

def drawSideBarWeek(df):
    with st.sidebar:
        #week filter
        thisWeek = dt.datetime.now().date().isocalendar()[1]
        weekSelection = st.radio('Semana',['Semana passada','Essa semana',
                                           'Próxima semana'],1)
        weekDict = {'Semana passada':thisWeek-1, 'Essa semana':thisWeek,
                    'Próxima semana': thisWeek+1}
        df = df.loc[(df['Data'].dt.isocalendar().week==weekDict[weekSelection])]

        #type filter
        setTipo = set(df['Tipo'].values)
        tipoSelect = st.multiselect('Tipo', setTipo)
        stmtTipo = ['Tipo=="%s"'%i for i in tipoSelect]
        queryTipo = ' | '.join(stmtTipo)
        if queryTipo:
            df.query(queryTipo, inplace=True)

        #empresa filter
        setEmpresa = set(df['Empresa'].values)
        empresaSelect = st.multiselect('Empresa',setEmpresa)
        stmtEmpresa = ['Empresa=="%s"'%i for i in empresaSelect]
        queryEmpresa = ' | '.join(stmtEmpresa)
        if queryEmpresa:
            df.query(queryEmpresa, inplace=True)

        #number filter
        setNumero = set(df['Número'].loc[df['Número'].notnull().values])
        numeroSelect = st.multiselect('Número',setNumero,
                                      format_func=lambda x:'%d'%x)
        stmtNumero = ['Número==%s'% i for i in numeroSelect]
        queryNumero = ' | '.join(stmtNumero)
        if queryNumero:
            df.query(queryNumero, inplace=True)

        st.session_state['df'] = df       
        return df

def drawSideBarMonth(df):
    with st.sidebar:
        #month filter
        monthsList = list(monthsDict.keys())
        monthsList.append('')
        selectMonth = st.selectbox('Mês', monthsList)
        if selectMonth:
            df = df.loc[(df['Data'].dt.month==monthsDict[selectMonth])]

        #type filter
        setTipo = set(df['Tipo'].values)
        tipoSelect = st.multiselect('Tipo', setTipo)
        stmtTipo = ['Tipo=="%s"'%i for i in tipoSelect]
        queryTipo = ' | '.join(stmtTipo)
        if queryTipo:
            df.query(queryTipo, inplace=True)

        #empresa filter
        setEmpresa = set(df['Empresa'].values)
        empresaSelect = st.multiselect('Empresa',setEmpresa)
        stmtEmpresa = ['Empresa=="%s"'%i for i in empresaSelect]
        queryEmpresa = ' | '.join(stmtEmpresa)
        if queryEmpresa:
            df.query(queryEmpresa, inplace=True)

        #number filter
        setNumero = set(df['Número'].loc[df['Número'].notnull().values])
        numeroSelect = st.multiselect('Número',setNumero,
                                      format_func=lambda x:'%d'%x)
        stmtNumero = ['Número==%s'% i for i in numeroSelect]
        queryNumero = ' | '.join(stmtNumero)
        if queryNumero:
            df.query(queryNumero, inplace=True)

        st.session_state['df'] = df       
        return df

def fetchSheet(conn, month):
    df = conn.read(
    worksheet=month,
    usecols=[0,1,2,3,4,5,6,7,8],
    skiprows=12,
    #ttl='10m',
    )

    #db clean
    dfColumns = ['Data','Empresa','Tipo','Número','Parcela','Valor',
                 'Falta Boleta','Fora','Pago']
    df.columns=dfColumns
    return df

def fetchDb(conn):
    df = pd.DataFrame()
    for i in range(1,13):
        sheet = fetchSheet(conn, i)
        df = pd.concat([df,sheet])

    #remove values without date
    df = df.loc[df['Data'].notnull()]
    #remove nulls
    df = df.replace({None:'',})

    #Date conversion
    df['Data'] = pd.to_datetime(df['Data'],dayfirst=True)

    return df

def drawProgressBar(df):
    total = df['Valor'].sum()
    now = df['Valor'].loc(df[''])

#
#col1,col2,col3 = st.columns(3)
#col1.metric('Total','R$ %.2f'%displayDf['Valor'].sum())
#col2.metric('Mercado','R$ %.2f'%displayDf.query('Categoria=="Mercado"')['Valor'].sum())
#col3.metric('Treatos','R$ %.2f'%displayDf.query('Categoria=="Treatos"')['Valor'].sum())
#
##legendSel = alt.selection_point(fields=['Categoria'], bind='legend')
#
#displayDfHor = displayDf
##displayDfHor['Mes'] = [i.month for i in displayDf['Data']]
##displayDfHor = displayDf.resample(rule='M', on='Data')['Valor'].sum().reset_index()
#displayDfHor['Mes'] = displayDfHor['Data'].dt.to_period('M').astype('datetime64[M]')
#displayDfHor = displayDfHor.groupby(['Mes','Categoria']).sum().reset_index()
##displayDfHor = displayDfHor.sort_values('Mes',ascending=False)
##displayDfHor = displayDfHor.replace(invMonthDict)
#
#chartSel = alt.selection_multi()
#horChart = alt.Chart(displayDfHor,height=300).mark_bar(size=40).encode(
#    x='Valor',
#    y='Mes',
#    color=alt.condition(chartSel, 'Categoria', alt.value('lightgray'))
#).add_params(chartSel)
#st.altair_chart(horChart,use_container_width=True)
#
#displayDf['Data'] = displayDf['Data'].dt.strftime('%d/%m/%Y')
#dfFormat = {'Valor':'R$ {:.2f}'}
#for key, value in dfFormat.items():
#    displayDf[key] = displayDf[key].apply(value.format)
#
## Print results.
#st.dataframe(displayDf, use_container_width=True, hide_index=True)


#from fantasy import *
import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title='Big Fantasy', page_icon=':bar_chart:',
                   layout='wide')

# Create a connection object.
conn = st.connection("gsheets", type=GSheetsConnection)
st.session_state['conn'] = conn

df = fetchDb(conn)
st.session_state['dfBol'] = df

df = drawSideBarToday(df)

col1,col2,col3 = st.columns(3)
col1.metric('Total','R$ {:,.2f}'.format(df['Valor'].sum()))
col2.metric('Total dentro','R$ {:,.2f}'.format(
    df['Valor'].loc[df['Fora']==''].sum()))
col3.metric('Total fora','R$ {:,.2f}'.format(
    df['Valor'].loc[df['Fora']=='x'].sum()))

st.dataframe(df[drawColumns],use_container_width=True,
             column_config=colConfigDict, hide_index=True)