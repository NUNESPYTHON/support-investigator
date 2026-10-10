
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
    Renderiza a tela de login do Support Investigator.
    """

    # ======================================================
    # IDENTIDADE VISUAL ORBITCODE
    # ======================================================

    st.markdown(
        """
        <div style="
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 22px;
        ">
            <div style="
                width: 38px;
                height: 38px;
                border: 2px solid #66E0CA;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                color: #66E0CA;
                font-size: 16px;
                font-weight: 800;
            ">
                &lt;/&gt;
            </div>

            <div style="
                color: #66E0CA;
                font-size: 20px;
                font-weight: 800;
                letter-spacing: 1px;
            ">
                ORBITCODE
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # TÍTULO
    # ======================================================

    st.title("Support Investigator")

    st.caption(
        "Entre na sua conta para continuar."
    )

    # ======================================================
    # CREDENCIAIS
    # ======================================================

    email = st.text_input(
        "E-mail",
        placeholder="Digite seu e-mail",
    )

    senha = st.text_input(
        "Senha",
        type="password",
        placeholder="Digite sua senha",
    )

    # ======================================================
    # AÇÕES
    # ======================================================

    entrar = st.button(
        "Entrar",
        type="primary",
        use_container_width=True,
    )

    criar = st.button(
        "Criar conta",
        type="secondary",
        use_container_width=True,
    )

    recuperar = st.button(
        "Esqueci minha senha",
        type="secondary",
        use_container_width=True,
    )

    # ======================================================
    # RETORNO
    # ======================================================

    return (
        email,
        senha,
        entrar,
        criar,
        recuperar,
    )
