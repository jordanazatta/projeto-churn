# --- Função responsável por gerar o relatório --- #
def gerar_relatorio(df):

# --- Indicadores gerais --- #
    total_clientes = len(df)

    clientes_cancelados = (
        df['Churn Label']
        .eq('Yes')
        .sum()
    )

    taxa_churn = (
        clientes_cancelados / total_clientes * 100
    )

# --- Principais categorias de cancelamento --- #
    categorias = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Category']
        .value_counts()
    )

    principal_categoria = categorias.index[0]
    quantidade_categoria = categorias.iloc[0]

    traducao_categoria = {
        'Competitor': 'Concorrência',
        'Attitude': 'Atendimento',
        'Dissatisfaction': 'Insatisfação',
        'Price': 'Preço',
        'Other': 'Outros'
    }

    principal_categoria = traducao_categoria.get(
        principal_categoria,
        principal_categoria
    )

# --- Principal motivo específico --- #
    motivos = (
        df[df['Churn Label'] == 'Yes']
        ['Churn Reason']
        .value_counts()
    )

    principal_motivo = motivos.index[0]
    quantidade_motivo = motivos.iloc[0]

    traducao_motivo = {
        'Competitor had better devices':
            'concorrente com melhores equipamentos',
        'Competitor made better offer':
            'concorrente com melhor oferta',
        'Attitude of support person':
            'atendimento prestado pelo suporte',
        "Don't know":
            'motivo não informado',
        'Competitor offered more data':
            'concorrente oferecendo maior volume de dados',
        'Competitor offered higher download speeds':
            'concorrente oferecendo maior velocidade',
        'Price too high':
            'preço considerado elevado',
        'Product dissatisfaction':
            'insatisfação com o serviço',
        'Network reliability':
            'problemas relacionados à rede'
    }

    principal_motivo = traducao_motivo.get(
        principal_motivo,
        principal_motivo
    )

# --- Taxa de churn por contrato --- #
    churn_contrato = (
        df
        .assign(Cancelou=df['Churn Label'] == 'Yes')
        .groupby('Contract')['Cancelou']
        .mean()
        .mul(100)
        .sort_values(ascending=False)
    )

    maior_contrato = churn_contrato.index[0]
    maior_taxa_contrato = churn_contrato.iloc[0]

    traducao_contrato = {
        'Month-to-Month': 'mensal',
        'One Year': 'anual',
        'Two Year': 'de dois anos'
    }

    maior_contrato = traducao_contrato.get(
        maior_contrato,
        maior_contrato
    )

# --- Montar o relatório --- #
    relatorio = f"""
1. RESUMO GERAL

A base analisada contém {total_clientes:,} clientes.
Desse total, {clientes_cancelados:,} cancelaram os serviços,
resultando em uma taxa de churn de {taxa_churn:.2f}%.

2. PRINCIPAIS DESCOBERTAS

A categoria de cancelamento com maior ocorrência foi
{principal_categoria}, responsável por {quantidade_categoria:,}
cancelamentos.

O motivo específico mais frequente foi relacionado a
{principal_motivo}, registrado por {quantidade_motivo:,} clientes.

Os clientes com contrato {maior_contrato} apresentaram a maior
taxa de churn, equivalente a {maior_taxa_contrato:.1f}%.

Também foi observado que clientes com menor satisfação e menor
tempo de permanência apresentam maior chance de cancelamento.

3. RECOMENDAÇÕES

- Criar ações de retenção para os clientes que possuem contratos mensais;
- Revisar preços, ofertas e benefícios em comparação à concorrência;
- Oferecer vantagens para a migração dos contratos mensais para contratos anuais;
- Melhorar a qualidade do suporte e do atendimento ao cliente;
- Monitorar clientes com baixa satisfação;
- Priorizar clientes com alto valor de vida (CLTV);
- Desenvolver ofertas personalizadas para clientes com maior risco.

4. CONCLUSÃO

A empresa apresenta uma taxa de churn relevante, concentrada 
principalmente em fatores relacionados à concorrência, ao tipo
de contrato, à satisfação e à experiência do cliente.

O acompanhamento desses indicadores pode ajudar a empresa a
antecipar cancelamentos e desenvolver estratégias de retenção
mais eficientes.

Atenciosamente,

JZ Data Analytics
Jordana Zatta Prado
"""

    return relatorio