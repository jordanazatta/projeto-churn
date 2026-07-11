# --- Importar as bibliotecas --- #
import streamlit as st

# --- Importar a função de carregamento dos dados --- #
from carregar_dados import carregar_dados

# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get('nome_usuario', '')

# --- Saudação --- #
if nome_usuario:
    st.write(f'Olá, {nome_usuario}!')
else:
    st.write('Olá!')

# --- Título --- #
st.title('Consulta das Tabelas')

# --- Carregar os dados --- #
df = carregar_dados()

# --- Selecionar a tabela que será exibida --- #
sel_tabela = st.selectbox(
    label='Selecione a análise desejada:',
    options=[
        'Base completa',
        'Clientes que cancelaram',
        'Resumo por categoria de cancelamento',
        'Resumo por motivo de cancelamento'
    ]
)

# --- Mostrar a base completa --- #
if sel_tabela == 'Base completa':
    st.subheader('Base completa de clientes')
    st.info(
        "A tabela abaixo apresenta todos os clientes disponíveis na base de dados."
    )
    st.dataframe(
        df,
        use_container_width=True
    )

# --- Clientes que cancelaram --- #
elif sel_tabela == 'Clientes que cancelaram':
    st.subheader('Clientes que cancelaram os serviços')

    clientes_cancelados = df[df['Churn Label'] == 'Yes']
    st.dataframe(
        clientes_cancelados,
        use_container_width=True
    )

# --- Resumo por categoria --- #
elif sel_tabela == 'Resumo por categoria de cancelamento':
    st.subheader('Cancelamentos por categoria')
    st.info(
        'Esta tabela apresenta as categorias relacionadas aos cancelamentos dos clientes.'
    )
    resumo_categoria = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Category']
        .value_counts()
        .reset_index()
    )
    resumo_categoria.columns = [
        'Categoria do cancelamento',
        'Quantidade de clientes'
    ]
    st.dataframe(
        resumo_categoria,
        use_container_width=True,
        hide_index=True
    )

# --- Resumo por motivo --- #
elif sel_tabela == 'Resumo por motivo de cancelamento':
    st.subheader('Cancelamentos por motivo')
    st.info(
        'Esta tabela apresenta os motivos informados '
        'pelos clientes que cancelaram os serviços.'
    )
    resumo_motivo = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Reason']
        .value_counts()
        .reset_index()
    )
    resumo_motivo.columns = [
        'Motivo do cancelamento',
        'Quantidade de clientes'
    ]
    st.dataframe(
        resumo_motivo,
        use_container_width=True,
        hide_index=True
    )

# --- Rodapé --- #
st.divider()

st.caption('Análise elaborada pela JZ Data Analytics')