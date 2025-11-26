# importação das bibliotecas

import streamlit as st #criar app
import pandas as pd #importar dados
from io import BytesIO #criar botão

#funções

def carregar_arquivo(upload_file):
    """Carrega CSV ou Excel em tabela"""

    try:
        if upload_file.name.endswith('.csv'):
            return pd.read_csv(upload_file, engine='python', on_bad_lines='warn')
        elif upload_file.name.endswith(('.xls', '.xlsx')):
            return pd.read_excel(upload_file, engine='openpyxl')
        else:
            st.error("Formato de arquivo não suportado. Por favor, envie um arquivo CSV ou Excel.")
            return None
    except Exception as e:
        st.error(f"Erro ao carregar o arquivo: {e}")
        return None
    
    def gerar_download(df, nome):
        """Gera botão de download para DataFrame"""

        output = BytesIO()
        df.to_excel(output, index=False, engine='openpyxl')
        output.seek(0)
        st.download_button(
            label="Baixar {nome}",
            data=output,
            file_name=f"{nome}.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )