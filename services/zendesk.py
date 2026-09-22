"""
==========================================================
Support Investigator

Arquivo:
zendesk.py

Responsabilidade:
Centralizar a comunicação com a API da Zendesk.

Autenticação:
- OAuth 2.0 / Bearer Token em produção
- API Token como fallback temporário para desenvolvimento local

Autor:
Elias Nunes
==========================================================
"""

import requests

from config.settings import (
    EMAIL,
    API_TOKEN,
)

from services.auth import (
    obter_contexto,
    obter_headers,
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

REQUEST_TIMEOUT = 30


# ==========================================================
# REQUISIÇÃO À API
# ==========================================================

def fazer_request(
    url: str,
    params: dict | None = None,
):
    """
    Executa uma requisição GET autenticada na API da Zendesk.

    Prioridade de autenticação:

    1. OAuth 2.0 / Bearer Token
    2. API Token legado para desenvolvimento local

    Args:
        url (str):
            URL completa do endpoint da Zendesk.

        params (dict | None):
            Parâmetros opcionais da requisição.

    Returns:
        requests.Response | None:
            Resposta da API ou None em caso de erro.
    """

    try:

        contexto = obter_contexto()

        auth_type = contexto.get(
            "auth_type"
        )

        # ==================================================
        # OAUTH
        # ==================================================

        if auth_type == "oauth":

            headers = obter_headers()

            response = requests.get(
                url,
                headers=headers,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

        # ==================================================
        # LEGADO - API TOKEN
        # ==================================================

        elif auth_type == "legacy":

            if not EMAIL or not API_TOKEN:

                raise RuntimeError(
                    "Credenciais legadas da Zendesk "
                    "não estão configuradas."
                )

            response = requests.get(
                url,
                auth=(
                    f"{EMAIL}/token",
                    API_TOKEN,
                ),
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

        # ==================================================
        # TIPO DESCONHECIDO
        # ==================================================

        else:

            raise RuntimeError(
                "Tipo de autenticação Zendesk "
                "não reconhecido."
            )

        # ==================================================
        # SUCESSO
        # ==================================================

        if 200 <= response.status_code < 300:

            return response

        # ==================================================
        # ERRO HTTP
        # ==================================================

        print()
        print(
            "=================================================="
        )
        print(
            "ERRO HTTP ZENDESK"
        )
        print(
            "=================================================="
        )

        print(
            "Status:",
            response.status_code,
        )

        print(
            "URL:",
            url,
        )

        print(
            "Auth type:",
            auth_type,
        )

        if params:
            print(
                "Params:",
                params,
            )

        print(
            "Response:",
            response.text,
        )

        print(
            "=================================================="
        )
        print()

        return None

    # ======================================================
    # TIMEOUT
    # ======================================================

    except requests.exceptions.Timeout:

        print(
            "Timeout ao consultar a API da Zendesk."
        )

        return None

    # ======================================================
    # CONEXÃO
    # ======================================================

    except requests.exceptions.ConnectionError as erro:

        print(
            "Erro de conexão com a API da Zendesk:",
            erro,
        )

        return None

    # ======================================================
    # AUTENTICAÇÃO / CONFIGURAÇÃO
    # ======================================================

    except RuntimeError as erro:

        print(
            "Erro de autenticação/configuração:",
            erro,
        )

        return None

    # ======================================================
    # ERRO HTTP / REQUEST
    # ======================================================

    except requests.exceptions.RequestException as erro:

        print(
            "Erro na requisição à API da Zendesk:",
            erro,
        )

        return None

    # ======================================================
    # ERRO INESPERADO
    # ======================================================

    except Exception as erro:

        print(
            "Erro inesperado ao consultar a Zendesk:",
            type(erro).__name__,
            erro,
        )

        return None