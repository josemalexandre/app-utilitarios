import pandas as pd
import numpy as np
import streamlit as st
import warnings
import io

warnings.filterwarnings('ignore')

def tratar_dados(xls):
    file_xls = pd.read_excel(xls, skiprows=3)
    file_xls = file_xls[['LJ', 'CREDOR', 'DT. PAG.', 'VALOR ']]
    file_xls['LJ'].replace(1, np.nan, inplace=True)
    file_xls['LJ'].ffill(inplace=True)
    file_xls.rename(columns={'LJ':'ORIGEM', 'DT. PAG.': 'DATA', 'VALOR ':'DÉBITO'}, inplace=True)
    file_xls.dropna(inplace=True)

    return file_xls

st.title('Tratamento da Planilha CC Ducampo')

uploaded_file = st.file_uploader('Insira o arquivo em Excel')

if uploaded_file is not None:
    xls_file = tratar_dados(uploaded_file)

    st.dataframe(xls_file)

    st.write('---')

    buffer = io.BytesIO()

    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        xls_file.to_excel(writer, index=False, sheet_name='dados1')


    st.download_button(
        'Exportar XLXS',
        data=buffer,
        file_name='dados.xlsx',
        mime='text/xlsx'
    )