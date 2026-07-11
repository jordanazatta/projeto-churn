# --- Importar o Streamlit --- #
import streamlit as st

# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get('nome_usuario', '')

# --- Mostrar o logo --- #
coluna_logo, coluna_espaco = st.columns([1, 2])

with coluna_logo:
    st.image(
        'imagens/logo.png',
        width=450
    )

# --- Saudação --- #
if nome_usuario:
    st.subheader(f'Olá, {nome_usuario}! Seja bem-vindo(a).')
else:
    st.subheader('Bem-vindo(a)!')

# --- Resumo --- #
st.header('Análise de Cancelamento dos Clientes')
st.write(
    'Esse projeto foi desenvolvido para analisar os cancelamentos '
    'dos clientes de uma empresa de telecomunicações.'
)
st.write(
    'O objetivo é identificar os principais motivos dos cancelamentos, '
    'avaliar o perfil dos clientes que realizaram os cancelamentos e apresentar '
    'informações que auxiliem a empresa na tomada de decisão.'
)

# --- Divisor --- #
st.divider()

# --- Informações sobre a base --- #
st.subheader('Sobre a base de dados')

coluna_1, coluna_2, coluna_3 = st.columns(3)

with coluna_1:
    st.metric(
        label='Clientes analisados',
        value='7.043'
    )
with coluna_2:
    st.metric(
        label='Colunas da base de dados',
        value=50
    )
with coluna_3:
    st.metric(
        label='Segmento',
        value='Telecomunicações'
    )

# --- Separador --- #
st.divider()

# --- Conteúdo disponível --- #
st.subheader('Objetivos da análise')
st.markdown(
    '''
    - Identificar quantos clientes cancelaram os serviços;
    - Calcular a taxa de churn;
    - Analisar os principais motivos dos cancelamentos;
    - Avaliar características dos clientes que cancelaram;
    - Apresentar tabelas e gráficos;
    - Gerar um relatório com insights e recomendações;
    - Permitir o envio de gráficos ou relatório por e-mail.
    '''
)

# --- Orientação --- #
if not nome_usuario:
    st.info(
        'Digite seu nome no campo da barra lateral para personalizar '
        'a navegação pela aplicação.'
    )

# --- Rodapé --- #
st.divider()
st.caption(
    'Projeto desenvolvido por Jordana Zatta Prado | JZ Data Analytics'
)