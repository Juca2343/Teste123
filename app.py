import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Dashboard de Custos", layout="wide")
st.title("📊 Dashboard de Custos e Reduções")

# Upload do Excel
arquivo = st.file_uploader("📤 Faça upload do arquivo Excel", type=["xlsx"])

if arquivo is not None:
    df = pd.read_excel(arquivo)

    # Tratamento de dados
    df = df.dropna(subset=['Categoria', 'Fornecedor', 'Custo Anual', 'Redução'])
    df['% Redução'] = df['Redução'] / df['Custo Anual']

    # Filtros
    categorias = df['Categoria'].unique()
    fornecedores = df['Fornecedor'].unique()

    col_filtros1, col_filtros2 = st.columns(2)
    categoria_sel = col_filtros1.multiselect("🔹 Filtrar por Categoria", categorias, default=categorias)
    fornecedor_sel = col_filtros2.multiselect("🔹 Filtrar por Fornecedor", fornecedores, default=fornecedores)

    df_filtrado = df[
        (df['Categoria'].isin(categoria_sel)) &
        (df['Fornecedor'].isin(fornecedor_sel))
    ]

    # KPIs
    custo_total = df_filtrado['Custo Anual'].sum()
    reducao_total = df_filtrado['Redução'].sum()
    pct_total = reducao_total / custo_total if custo_total > 0 else 0

    col1, col2, col3 = st.columns(3)
    col1.metric("💰 Custo Total", f"R$ {custo_total:,.0f}")
    col2.metric("📉 Redução Total", f"R$ {reducao_total:,.0f}")
    col3.metric("📊 % Redução Média", f"{pct_total:.1%}")

    st.markdown("---")

    # Abas para gráficos
    aba1, aba2, aba3, aba4 = st.tabs(["💰 Custo por Categoria", "📉 Redução por Fornecedor", "📊 % Redução por Categoria", "🧠 Custo vs Redução"])

    with aba1:
        custo_categoria = df_filtrado.groupby('Categoria', as_index=False)['Custo Anual'].sum()
        fig1 = px.bar(custo_categoria, x='Categoria', y='Custo Anual', text_auto=True,
                      title="💰 Custo Total por Categoria")
        st.plotly_chart(fig1, use_container_width=True)

    with aba2:
        fornecedor_reducao = df_filtrado.groupby('Fornecedor', as_index=False).agg({
            'Custo Anual': 'sum',
            'Redução': 'sum'
        })
        fornecedor_reducao['% Redução'] = fornecedor_reducao['Redução'] / fornecedor_reducao['Custo Anual']
        fig2 = px.bar(fornecedor_reducao, x='Fornecedor', y='% Redução', text_auto='.1%',
                      title="📉 % de Redução por Fornecedor")
        st.plotly_chart(fig2, use_container_width=True)

    with aba3:
        categoria_reducao = df_filtrado.groupby('Categoria', as_index=False).agg({
            'Custo Anual': 'sum',
            'Redução': 'sum'
        })
        categoria_reducao['% Redução'] = categoria_reducao['Redução'] / categoria_reducao['Custo Anual']
        fig3 = px.bar(categoria_reducao, x='Categoria', y='% Redução', text_auto='.1%',
                      title="📉 % de Redução por Categoria")
        st.plotly_chart(fig3, use_container_width=True)

    with aba4:
        fig4 = px.scatter(df_filtrado, x='Custo Anual', y='Redução', color='Categoria',
                          hover_name='Fornecedor', size='Custo Anual',
                          title="🧠 Custo x Redução por Fornecedor")
        st.plotly_chart(fig4, use_container_width=True)

    st.markdown("---")

    # Download dos dados
    csv = df_filtrado.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Baixar dados filtrados", data=csv, file_name="dados_filtrados.csv", mime="text/csv")

    # Dados brutos
    st.subheader("📄 Dados Brutos Filtrados")
    st.dataframe(df_filtrado)