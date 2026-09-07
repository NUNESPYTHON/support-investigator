"""
==========================================================
Zendesk Investigator

Arquivo:
email.py

Responsabilidade:
Enviar arquivos por e-mail utilizando SMTP.

Autor:
Elias Nunes
==========================================================
"""

import os
import smtplib
import traceback
from email.message import EmailMessage
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()


def enviar_arquivo_email(
    caminho_arquivo,
    destinatario,
    assunto,
    corpo,
):
    """
    Envia um arquivo por e-mail.

    Args:
        caminho_arquivo (str): Caminho do arquivo a anexar.
        destinatario (str): E-mail que receberá a mensagem.
        assunto (str): Assunto do e-mail.
        corpo (str): Corpo da mensagem.

    Returns:
        bool: True em caso de sucesso, False em caso de erro.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    if not all(
        [
            smtp_host,
            smtp_port,
            smtp_user,
            smtp_password,
        ]
    ):
        print("Configuração SMTP incompleta.")
        return False

    arquivo = Path(caminho_arquivo)

    if not arquivo.exists():
        print("Arquivo para envio não encontrado.")
        return False

    mensagem = EmailMessage()

    mensagem["From"] = smtp_user
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    mensagem.set_content(corpo)

    mensagem.add_attachment(
        arquivo.read_bytes(),
        maintype="text",
        subtype="csv",
        filename=arquivo.name,
    )

    try:
        with smtplib.SMTP_SSL(
            smtp_host,
            int(smtp_port),
            timeout=20,
        ) as servidor:

            servidor.login(
                smtp_user,
                smtp_password,
            )

            servidor.send_message(
                mensagem
            )

        return True

    except Exception:
        traceback.print_exc()
        return False