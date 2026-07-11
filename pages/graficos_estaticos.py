# --- Importar as bibliotecas --- #
import streamlit as st
import matplotlib.pyplot as plt

# --- Importar os módulos do projeto --- #
from carregar_dados import carregar_dados
from graficos import Graficos

# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get('nome_usuario', '')

# --- Saudação --- #
if nome_usuario:
    st.write(f'Olá, {nome_usuario}!')
else:
    st.write('Olá!')

# --- Título --- #
st.title('Gráficos Estáticos')

st.write(
    'Selecione um gráfico para visualizar informações relacionadas '
    'ao cancelamento dos clientes.'
)

# --- Carregar os dados --- #
df = carregar_dados()

graficos = Graficos(df)

# --- Seleção do gráfico --- #
sel_grafico = st.selectbox(
    label='Selecione o gráfico:',
    options=[
        'Situação dos clientes',
        'Categorias de cancelamento',
        'Principais motivos de cancelamento',
        'Churn por tipo de contrato'
    ]
)

# --- Gerar os gráficos --- #
if sel_grafico == 'Situação dos clientes':
    figura = graficos.situacao_clientes()

elif sel_grafico == 'Categorias de cancelamento':
    figura = graficos.categorias_cancelamento()
        

elif sel_grafico == 'Principais motivos de cancelamento':
    figura = graficos.principais_motivos()

else:
    figura = graficos.churn_por_contrato()

# --- Mostrar os gráficos --- #
st.pyplot(
    figura,
    use_container_width=True
)

plt.close(figura)

# --- Rodapé --- #
st.divider()

st.caption('Análise elaborada pela JZ Data Analytics')