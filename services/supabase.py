"""
==========================================================
Support Investigator

Arquivo:
supabase.py

Responsabilidade:
Centralizar as conexões com o Supabase.

Autor:
Elias Nunes
==========================================================
"""

import os

import streamlit as st

from dotenv import load_dotenv
from supabase import Client, create_client


load_dotenv()


SUPABASE_URL = os.getenv(
    "SUPABASE_URL"
)

SUPABASE_PUBLISHABLE_KEY = os.getenv(
    "SUPABASE_PUBLISHABLE_KEY"
)

SUPABASE_SECRET_KEY = os.getenv(
    "SUPABASE_SECRET_KEY"
)


def get_supabase() -> Client:
    """
    Cria um cliente Supabase para operações
    autenticadas pelo usuário.

    Quando existe uma sessão do Supabase Auth
    na sessão do Streamlit, ela é aplicada ao cliente.
    """

    if not SUPABASE_URL:

        raise RuntimeError(
            "SUPABASE_URL não configurada."
        )

    if not SUPABASE_PUBLISHABLE_KEY:

        raise RuntimeError(
            "SUPABASE_PUBLISHABLE_KEY não configurada."
        )

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )

    access_token = (
        st.session_state.get(
            "supabase_access_token"
        )
    )

    refresh_token = (
        st.session_state.get(
            "supabase_refresh_token"
        )
    )

    if access_token and refresh_token:

        try:

            supabase.auth.set_session(
                access_token,
                refresh_token,
            )

        except Exception:
            pass

    return supabase


def get_supabase_admin() -> Client:
    """
    Cria um cliente administrativo para operações
    exclusivamente de backend.

    A secret key não deve ser exposta ao navegador,
    ao cliente ou ao código-fonte público.
    """

    if not SUPABASE_URL:

        raise RuntimeError(
            "SUPABASE_URL não configurada."
        )

    if not SUPABASE_SECRET_KEY:

        raise RuntimeError(
            "SUPABASE_SECRET_KEY não configurada."
        )

    return create_client(
        SUPABASE_URL,
        SUPABASE_SECRET_KEY,
    )