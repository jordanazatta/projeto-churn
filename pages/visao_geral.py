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

# --- Título da página --- #
st.title('Panorama Geral')

# --- Carregar os dados --- #
df = carregar_dados()

# --- Calcular os indicadores principais --- #
total_clientes = len(df)

clientes_cancelados = df['Churn Label'].eq('Yes').sum()

clientes_ativos = total_clientes - clientes_cancelados

taxa_churn = clientes_cancelados / total_clientes * 100

# --- Mostrar os indicadores --- #
coluna_1, coluna_2, coluna_3, coluna_4 = st.columns(4)

with coluna_1:
    st.metric(
        label='Total de Clientes',
        value=f'{total_clientes:,}'.replace(',', '.')
    )
with coluna_2:
    st.metric(
        label='Clientes Cancelados',
        value=f'{clientes_cancelados:,}'.replace(',', '.')
    )
with coluna_3:
    st.metric(
        label='Clientes Ativos',
        value=f'{clientes_ativos:,}'.replace(',', '.')
    )
with coluna_4:
    st.metric(
        label='Taxa de Churn',
        value=f'{taxa_churn:.2f}%'
    )

# --- Divisor --- #
st.divider()

# --- Principais descobertas --- #
st.subheader('Principais descobertas')

st.markdown(
    '''
    - A taxa de churn é de **26,54%**;
    - A categoria **Concorrente** concentra a maior parte dos cancelamentos;
    - Clientes com contrato mensal apresentam maior risco de cancelamento;
    - Clientes com menor satisfação tendem a cancelar com mais frequência;
    - Clientes com menor tempo de permanência também apresentam maior chance de cancelamento.
    '''
)

# --- Divisor --- #
st.divider()

# --- Identidade da análise --- #
st.caption('Análise elaborada pela JZ Data Analytics')