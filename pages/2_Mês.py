#from Dia import drawSideBarMonth, drawColumns, colConfigDict
import streamlit as st
from streamlit_gsheets import GSheetsConnection

monthsDict = {'janeiro':1,'fevereiro':2,'março':3,'abril':4,'maio':5,'junho':6,
        'julho':7,'agosto':8, 'setembro':9, 'outubro':10, 'novembro':11,
        'dezembro':12}

drawColumns = ['Data','Empresa','Tipo','Número','Parcela','Valor',
                'Falta Boleta','Fora','Pago']

colConfigDict = {
    'Data':st.column_config.DateColumn(format='DD/MM/YY'),
    'Número':st.column_config.NumberColumn(format='%d'),
    'Valor':st.column_config.NumberColumn(format='R$ %.2f'),
    }

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

st.set_page_config(page_title='Big Fantasy', page_icon=':bar_chart:',
                   layout='wide')

df = st.session_state['dfBol']

df = drawSideBarMonth(df)

col1,col2,col3 = st.columns(3)
col1.metric('Total','R$ {:,.2f}'.format(df['Valor'].sum()))
col2.metric('Total dentro','R$ {:,.2f}'.format(
    df['Valor'].loc[df['Fora']==''].sum()))
col3.metric('Total fora','R$ {:,.2f}'.format(
    df['Valor'].loc[df['Fora']=='x'].sum()))

st.dataframe(df[drawColumns],use_container_width=True,
             column_config=colConfigDict, hide_index=True)