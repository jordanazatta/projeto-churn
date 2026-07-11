# --- Importar o Streamlit --- #
import streamlit as st

# --- Importar os módulos do projeto --- #
from carregar_dados import carregar_dados
from gerar_relatorio import gerar_relatorio
from traducao import traducao_motivos

# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get(
    'nome_usuario',
    ''
)

# --- Saudação --- #
if nome_usuario:
    st.write(f'Olá, {nome_usuario}!')
else:
    st.write('Olá!')

# --- Título --- #
st.title('Relatório Gerencial')

st.write(
    'Nesta página é apresentado um resumo das principais '
    'descobertas e recomendações obtidas por meio das análises.'
)

# --- Carregar os dados --- #
df = carregar_dados()

# --- Gerar o relatório --- #
relatorio = gerar_relatorio(df)

# --- Indicadores para exibição --- #
total_clientes = len(df)

clientes_cancelados = (
    df['Churn Label']
    .eq('Yes')
    .sum()
)
taxa_churn = (
    clientes_cancelados / total_clientes * 100
)

# --- Separar os clientes que cancelaram --- #
clientes_que_cancelaram = (
    df[df['Churn Label'] == 'Yes']
)

# --- Calcular as categorias de cancelamento --- #
categorias_cancelamento = (
    clientes_que_cancelaram['Churn Category']
    .value_counts()
)

# --- Identificar a principal categoria --- #
principal_categoria = categorias_cancelamento.index[0]

quantidade_principal_categoria = (
    categorias_cancelamento.iloc[0]
)

percentual_principal_categoria = (
    quantidade_principal_categoria
    / clientes_cancelados
    * 100
)

traducao_categoria = {
    'Competitor': 'Concorrência',
    'Attitude': 'Atendimento',
    'Dissatisfaction': 'Insatisfação',
    'Price': 'Preço',
    'Other': 'Outros'
}

# --- Principais motivos de cancelamento --- #
principais_motivos = (
    clientes_que_cancelaram['Churn Reason']
    .value_counts()
    .head(5)
)

# --- Criar uma lista com os motivos traduzidos --- #
lista_motivos = []

for motivo, quantidade in principais_motivos.items():

    motivo_traduzido = traducao_motivos.get(
        motivo,
        motivo
    )

    percentual = (
        quantidade
        / clientes_cancelados
        * 100
    )

    lista_motivos.append(
        f'- **{motivo_traduzido}**: '
        f'{quantidade} clientes '
        f'({percentual:.1f}% dos cancelamentos);'
    )

# --- Juntar os motivos em um único texto --- #
texto_motivos = '\n'.join(lista_motivos)

principal_categoria = traducao_categoria.get(
    principal_categoria,
    principal_categoria
)

# --- Maior taxa de churn por contrato --- #
churn_contrato = (
    df
    .assign(Cancelou=df['Churn Label'] == 'Yes')
    .groupby('Contract')['Cancelou']
    .mean()
    .mul(100)
    .sort_values(ascending=False)
)

contrato_maior_churn = churn_contrato.index[0]
taxa_maior_contrato = churn_contrato.iloc[0]

traducao_contrato = {
    'Month-to-Month': 'Mensal',
    'One Year': '1 Ano',
    'Two Year': '2 Anos'
}

contrato_maior_churn = traducao_contrato.get(
    contrato_maior_churn,
    contrato_maior_churn
)

# --- Mostrar o resumo --- #
st.markdown("##### 📄 Resumo Geral")

st.success(
    f'''
    A base possui **{total_clientes:,} clientes**.

    Foram identificados **{clientes_cancelados:,} cancelamentos**,
    o que representa uma taxa de churn de **{taxa_churn:.2f}%**.

    A principal categoria de cancelamento foi **{principal_categoria}**.
    '''
)

# --- Mostrar as principais descobertas --- #
st.markdown('### 📊 Principais descobertas')

st.info(
    f'''
A taxa de churn identificada foi de **{taxa_churn:.2f}%**,
representando **{clientes_cancelados:,} clientes cancelados**.

A categoria **{principal_categoria}** apresentou
**{quantidade_principal_categoria} cancelamentos**,
o equivalente a **{percentual_principal_categoria:.1f}%**
de todos os clientes que deixaram a empresa.

Os principais motivos específicos de cancelamento foram:

{texto_motivos}

Além dos motivos informados pelos clientes, o tipo de contrato
também apresenta influência importante. Os clientes com contrato
**{contrato_maior_churn}** apresentaram a maior taxa de churn,
com **{taxa_maior_contrato:.1f}%**.

Os resultados indicam que os cancelamentos estão relacionados
principalmente à competitividade das ofertas, à qualidade dos
serviços e à experiência do atendimento.
    '''
)

# --- Mostrar as recomendações --- #
st.markdown("##### ✅ Recomendações")

st.warning(
    '''
    - Criar campanhas de retenção para clientes com contratos mensais;
    - Incentivar a migração dos contratos mensais para contratos anuais;
    - Revisar preços, ofertas e benefícios em relação à concorrência;
    - Melhorar a qualidade do atendimento e do suporte;
    - Acompanhar os clientes com baixa satisfação;
    - Priorizar clientes com alto valor de vida (CLTV);
    - Desenvolver ofertas personalizadas para clientes com maior risco.
    '''
)

# --- Arquivo para download --- #
arquivo_txt = relatorio.encode('utf-8')

# --- Botão de download --- #
st.download_button(
    label='Baixar relatório em TXT',
    data=arquivo_txt,
    file_name='relatorio_analise_churn.txt',
    mime='text/plain',
    use_container_width=True
)

# --- Rodapé --- #
st.divider()

st.caption(
    'Análise elaborada pela JZ Data Analytics'
)