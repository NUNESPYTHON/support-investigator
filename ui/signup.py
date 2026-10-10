
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

    st.title("Crie sua conta")

    st.caption(
        "Comece a usar o Support Investigator."
    )

    nome = st.text_input(
        "Nome",
        placeholder="Digite seu nome",
    )

    empresa = st.text_input(
        "Empresa",
        placeholder="Sua empresa (opcional)",
    )

    email = st.text_input(
        "E-mail",
        placeholder="Digite seu e-mail",
    )

    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Crie uma senha",
    )

    confirmar_senha = st.text_input(
        "Confirmar senha",
        type="password",
        placeholder="Digite sua senha novamente",
    )

    criar_conta = st.button(
        "Criar conta",
        use_container_width=True,
    )

    voltar_login = st.button(
        "Voltar para o login",
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
