import pandas as pd
import streamlit as st
import requests
import io
from datetime import datetime as dt

st.set_page_config(layout='wide')

st.title('Atualização de um valor por um índice financeiro')

@st.cache_data
def atualiza_valores(dt_inicial, dt_final, serie, vlr):
    url = requests.get(f'https://api.bcb.gov.br/dados/serie/bcdata.sgs.{serie}/dados?formato=json&dataInicial={dt_inicial}&dataFinal={dt_final}')
    dados = url.json()
    df = pd.DataFrame(dados)
    df['valor'] = df['valor'].astype('float')
    df['acumulado'] = ((df['valor'] / 100) + 1).cumprod()
    df['vlr atualizado'] = vlr * df['acumulado']
  
    return df


container = st.container(border=True)

col1, col2, col3, col4 = container.columns([1, 1, 2, 2])

with col1:
    data_inicial = pd.to_datetime(st.date_input('Selecione a data inicial: ',value=dt(2024, 1, 1), format='DD/MM/YYYY'), format='%d/%m/%Y').strftime('%d/%m/%Y')

with col2:
    data_final = pd.to_datetime(st.date_input('Selecione a data final: ', format='DD/MM/YYYY'), format='%d/%m/%Y').strftime('%d/%m/%Y')

with col3:
    valor = st.number_input('Digite o valor a ser atualizado: ')
    
with col4:
    indices = sorted(['IPCA', 'INPC', 'INCC', 'IGP-M', 'SELIC'])
    indice = st.selectbox('Selecione o índice: ', indices)


col_df_1, col_df_2 = st.columns(2)

with col_df_1:
    if indice == 'IPCA':
        st.subheader('IPCA')
        dados_df = atualiza_valores(data_inicial, data_final, 433, valor)
   
    if indice == 'INPC':
        st.subheader('INPC')
        dados_df = atualiza_valores(data_inicial, data_final, 188, valor)
    
    if indice == 'IGP-M':
        st.subheader('IGP-M')
        dados_df = atualiza_valores(data_inicial, data_final, 189, valor)    
    
    if indice == 'INCC':
        st.subheader('INCC')
        dados_df = atualiza_valores(data_inicial, data_final, 192, valor)
   
    if indice == 'SELIC':
        st.subheader('SELIC')
        dados_df = atualiza_valores(data_inicial, data_final, 29541, valor)
    
    st.dataframe(dados_df, width=600)


with col_df_2:
    st.subheader('Valor Atualizado')
    with st.container(border=True):
        st.markdown(f'### **R$ {dados_df.iloc[-1,-2] * valor:.2f}**')
    
    st.subheader(f'Evolução do {indice}')
    st.line_chart(dados_df['valor'])
        
st.write('---')

buffer = io.BytesIO() # ESTUDAR

with pd.ExcelWriter(buffer, engine='openpyxl') as writer:   # ESTUDAR
    dados_df.to_excel(writer, index=False, sheet_name='dados1')


st.download_button(
    'Exportar XLXS',
    data=buffer,
    file_name='dados.xlsx',
    mime='text/xlsx'
)



    