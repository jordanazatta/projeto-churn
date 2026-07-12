# --- Importar as bibliotecas --- #
import io

import matplotlib.pyplot as plt
import streamlit as st

# --- Importar os módulos do projeto --- #
from carregar_dados import carregar_dados
from enviar_email import enviar_email
from gerar_relatorio import gerar_relatorio
from graficos import Graficos


# --- Obter o nome do usuário --- #
nome_usuario = st.session_state.get(
    'nome_usuario',
    ''
)

# --- Saudação --- #
if nome_usuario:
    st.write(f'Olá, {nome_usuario}!')
else:
    st.write('Bem-vindo(a)!')

# --- Título --- #
st.title('Enviar por E-mail')

st.write(
    'Nesta página você pode enviar um gráfico estático ou o '
    'relatório gerencial para o endereço de e-mail desejado.'
)

# --- Carregar os dados --- #
df = carregar_dados()

# --- Escolher o conteúdo do e-mail --- #
tipo_envio = st.radio(
    label='O que deseja enviar?',
    options=[
        'Gráfico estático',
        'Relatório gerencial'
    ],
    horizontal=True
)

# --- Selecionar o gráfico --- #
if tipo_envio == 'Gráfico estático':

    grafico_selecionado = st.selectbox(
        label='Selecione o gráfico:',
        options=[
            'Situação dos clientes',
            'Categorias de cancelamento',
            'Principais motivos de cancelamento',
            'Churn por tipo de contrato'
        ]
    )

# --- Aviso sobre o recebimento do e-mail --- #
st.info(
    'O e-mail pode ser direcionado para a caixa de spam ou lixo eletrônico. '
    'Caso não apareça na caixa de entrada, verifique essas pastas.'
)

# --- Formulário do e-mail --- #
with st.form('formulario_email'):

    destinatario = st.text_input(
        label='E-mail do destinatário:*',
        placeholder='exemplo@email.com'
    )

    confirmar = st.checkbox(
        'Confirmo que desejo enviar este conteúdo.'
    )

    enviar = st.form_submit_button(
        label='Enviar E-mail',
        use_container_width=True
    )

# --- Verificar se o botão foi clicado --- #
if enviar:

    if not destinatario:
        st.warning(
            'Digite o e-mail do destinatário.'
        )

    elif not confirmar:
        st.warning(
            'Marque a confirmação antes de enviar.'
        )

    else:
        try:
# --- Ler as credenciais protegidas --- #
            remetente = st.secrets['REMETENTE']
            senha = st.secrets['SENHA']

        except Exception:
            st.error(
                'As credenciais não foram encontradas. '
                'Confira o arquivo .streamlit/secrets.toml.'
            )

            st.stop()


        with st.spinner('Preparando e enviando o e-mail...'):

# --- Enviar um gráfico --- #
            if tipo_envio == 'Gráfico estático':

                graficos = Graficos(df)

                if grafico_selecionado == 'Situação dos clientes':
                    figura = graficos.situacao_clientes()
                    nome_anexo = 'situacao_clientes.png'

                elif grafico_selecionado == 'Categorias de cancelamento':
                    figura = graficos.categorias_cancelamento()
                    nome_anexo = 'categorias_cancelamento.png'

                elif grafico_selecionado == 'Principais motivos de cancelamento':
                    figura = graficos.principais_motivos()
                    nome_anexo = 'principais_motivos_cancelamento.png'

                else:
                    figura = graficos.churn_por_contrato()
                    nome_anexo = 'churn_por_contrato.png'


# --- Salvar o gráfico na memória --- #
                buffer = io.BytesIO()

                figura.savefig(
                    buffer,
                    format='png',
                    bbox_inches='tight'
                )

                buffer.seek(0)

                anexo = buffer.getvalue()

                plt.close(figura)


# --- Assunto padronizado --- #
                assunto = (
                    'JZ Data Analytics - '
                    'Gráfico de Análise de Churn'
                )


# --- Corpo padronizado --- #
                corpo = f'''
Olá,

Segue em anexo o gráfico "{grafico_selecionado}", elaborado
a partir da análise dos dados de cancelamento dos clientes.

O gráfico apresenta informações que podem auxiliar na
identificação dos principais fatores relacionados ao churn.

Atenciosamente,

JZ Data Analytics
Jordana Zatta Prado
'''


                sucesso, mensagem = enviar_email(
                    remetente=remetente,
                    senha=senha,
                    destinatario=destinatario,
                    assunto=assunto,
                    corpo=corpo,
                    anexo=anexo,
                    nome_anexo=nome_anexo,
                    tipo_anexo='imagem'
                )


# --- Enviar o relatório --- #
            else:
                relatorio = gerar_relatorio(df)

                anexo = relatorio.encode('utf-8')

                nome_anexo = 'relatorio_analise_churn.txt'

                assunto = (
                    'JZ Data Analytics - '
                    'Relatório de Análise de Churn'
                )

                corpo = '''
Olá,

Segue em anexo o relatório gerencial elaborado a partir
da análise dos dados de cancelamento dos clientes.

O documento apresenta os principais resultados identificados
e recomendações que podem auxiliar a empresa na redução da taxa de cancelamento
e na retenção dos clientes.

Atenciosamente,

JZ Data Analytics
Jordana Zatta Prado
'''


                sucesso, mensagem = enviar_email(
                    remetente=remetente,
                    senha=senha,
                    destinatario=destinatario,
                    assunto=assunto,
                    corpo=corpo,
                    anexo=anexo,
                    nome_anexo=nome_anexo,
                    tipo_anexo='texto'
                )


# --- Mostrar o resultado --- #
            if sucesso:
                st.success(
                    'E-mail enviado com sucesso! '
                    'Caso não apareça na caixa de entrada, verifique a pasta de spam '
                    'ou lixo eletrônico.')

            else:
                st.error(mensagem)

# --- Rodapé --- #
st.divider()

st.caption(
    'Compartilhamento realizado pela JZ Data Analytics'
)