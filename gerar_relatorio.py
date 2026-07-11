# --- Importar as traduções do projeto --- #
from traducao import (
    traducao_categorias,
    traducao_motivos,
    traducao_contratos
)

# --- Gerar o relatório escrito --- #
def gerar_relatorio(df):

# --- Indicadores gerais --- #
    total_clientes = len(df)

    clientes_cancelados = (
        df['Churn Label']
        .eq('Yes')
        .sum()
    )

    taxa_churn = (
        clientes_cancelados
        / total_clientes
        * 100
    )

    # --- Separar somente os clientes que cancelaram --- #
    clientes_que_cancelaram = (
        df[df['Churn Label'] == 'Yes']
    )

    # --- Analisar as categorias de cancelamento --- #
    categorias_cancelamento = (
        clientes_que_cancelaram['Churn Category']
        .value_counts()
    )

    principal_categoria = categorias_cancelamento.index[0]

    quantidade_principal_categoria = (
        categorias_cancelamento.iloc[0]
    )

    percentual_principal_categoria = (
        quantidade_principal_categoria
        / clientes_cancelados
        * 100
    )

    principal_categoria = traducao_categorias.get(
        principal_categoria,
        principal_categoria
    )

    # --- Identificar os principais motivos --- #
    principais_motivos = (
        clientes_que_cancelaram['Churn Reason']
        .value_counts()
        .head(5)
    )

    lista_motivos = []

    for motivo, quantidade in principais_motivos.items():

        motivo_traduzido = traducao_motivos.get(
            motivo,
            motivo
        )

        percentual_motivo = (
            quantidade
            / clientes_cancelados
            * 100
        )

        lista_motivos.append(
            f'- {motivo_traduzido}: '
            f'{quantidade} clientes '
            f'({percentual_motivo:.1f}% dos cancelamentos)'
        )

    texto_motivos = '\n'.join(lista_motivos)

    # --- Calcular a taxa de churn por contrato --- #
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

    contrato_maior_churn = traducao_contratos.get(
        contrato_maior_churn,
        contrato_maior_churn
    )

# --- Montar o relatório completo --- #
    relatorio = f"""
1. RESUMO GERAL

A base analisada possui {total_clientes:,} clientes.

Foram identificados {clientes_cancelados:,} cancelamentos,
o que representa uma taxa de churn de {taxa_churn:.2f}%.


2. PRINCIPAIS DESCOBERTAS

A categoria {principal_categoria} concentrou
{quantidade_principal_categoria} cancelamentos,
representando {percentual_principal_categoria:.1f}%
do total de clientes que deixaram a empresa.

Os principais motivos específicos de cancelamento foram:

{texto_motivos}

Os resultados mostram que os cancelamentos estão
relacionados principalmente à competitividade das ofertas,
à qualidade dos serviços oferecidos e à experiência de
atendimento dos clientes.

O tipo de contrato também apresenta influência importante.
Os clientes com contrato {contrato_maior_churn} apresentaram
a maior taxa de churn, equivalente a
{taxa_maior_contrato:.1f}%.


3. RECOMENDAÇÕES

- Criar campanhas de retenção para clientes com contrato mensal;
- Revisar preços, benefícios e ofertas em relação à concorrência;
- Avaliar a qualidade dos equipamentos e serviços oferecidos;
- Melhorar o atendimento prestado pelo suporte;
- Oferecer benefícios para a migração do contrato mensal para contratos mais longos;
- Monitorar clientes com baixa satisfação;
- Criar ofertas personalizadas para clientes com maior risco;
- Acompanhar continuamente os principais motivos de cancelamento.


4. CONCLUSÃO

A análise mostra que a concorrência possui forte influência
sobre os cancelamentos, principalmente por oferecer melhores
equipamentos, condições comerciais e benefícios.

Além disso, fatores relacionados ao atendimento, à qualidade
dos serviços e ao tipo de contrato também contribuem para o churn.

O acompanhamento desses indicadores pode auxiliar a empresa
na criação de estratégias de retenção mais eficientes e na
melhoria da experiência dos clientes.


Atenciosamente,

JZ Data Analytics
Jordana Zatta Prado
"""

    return relatorio