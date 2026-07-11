# --- Importar as bibliotecas --- #
import smtplib

from email.mime.application import MIMEApplication
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# --- Função responsável pelo envio do e-mail --- #
def enviar_email(
        remetente,
        senha,
        destinatario,
        assunto,
        corpo,
        anexo,
        nome_anexo,
        tipo_anexo
):
    try:
# --- Criar a mensagem de e-mail --- #
        mensagem = MIMEMultipart()

        mensagem['From'] = remetente
        mensagem['To'] = destinatario
        mensagem['Subject'] = assunto

# --- Adicionar o corpo do e-mail --- #
        mensagem.attach(
            MIMEText(
                corpo,
                'plain',
                'utf-8'
            )
        )

# --- Preparar o anexo de imagem --- #
        if tipo_anexo == 'imagem':
            arquivo = MIMEImage(
                anexo,
                _subtype='png'
            )

# --- Preparar o anexo de texto --- #
        else:
            arquivo = MIMEApplication(
                anexo,
                _subtype='txt'
            )

# --- Adicionar o nome do arquivo anexado --- #
        arquivo.add_header(
            'Content-Disposition',
            'attachment',
            filename=nome_anexo
        )
        mensagem.attach(arquivo)

# --- Conectar ao servidor do Gmail --- #
        servidor = smtplib.SMTP(
            'smtp.gmail.com',
            587
        )

        servidor.starttls()

        servidor.login(
            remetente,
            senha
        )

# --- Enviar a mensagem --- #
        servidor.send_message(mensagem)

        servidor.quit()

        return True, 'E-mail enviado com sucesso!'

    except Exception as erro:
        return False, f'Não foi possível enviar o e-mail: {erro}'