"""
==========================================================
Support Investigator

Arquivo:
auth.py

Responsabilidade:
Centralizar o contexto de autenticação e conexão
com o Zendesk.

Suporta:
- OAuth 2.0
- Access Token
- Subdomínio por sessão
- Fallback para ambiente local legado

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from config.settings import (
    SUBDOMAIN,
    API_TOKEN,
    EMAIL,
)


# ==========================================================
# CONTEXTO DA CONEXÃO
# ==========================================================

def obter_subdomain() -> str | None:
    """
    Retorna o subdomínio atualmente conectado.

    Em produção:
    - usa o valor salvo pelo fluxo OAuth.

    Em desenvolvimento/local:
    - faz fallback para SUBDOMAIN do .env.
    """

    subdomain = st.session_state.get(
        "oauth_ctx_subdomain"
    )

    if subdomain:
        return subdomain

    return SUBDOMAIN


def obter_access_token() -> str | None:
    """
    Retorna o access token OAuth armazenado
    na sessão atual.
    """

    return st.session_state.get(
        "zendesk_access_token"
    )


# ==========================================================
# HEADERS
# ==========================================================

def obter_headers() -> dict:
    """
    Retorna os headers de autenticação
    da conexão atual.

    Prioridade:
    1. OAuth Bearer Token
    2. Erro explícito caso não exista OAuth
    """

    access_token = obter_access_token()

    if access_token:
        return {
            "Authorization": (
                f"Bearer {access_token}"
            )
        }

    # Fallback temporário apenas para
    # manter o ambiente local legado funcionando.
    if EMAIL and API_TOKEN:
        return {}

    raise RuntimeError(
        "Nenhuma autenticação Zendesk disponível."
    )


# ==========================================================
# AUTENTICAÇÃO COMPLETA
# ==========================================================

def obter_contexto() -> dict:
    """
    Retorna o contexto atual da conexão Zendesk.
    """

    subdomain = obter_subdomain()

    if not subdomain:
        raise RuntimeError(
            "Nenhum subdomínio Zendesk disponível."
        )

    access_token = obter_access_token()

    if access_token:
        return {
            "subdomain": subdomain,
            "access_token": access_token,
            "auth_type": "oauth",
        }

    if EMAIL and API_TOKEN:
        return {
            "subdomain": subdomain,
            "access_token": None,
            "auth_type": "legacy",
        }

    raise RuntimeError(
        "Nenhuma conexão Zendesk disponível."
    )

# ==========================================================
# URLS
# ==========================================================

def montar_url(endpoint: str) -> str:
    """
    Monta a URL completa da API Zendesk usando
    o subdomínio da conexão atual.
    """

    contexto = obter_contexto()

    return (
        f"https://{contexto['subdomain']}.zendesk.com"
        f"{endpoint}"
    )