import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Custos", layout="wide")
st.title("📊 Dashboard de Custos e Reduções")

arquivo = st.file_uploader("📤 Faça upload do arquivo Excel", type=["xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)

    # Tratamento de dados
    df = df.dropna(subset=['Categoria', 'Fornecedor', 'Custo Anual', 'Redução'])
    df['% Redução'] = df['Redução'] / df['Custo Anual']

    # KPIs
    custo_total = df['Custo Anual'].sum()
    reducao_total = df['Redução'].sum()
    pct_total = reducao_total / custo_total

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Custo Total", f"R$ {custo_total:,.0f}")
    col2.metric("📉 Redução Total", f"R$ {reducao_total:,.0f}")
    col3.metric("📊 % Redução Média", f"{pct_total:.1%}")

    st.markdown("---")

    # Gráfico 1: Custo Anual por Categoria
    custo_categoria = df.groupby('Categoria', as_index=False)['Custo Anual'].sum()
    fig1 = px.bar(custo_categoria, x='Categoria', y='Custo Anual', text_auto=True,
                  title="💰 Custo Total por Categoria")
    st.plotly_chart(fig1, use_container_width=True)

    # Gráfico 2: % de Redução por Fornecedor
    fornecedor_reducao = df.groupby('Fornecedor', as_index=False).agg({
        'Custo Anual': 'sum',
        'Redução': 'sum'
    })
    fornecedor_reducao['% Redução'] = fornecedor_reducao['Redução'] / fornecedor_reducao['Custo Anual']
    fig2 = px.bar(fornecedor_reducao, x='Fornecedor', y='% Redução', text_auto='.1%',
                  title="📉 % de Redução por Fornecedor")
    st.plotly_chart(fig2, use_container_width=True)

    # Gráfico 3: % de Redução por Categoria
    categoria_reducao = df.groupby('Categoria', as_index=False).agg({
        'Custo Anual': 'sum',
        'Redução': 'sum'
    })
    categoria_reducao['% Redução'] = categoria_reducao['Redução'] / categoria_reducao['Custo Anual']
    fig3 = px.bar(categoria_reducao, x='Categoria', y='% Redução', text_auto='.1%',
                  title="📉 % de Redução por Categoria")
    st.plotly_chart(fig3, use_container_width=True)

    # Gráfico 4: Custo vs Redução (scatter)
    fig4 = px.scatter(df, x='Custo Anual', y='Redução', color='Categoria', hover_name='Fornecedor',
                      size='Custo Anual', title="🧠 Custo x Redução por Fornecedor")
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")
    st.subheader("📄 Dados Brutos")
    st.dataframe(df)

