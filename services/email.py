"""
==========================================================
Support Investigator

Arquivo:
email.py

Responsabilidade:
Enviar arquivos por e-mail utilizando SMTP.

Autor:
Elias Nunes
==========================================================
"""

import mimetypes
import os
import smtplib
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
    Envia um arquivo por e-mail utilizando SMTP.

    Args:
        caminho_arquivo (str): Caminho do arquivo.
        destinatario (str): E-mail do destinatário.
        assunto (str): Assunto da mensagem.
        corpo (str): Corpo da mensagem.

    Returns:
        bool: True em caso de sucesso, False em caso de erro.
    """

    smtp_host = os.getenv("SMTP_HOST")
    smtp_port = os.getenv("SMTP_PORT")
    smtp_user = os.getenv("SMTP_USER")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # ------------------------------------------------------
    # VALIDAR CONFIGURAÇÃO
    # ------------------------------------------------------

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

    # ------------------------------------------------------
    # VALIDAR ARQUIVO
    # ------------------------------------------------------

    arquivo = Path(caminho_arquivo)

    if not arquivo.exists():
        print(
            f"Arquivo para envio não encontrado: "
            f"{arquivo}"
        )
        return False

    # ------------------------------------------------------
    # CRIAR MENSAGEM
    # ------------------------------------------------------

    mensagem = EmailMessage()

    mensagem["From"] = smtp_user
    mensagem["To"] = destinatario
    mensagem["Subject"] = assunto

    mensagem.set_content(corpo)

    # ------------------------------------------------------
    # IDENTIFICAR TIPO DO ARQUIVO
    # ------------------------------------------------------

    mime_type, _ = mimetypes.guess_type(
        arquivo.name
    )

    if mime_type:
        maintype, subtype = mime_type.split(
            "/",
            1,
        )
    else:
        maintype = "application"
        subtype = "octet-stream"

    # ------------------------------------------------------
    # ADICIONAR ANEXO
    # ------------------------------------------------------

    mensagem.add_attachment(
        arquivo.read_bytes(),
        maintype=maintype,
        subtype=subtype,
        filename=arquivo.name,
    )

    # ------------------------------------------------------
    # ENVIO SMTP
    # ------------------------------------------------------

    try:

        print(
            f"Conectando ao SMTP: "
            f"{smtp_host}:{smtp_port}"
        )

        with smtplib.SMTP_SSL(
            smtp_host,
            int(smtp_port),
            timeout=30,
        ) as servidor:

            servidor.login(
                smtp_user,
                smtp_password,
            )

            servidor.send_message(
                mensagem
            )

        print(
            f"E-mail enviado com sucesso para "
            f"{destinatario}"
        )

        return True

    except smtplib.SMTPAuthenticationError as erro:

        print(
            "Erro de autenticação SMTP."
        )

        print(
            "Verifique se o usuário é o endereço "
            "Gmail correto e se SMTP_PASSWORD "
            "é uma senha de app válida."
        )

        print(
            f"Código SMTP: {erro.smtp_code}"
        )

        print(
            f"Mensagem: {erro.smtp_error}"
        )

        return False

    except smtplib.SMTPException as erro:

        print(
            f"Erro SMTP: {erro}"
        )

        return False

    except Exception as erro:

        print(
            f"Erro inesperado ao enviar e-mail: "
            f"{erro}"
        )

        return False