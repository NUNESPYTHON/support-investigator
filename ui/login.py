
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
        "Entre na sua conta para continuar."
    )

    email = st.text_input(
        "E-mail",
        placeholder="Digite seu e-mail",
    )

    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Digite sua senha",
    )

    entrar = st.button(
        "Entrar",
        use_container_width=True,
    )

    criar = st.button(
        "Criar conta",
        use_container_width=True,
    )

    recuperar = st.button(
        "Esqueci minha senha",
        use_container_width=True,
    )

    return (
        email,
        senha,
        entrar,
        criar,
        recuperar,
    )
