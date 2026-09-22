"""
==========================================================
Support Investigator

Arquivo:
login.py

Responsabilidade:
Tela de autenticação do usuário.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render():
    """
    Renderiza a tela de login.
    """

    st.title("Support Investigator")

    st.caption(
        "Sign in to continue."
    )

    email = st.text_input(
        "Email"
    )

    senha = st.text_input(
        "Password",
        type="password",
    )

    entrar = st.button(
        "Login",
        use_container_width=True,
    )

    criar = st.button(
        "Create account",
        use_container_width=True,
    )

    recuperar = st.button(
        "Forgot password",
        use_container_width=True,
    )

    return (
        email,
        senha,
        entrar,
        criar,
        recuperar,
    )