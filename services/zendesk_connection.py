"""
==========================================================
Support Investigator V2

Arquivo:
zendesk_connection.py

Responsabilidade:
Persistir e recuperar a conexão Zendesk do usuário autenticado.

Autor:
Elias Nunes
==========================================================
"""

from typing import Any

import streamlit as st

from services.supabase import get_supabase


TABLE_NAME = "zendesk_connections"


def _get_user_id() -> str | None:
    """
    Retorna o ID do usuário autenticado.
    """

    usuario = st.session_state.get("user")

    if usuario is None:
        return None

    user_id = getattr(
        usuario,
        "id",
        None,
    )

    if not user_id:
        return None

    return str(user_id)


def salvar_conexao(
    subdomain: str,
    client_kind: str,
    client_id: str,
    client_secret: str | None,
    access_token: str | None,
    refresh_token: str | None,
    token_data: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """
    Salva ou atualiza a conexão Zendesk do usuário autenticado.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    supabase = get_supabase()

    payload = {
        "user_id": user_id,
        "subdomain": subdomain,
        "client_kind": client_kind,
        "client_id": client_id,
        "client_secret": client_secret,
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_data": token_data,
    }

    response = (
        supabase
        .table(TABLE_NAME)
        .upsert(
            payload,
            on_conflict="user_id",
        )
        .execute()
    )

    if response is None:
        raise RuntimeError(
            "Não foi possível salvar a conexão Zendesk."
        )

    if not response.data:
        raise RuntimeError(
            "A conexão Zendesk não foi salva."
        )

    return response.data[0]


def buscar_conexao() -> dict[str, Any] | None:
    """
    Busca a conexão Zendesk do usuário autenticado.
    """

    user_id = _get_user_id()

    if not user_id:
        return None

    supabase = get_supabase()

    response = (
        supabase
        .table(TABLE_NAME)
        .select(
            """
            id,
            user_id,
            subdomain,
            client_kind,
            client_id,
            client_secret,
            access_token,
            refresh_token,
            token_data,
            created_at,
            updated_at
            """
        )
        .eq(
            "user_id",
            user_id,
        )
        .limit(1)
        .execute()
    )

    if response is None:
        return None

    if not response.data:
        return None

    return response.data[0]


def atualizar_tokens(
    access_token: str | None,
    refresh_token: str | None = None,
    token_data: dict[str, Any] | None = None,
) -> dict[str, Any] | None:
    """
    Atualiza os tokens da conexão existente.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    supabase = get_supabase()

    payload = {
        "access_token": access_token,
        "token_data": token_data,
    }

    if refresh_token is not None:
        payload["refresh_token"] = refresh_token

    response = (
        supabase
        .table(TABLE_NAME)
        .update(payload)
        .eq(
            "user_id",
            user_id,
        )
        .execute()
    )

    if response is None:
        return None

    if not response.data:
        return None

    return response.data[0]


def remover_conexao() -> bool:
    """
    Remove a conexão Zendesk do usuário autenticado.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    supabase = get_supabase()

    response = (
        supabase
        .table(TABLE_NAME)
        .delete()
        .eq(
            "user_id",
            user_id,
        )
        .execute()
    )

    if response is None:
        return False

    return True


def restaurar_conexao_na_sessao() -> bool:
    """
    Carrega a conexão persistida no banco para a sessão atual.
    """

    conexao = buscar_conexao()

    if not conexao:
        return False

    st.session_state[
        "zendesk_connected"
    ] = bool(
        conexao.get(
            "access_token"
        )
    )

    st.session_state[
        "zendesk_access_token"
    ] = conexao.get(
        "access_token"
    )

    st.session_state[
        "zendesk_refresh_token"
    ] = conexao.get(
        "refresh_token"
    )

    st.session_state[
        "zendesk_token_data"
    ] = conexao.get(
        "token_data"
    )

    st.session_state[
        "oauth_ctx_subdomain"
    ] = conexao.get(
        "subdomain"
    )

    st.session_state[
        "oauth_ctx_client_kind"
    ] = conexao.get(
        "client_kind"
    )

    st.session_state[
        "oauth_ctx_client_id"
    ] = conexao.get(
        "client_id"
    )

    st.session_state[
        "oauth_ctx_client_secret"
    ] = conexao.get(
        "client_secret"
    )

    return True