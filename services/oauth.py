"""
==========================================================
Support Investigator

Arquivo:
oauth.py

Responsabilidade:
Implementar o fluxo OAuth 2.0 do Zendesk.

Suporta:
- Public + PKCE
- Confidential + client_secret
- Authorization Code
- Refresh Token

Autor:
Elias Nunes
==========================================================
"""

import base64
import hashlib
import secrets
import time
from urllib.parse import urlencode

import requests

from config.settings import (
    ZENDESK_OAUTH_CLIENT_ID,
    ZENDESK_OAUTH_REDIRECT_URI,
)


# ==========================================================
# CONFIGURAÇÕES
# ==========================================================

ZENDESK_AUTH_PATH = (
    "/oauth/authorizations/new"
)

ZENDESK_TOKEN_PATH = (
    "/oauth/tokens"
)

DEFAULT_SCOPE = (
    "read"
)


# ==========================================================
# NORMALIZAÇÃO
# ==========================================================

def normalizar_subdomain(
    subdomain: str,
) -> str:
    """
    Normaliza o subdomínio do Zendesk.
    """

    valor = (
        subdomain
        .strip()
        .lower()
        .replace("https://", "")
        .replace("http://", "")
    )

    valor = valor.split(".")[0]

    return valor


# ==========================================================
# STATE
# ==========================================================

def gerar_state() -> str:
    """
    Gera um state aleatório para proteção contra CSRF.
    """

    return secrets.token_urlsafe(32)


# ==========================================================
# PKCE
# ==========================================================

def gerar_pkce():
    """
    Gera code_verifier e code_challenge
    utilizando SHA-256 / S256.
    """

    code_verifier = (
        base64.urlsafe_b64encode(
            secrets.token_bytes(32)
        )
        .rstrip(b"=")
        .decode("utf-8")
    )

    digest = hashlib.sha256(
        code_verifier.encode("utf-8")
    ).digest()

    code_challenge = (
        base64.urlsafe_b64encode(
            digest
        )
        .rstrip(b"=")
        .decode("utf-8")
    )

    return (
        code_verifier,
        code_challenge,
    )


# ==========================================================
# URL DE AUTORIZAÇÃO
# ==========================================================

def gerar_url_autorizacao(
    subdomain: str,
    state: str | None = None,
    client_kind: str = "confidential",
    client_id: str | None = None,
    redirect_uri: str | None = None,
    scope: str = DEFAULT_SCOPE,
):
    """
    Gera a URL de autorização OAuth do Zendesk.

    Para Public:
    - gera PKCE
    - adiciona code_challenge

    Para Confidential:
    - não exige PKCE
    - usa client_id normalmente
    """

    subdomain = normalizar_subdomain(
        subdomain
    )

    if not subdomain:
        raise ValueError(
            "O subdomínio do Zendesk é obrigatório."
        )

    if not client_id:

        client_id = (
            ZENDESK_OAUTH_CLIENT_ID
        )

    if not state:

        state = gerar_state()

    code_verifier = None

    parametros = {
    "response_type": "code",
    "client_id": client_id,
    "redirect_uri": (
        redirect_uri
        or ZENDESK_OAUTH_REDIRECT_URI
    ),
    "scope": scope,
    "state": state,
}

    if client_kind == "public":

        (
            code_verifier,
            code_challenge,
        ) = gerar_pkce()

        parametros[
            "code_challenge"
        ] = code_challenge

        parametros[
            "code_challenge_method"
        ] = "S256"

    elif client_kind != "confidential":

        raise ValueError(
            "client_kind deve ser "
            "'public' ou 'confidential'."
        )

    url = (
        f"https://{subdomain}.zendesk.com"
        f"{ZENDESK_AUTH_PATH}?"
        f"{urlencode(parametros)}"
    )

    return {
        "url": url,
        "state": state,
        "code_verifier": code_verifier,
    }


# ==========================================================
# TROCA DO AUTHORIZATION CODE
# ==========================================================

def trocar_codigo_por_token(
    subdomain: str,
    code: str,
    client_kind: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    code_verifier: str | None = None,
    redirect_uri: str | None = None,
    scope: str = DEFAULT_SCOPE,
):
    """
    Troca o authorization code por access_token
    e refresh_token.
    """

    subdomain = normalizar_subdomain(
        subdomain
    )

    if not code:
        raise ValueError(
            "Authorization code não informado."
        )

    if not client_id:

        client_id = (
            ZENDESK_OAUTH_CLIENT_ID
        )

    payload = {
    "grant_type": "authorization_code",
    "code": code,
    "client_id": client_id,
    "redirect_uri": (
        redirect_uri
        or ZENDESK_OAUTH_REDIRECT_URI
    ),
    "scope": scope,
}

    if client_kind == "public":

        if not code_verifier:
            raise ValueError(
                "code_verifier é obrigatório "
                "para clientes Public."
            )

        payload[
            "code_verifier"
        ] = code_verifier

    elif client_kind == "confidential":

        if not client_secret:
            raise ValueError(
                "Client Secret é obrigatório "
                "para clientes Confidential."
            )

        payload[
            "client_secret"
        ] = client_secret

    else:

        raise ValueError(
            "client_kind deve ser "
            "'public' ou 'confidential'."
        )

    response = requests.post(
        f"https://{subdomain}.zendesk.com"
        f"{ZENDESK_TOKEN_PATH}",
        data=payload,
        timeout=30,
    )

    if not response.ok:

        try:
            detalhe = response.json()

        except ValueError:

            detalhe = response.text

        raise RuntimeError(
            "Erro ao trocar authorization code "
            f"por token: "
            f"{response.status_code} - "
            f"{detalhe}"
        )

    dados = response.json()

    access_token = dados.get(
        "access_token"
    )

    if not access_token:

        raise RuntimeError(
            "Zendesk não retornou access_token."
        )

    return dados


# ==========================================================
# REFRESH TOKEN
# ==========================================================

def atualizar_access_token(
    subdomain: str,
    refresh_token: str,
    client_kind: str,
    client_id: str | None = None,
    client_secret: str | None = None,
    scope: str = DEFAULT_SCOPE,
):
    """
    Atualiza o access token utilizando o refresh token.
    """

    subdomain = normalizar_subdomain(
        subdomain
    )

    if not refresh_token:

        raise ValueError(
            "Refresh token não informado."
        )

    if not client_id:

        client_id = (
            ZENDESK_OAUTH_CLIENT_ID
        )

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "scope": scope,
    }

    if client_kind == "confidential":

        if not client_secret:

            raise ValueError(
                "Client Secret é obrigatório "
                "para clientes Confidential."
            )

        payload[
            "client_secret"
        ] = client_secret

    elif client_kind != "public":

        raise ValueError(
            "client_kind deve ser "
            "'public' ou 'confidential'."
        )

    response = requests.post(
        f"https://{subdomain}.zendesk.com"
        f"{ZENDESK_TOKEN_PATH}",
        data=payload,
        timeout=30,
    )

    if not response.ok:

        try:
            detalhe = response.json()

        except ValueError:

            detalhe = response.text

        raise RuntimeError(
            "Erro ao atualizar access token: "
            f"{response.status_code} - "
            f"{detalhe}"
        )

    dados = response.json()

    access_token = dados.get(
        "access_token"
    )

    if not access_token:

        raise RuntimeError(
            "Zendesk não retornou novo access_token."
        )

    return dados


# ==========================================================
# EXPIRAÇÃO
# ==========================================================

def calcular_expires_at(
    expires_in: int | None,
) -> float | None:
    """
    Converte expires_in em timestamp absoluto.
    """

    if not expires_in:
        return None

    return (
        time.time()
        + int(expires_in)
    )


def token_expirado(
    expires_at: float | None,
    margem_segundos: int = 60,
) -> bool:
    """
    Verifica se o token expirou ou está próximo de expirar.
    """

    if not expires_at:

        return True

    return (
        time.time()
        >=
        expires_at - margem_segundos
    )

# ==========================================================
# ARMAZENAMENTO TEMPORÁRIO DO FLUXO OAUTH
# ==========================================================

_OAUTH_PENDING = {}


def salvar_contexto_oauth(
    state: str,
    contexto: dict,
) -> None:
    """
    Armazena temporariamente os dados necessários
    para concluir o fluxo OAuth após o callback.
    """

    if not state:
        raise ValueError(
            "State OAuth não informado."
        )

    _OAUTH_PENDING[state] = contexto


def obter_contexto_oauth(
    state: str,
) -> dict | None:
    """
    Recupera o contexto OAuth associado ao state.
    """

    if not state:
        return None

    return _OAUTH_PENDING.get(
        state
    )


def remover_contexto_oauth(
    state: str,
) -> None:
    """
    Remove o contexto OAuth após a conclusão
    ou cancelamento do fluxo.
    """

    if state:
        _OAUTH_PENDING.pop(
            state,
            None,
        )