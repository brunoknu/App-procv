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
    #interações app

    st.set_page_config(page_title="Verificador de Divergência", layout="wide")
    st.title("Verificador de Divergência entre duas bases")


    #etapa 1: upload

    st.header("1. Envie as Bases")
    col1, col2 = st.columns(2)

    with col1:
        file1 = st.file_uploader("Base Principal (Arquivo 1)", type=['csv', 'xls', 'xlsx'])
    with col2:
        file2 = st.file_uploader("Base de Referência (Arquivo 2)", type=['csv', 'xls', 'xlsx'])
    
    if file1 and file2:
        df1 = carregar_arquivo(file1)
        df2 = carregar_arquivo(file2)

        if df1 is not None and df2 is not None:
            st.header("2. Escolha a Coluna de Comparação")
            coluna1 = st.selectbox("Coluna Base (Arquivo 1)", df1.columns)
            coluna2 = st.selectbox("Coluna Base (Arquivo 2)", df2.columns)

    #etapa 3

        if st.button('Executar Comparação'):
            set_ref = set(df2[coluna2])
            df_iguais = df1[df1[colun1].isin(set_ref)].copy()
            df_diferentes = df1[~df1[coluna1].isin(set_ref)].copy()

    # Resultados
            st.header("3. Resultados da Comparação")
            st.success(f" Registros Encontrados na referência: {len(df_iguais)}")
            st.warning(f" Registros Não Encontrados na referência: {len(df_diferentes)}")

            st.subheader("Registros Encontrados")
            st.dataframe(df_iguais, use_container_width=True)
            gerar_download(df_iguais, "registros_iguais")

            st.subheader("Registros Não Encontrados")
            st.dataframe(df_diferentes, use_container_width=True)
            gerar_download(df_diferentes, "registros_diferentes")
        else:
            st.error("Erro ao processar os arquivos.")
    else:
        st.info("Envie os dois arquivos para começar a comparação.")