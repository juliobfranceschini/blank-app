import streamlit as st
import pandas as pd

# Função para carregar a planilha
def carregar_planilha(uploaded_file):
    df = pd.read_excel(uploaded_file)
    return df

# Função para calcular a média e mediana das colunas "Taxa de compra" e "Taxa indicativa"
def calcular_estatisticas(df):
    media_taxa_compra = df['Taxa de compra'].mean()
    mediana_taxa_compra = df['Taxa de compra'].median()

    media_taxa_indicativa = df['Taxa indicativa'].mean()
    mediana_taxa_indicativa = df['Taxa indicativa'].median()

    return media_taxa_compra, mediana_taxa_compra, media_taxa_indicativa, mediana_taxa_indicativa

# Título do dashboard
st.title("Dashboard de Debêntures")

# Permitir upload do arquivo Excel
uploaded_file = st.file_uploader("Carregar arquivo Excel", type="xls")

# Verificar se um arquivo foi carregado
if uploaded_file is not None:
    # Carregar a planilha
    df = carregar_planilha(uploaded_file)

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
            debenture_dados = df_filtrado[df_filtrado['Data de referência'] == data_disponivel]

            if not debenture_dados.empty:
                st.write(f"### Informações da Debênture ({codigo_debenture}) em {data_disponivel}:")

                # Ajustar a coluna 'Duration' para mostrar o valor em anos
                debenture_dados['Duration (em anos)'] = debenture_dados['Duration'] / 252

                # Exibir as colunas relevantes (incluindo a nova coluna 'Duration (em anos)')
                st.write(debenture_dados[['Remuneração', 'Tipo Remuneração', 'Taxa de compra', 'Duration (em anos)']])

                # Calcular a média e mediana e exibir os resultados
                media_taxa_compra, mediana_taxa_compra, media_taxa_indicativa, mediana_taxa_indicativa = calcular_estatisticas(debenture_dados)
                st.write("### Estatísticas:")
                st.write(f"Média da Taxa de Compra: {media_taxa_compra:.2f}")
                st.write(f"Mediana da Taxa de Compra: {mediana_taxa_compra:.2f}")
                st.write(f"Média da Taxa Indicativa: {media_taxa_indicativa:.2f}")
                st.write(f"Mediana da Taxa Indicativa: {mediana_taxa_indicativa:.2f}")
            else:
                st.write("Nenhuma informação disponível para essa combinação de código e data.")
        else:
            st.write("Nenhuma debênture encontrada com o código fornecido.")
else:
    st.write("Por favor, carregue um arquivo Excel para buscar as informações.")
