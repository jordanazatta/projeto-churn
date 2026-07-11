# --- Importar as bibliotecas --- #
import streamlit as st
import plotly.express as px

# --- Importar os módulos do projeto --- #
from carregar_dados import carregar_dados

# --- Traduções --- #
from traducao import (
    traducao_categorias,
    traducao_motivos,
    traducao_contratos,
    traducao_churn
)


# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get('nome_usuario', '')

# --- Saudação --- #
if nome_usuario:
    st.write(f'Olá, {nome_usuario}!')
else:
    st.write('Olá!')

# --- Título --- #
st.title('Gráficos Interativos')

st.write(
    'Selecione um gráfico para explorar os dados de forma interativa.'
)

# --- Carregar os dados --- #
df = carregar_dados()

# --- Seleção dos gráficos --- #
sel_grafico = st.selectbox(
    label='Selecione o gráfico:',
    options=[
        'Situação dos clientes',
        'Categorias de cancelamento',
        'Principais motivos de cancelamento',
        'Churn por tipo de contrato'
    ]
)

# --- Situação dos clientes --- #
if sel_grafico == 'Situação dos clientes':

    dados = (
        df['Churn Label']
        .value_counts()
        .rename(index=traducao_churn)
        .reset_index()
    )

    dados.columns = [
        'Situação',
        'Quantidade de clientes'
    ]

    grafico = px.bar(
        dados,
        x='Situação',
        y='Quantidade de clientes',
        title='Situação dos clientes',
        text='Quantidade de clientes'
    )

    grafico.update_traces(
        textposition='outside'
    )

# --- Categorias de cancelamento --- #
elif sel_grafico == 'Categorias de cancelamento':

    dados = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Category']
        .value_counts()
        .rename(index=traducao_categorias)
        .reset_index()
    )

    dados.columns = [
        'Categoria',
        'Quantidade de clientes'
    ]

    grafico = px.bar(
        dados,
        x='Quantidade de clientes',
        y='Categoria',
        orientation='h',
        title='Cancelamentos por categoria',
        text='Quantidade de clientes'
    )

    grafico.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )

# --- Principais motivos --- #
elif sel_grafico == 'Principais motivos de cancelamento':

    dados = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Reason']
        .value_counts()
        .head(10)
        .rename(index=traducao_motivos)
        .reset_index()
    )

    dados.columns = [
        'Motivo',
        'Quantidade de clientes'
    ]

    grafico = px.bar(
        dados,
        x='Quantidade de clientes',
        y='Motivo',
        orientation='h',
        title='Principais motivos de cancelamento',
        text='Quantidade de clientes'
    )

    grafico.update_layout(
        yaxis={'categoryorder': 'total ascending'}
    )

# --- Taxa de churn por contrato --- #
else:
    dados = (
        df
        .assign(Cancelou=df['Churn Label'] == 'Yes')
        .groupby('Contract')['Cancelou']
        .mean()
        .mul(100)
        .sort_values(ascending=False)
        .rename(index=traducao_contratos)
        .reset_index()
    )

    dados.columns = [
        'Tipo de contrato',
        'Taxa de churn'
    ]

    grafico = px.bar(
        dados,
        x='Tipo de contrato',
        y='Taxa de churn',
        title='Taxa de churn por tipo de contrato',
        text='Taxa de churn'
    )

    grafico.update_traces(
        texttemplate='%{text:.1f}%',
        textposition='outside'
    )

    grafico.update_yaxes(
        title='Taxa de churn (%)'
    )

# --- Mostrar os gráficos --- #
st.plotly_chart(
    grafico,
    use_container_width=True
)

# --- Rodapé --- #
st.divider()

st.caption('Análise elaborada pela JZ Data Analytics')