"""
==========================================================
Support Investigator

Arquivo:
signup.py

Responsabilidade:
Tela de criação de conta do Support Investigator.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render():
    """
    Renderiza a tela de criação de conta.
    """

    st.title("Create your account")

    st.caption(
        "Start your Support Investigator account."
    )

    nome = st.text_input(
        "Name",
        placeholder="Your name",
    )

    empresa = st.text_input(
        "Company",
        placeholder="Your company (optional)",
    )

    email = st.text_input(
        "Email",
        placeholder="you@example.com",
    )

    senha = st.text_input(
        "Password",
        type="password",
    )

    confirmar_senha = st.text_input(
        "Confirm password",
        type="password",
    )

    criar_conta = st.button(
        "Create account",
        use_container_width=True,
    )

    voltar_login = st.button(
        "Back to login",
        use_container_width=True,
    )

    return (
        nome,
        empresa,
        email,
        senha,
        confirmar_senha,
        criar_conta,
        voltar_login,
    )