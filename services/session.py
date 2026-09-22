"""
==========================================================
Support Investigator V2

Arquivo:
session.py

Responsabilidade:
Gerenciar a sessão autenticada do usuário.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def inicializar_sessao():
    """
    Inicializa as variáveis de sessão do aplicativo.
    """

    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False

    if "user" not in st.session_state:
        st.session_state.user = None

    if "profile" not in st.session_state:
        st.session_state.profile = None


def usuario_autenticado() -> bool:
    """
    Retorna True quando existe um usuário autenticado.
    """

    return bool(
        st.session_state.get("authenticated", False)
    )


def definir_usuario(usuario, profile):
    """
    Salva o usuário autenticado e seu perfil
    na sessão do Streamlit.
    """

    st.session_state.authenticated = True
    st.session_state.user = usuario
    st.session_state.profile = profile


def limpar_sessao():
    """
    Remove os dados de autenticação da sessão.
    """

    st.session_state.authenticated = False
    st.session_state.user = None
    st.session_state.profile = None