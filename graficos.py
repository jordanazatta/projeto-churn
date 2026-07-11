# --- Importar as bibliotecas --- #
import matplotlib.pyplot as plt
import seaborn as sns

# --- Traduções --- #
from traducao import (
    traducao_categorias,
    traducao_motivos,
    traducao_contratos,
    traducao_churn
)

# --- Criando os gráficos --- #
class Graficos:

    def __init__(self, df):
        self.df = df

    def situacao_clientes(self): # cria o gráfico de clientes cancelados e não cancelados

        dados = (
            self.df['Churn Label']
            .value_counts()
            .rename(index=traducao_churn)
        )

        fig, ax = plt.subplots(figsize=(8, 5))

        sns.barplot(
            x=dados.index,
            y=dados.values,
            ax=ax
        )

        ax.set_title('Situação dos clientes')
        ax.set_xlabel('')
        ax.set_ylabel('Quantidade de clientes')

        for indice, valor in enumerate(dados.values):
            ax.text(
                indice,
                valor,
                f'{valor:,}'.replace(',', '.'),
                ha='center',
                va='bottom'
            )

        fig.tight_layout()
        return fig

    def categorias_cancelamento(self): # cria o gráfico das categorias de cancelamento

        dados = (
            self.df[self.df['Churn Label'] == 'Yes']
            ['Churn Category']
            .value_counts()
        )
        dados = dados.rename(index=traducao_categorias)

        fig, ax = plt.subplots(figsize=(9, 5))

        sns.barplot(
            x=dados.values,
            y=dados.index,
            ax=ax
        )

        ax.set_title('Cancelamentos por categoria')
        ax.set_xlabel('Quantidade de clientes')
        ax.set_ylabel('')

        fig.tight_layout()
        return fig

    def principais_motivos(self): # cria o gráfico dos principais motivos de cancelamento

        dados = (
            self.df[self.df['Churn Label'] == 'Yes']
            ['Churn Reason']
            .value_counts()
            .head(10)
        )
        dados = dados.rename(index=traducao_motivos)

        fig, ax = plt.subplots(figsize=(10, 6))

        sns.barplot(
            x=dados.values,
            y=dados.index,
            ax=ax
        )

        ax.set_title('Principais motivos de cancelamento')
        ax.set_xlabel('Quantidade de clientes')
        ax.set_ylabel('')

        fig.tight_layout()
        return fig

    def churn_por_contrato(self): # calcula a taxa de churn por tipo de contrato
        dados = (
            self.df
            .assign(Cancelou=self.df['Churn Label'] == 'Yes')
            .groupby('Contract')['Cancelou']
            .mean()
            .mul(100)
            .sort_values(ascending=False)
        )
        dados = dados.rename(index=traducao_contratos)

        fig, ax = plt.subplots(figsize=(9, 5))

        sns.barplot(
            x=dados.index,
            y=dados.values,
            ax=ax
        )

        ax.set_title('Taxa de churn por tipo de contrato')
        ax.set_xlabel('Tipo de contrato')
        ax.set_ylabel('Taxa de churn (%)')

        for indice, valor in enumerate(dados.values):
            ax.text(
                indice,
                valor,
                f'{valor:.1f}%',
                ha='center',
                va='bottom'
            )

        fig.tight_layout()

        return fig