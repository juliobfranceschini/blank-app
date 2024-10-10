import streamlit as st
import pandas as pd

# Função para carregar a planilha
def carregar_planilha(caminho_arquivo):
    df = pd.read_excel(caminho_arquivo)
    return df

# Função para filtrar os dados com base no código da debênture e na data
def filtrar_debenture(df, codigo_debenture, data_ref=None):
    df_filtrado = df[df['Código'] == codigo_debenture]

    # Se o usuário selecionar uma data específica
    if data_ref:
        df_filtrado = df_filtrado[df_filtrado['Data de referência'] == data_ref]

    return df_filtrado

# Caminho do arquivo Excel
caminho_arquivo = "debentures-precos-07-10-2024-13-59-00.xls"

# Carregar a planilha
df = carregar_planilha(caminho_arquivo)

# Ajustar as opções de exibição para ver todas as colunas no Streamlit (caso queira ver os dados brutos)
pd.set_option("display.max_columns", None)

# Título do dashboard
st.title("Dashboard de Debêntures")

# Entrada para o código da debênture
codigo_debenture = st.text_input("Digite o Código da Debênture:", "")

# Se um código foi inserido, filtrar os dados
if codigo_debenture:
    # Filtrar as datas disponíveis para a debênture inserida
    df_filtrado = df[df['Código'] == codigo_debenture]

    if not df_filtrado.empty:
        # Permitir que o usuário selecione uma data específica das disponíveis
        data_disponivel = st.selectbox("Selecione a Data de Referência:", df_filtrado['Data de referência'].unique())

        # Filtrar pelos dados da data selecionada
        debenture_dados = filtrar_debenture(df_filtrado, codigo_debenture, data_ref=data_disponivel)

        if not debenture_dados.empty:
            st.write(f"### Informações da Debênture ({codigo_debenture}) em {data_disponivel}:")

            # Ajustar a coluna 'Duration' para mostrar o valor em anos
            debenture_dados['Duration (em anos)'] = debenture_dados['Duration'] / 252

            # Exibir as colunas relevantes (incluindo a nova coluna 'Duration (em anos)')
            st.write(debenture_dados[['Remuneração', 'Tipo Remuneração', 'Taxa de compra', 'Duration (em anos)']])
        else:
            st.write("Nenhuma informação disponível para essa combinação de código e data.")
    else:
        st.write("Nenhuma debênture encontrada com o código fornecido.")
else:
    st.write("Por favor, insira o código da debênture para buscar as informações.")

# Adicionar opção para exportar os dados filtrados
if not df_filtrado.empty:
    df_filtrado.to_excel('df_combinado.xlsx', index=False)
    with open('df_combinado.xlsx', 'rb') as f:
        st.download_button('Baixar dados em Excel', f, file_name='df_combinado.xlsx')
