# --- Importar o Streamlit --- #
import streamlit as st

# --- Configurações da página --- #
st.set_page_config(
    page_title='Análise de Churn',
    page_icon='📊',
    layout='wide'
)

# --- Inserir o nome do usuário na sessão --- #
if 'nome_usuario' not in st.session_state:
    st.session_state.nome_usuario = ''

# --- Campo para o nome do usuário na sidebar --- #
nome = st.sidebar.text_input(
    label='Digite seu nome:',
    value=st.session_state.nome_usuario
)

# --- Salvar o nome na sessão --- #
st.session_state.nome_usuario = nome

# --- Criar as páginas da aplicação --- #
pagina_inicial = st.Page(
    'pages/home.py',
    title='Página Inicial',
    icon='🏠'
)
visao_geral = st.Page(
    'pages/visao_geral.py',
    title='Visão Geral',
    icon='📈'
)
tabelas = st.Page(
    'pages/tabelas.py',
    title='Tabelas',
    icon='📋'
)
graficos_estaticos = st.Page(
    'pages/graficos_estaticos.py',
    title='Gráficos Estáticos',
    icon='📊'
)
graficos_interativos = st.Page(
    'pages/graficos_interativos.py',
    title='Gráficos Interativos',
    icon='🌐'
)
relatorio = st.Page(
    'pages/relatorio.py',
    title='Relatório',
    icon='📝'
)
email = st.Page(
    'pages/email.py',
    title='Enviar E-mail',
    icon='📧'
)

# --- Criar a navegação --- #
navegacao = st.navigation(
    [
        pagina_inicial,
        visao_geral,
        tabelas,
        graficos_estaticos,
        graficos_interativos,
        relatorio,
        email
    ],
    position='sidebar'
)

# --- Executar a página selecionada --- #
navegacao.run()