"""
==========================================================
Zendesk Investigator

Arquivo:
zendesk.py

Responsabilidade:
Centralizar a comunicação com a API da Zendesk.

Autor:
Elias Nunes
==========================================================
"""

import requests

from config.settings import (
    SUBDOMAIN,
    EMAIL,
    API_TOKEN,
)


def fazer_request(url, params=None):
    """
    Executa uma requisição GET autenticada na API da Zendesk.

    Args:
        url (str): URL do endpoint.
        params (dict, optional): Parâmetros da requisição.

    Returns:
        requests.Response | None:
            Resposta da API ou None em caso de erro.
    """

    try:
        response = requests.get(
            url,
            auth=(f"{EMAIL}/token", API_TOKEN),
            params=params,
            timeout=10,
        )

        if response.status_code == 200:
            return response

        print("Erro HTTP:", response.status_code)
        return None

    except requests.exceptions.Timeout:
        print("Timeout na requisição.")
        return None

    except requests.exceptions.ConnectionError:
        print("Erro de conexão.")
        return None