
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
    # ESTILO VISUAL ORBITCODE
    # ======================================================

    st.markdown(
        """
<style>
/* Fundo com iluminação verde-azulada */
[data-testid="stAppViewContainer"] {
    background:
        radial-gradient(
            ellipse at 82% 12%,
            rgba(44, 126, 124, 0.35) 0%,
            rgba(24, 76, 84, 0.22) 35%,
            transparent 72%
        ),
        linear-gradient(
            145deg,
            #173d43 0%,
            #142f3c 38%,
            #101c29 85%
        );
    background-attachment: fixed;
}

/* Fundo transparente para o conteudo */
[data-testid="stMain"] {
    background: transparent;
}

/* Botões secundarios com verde-petroleo */
.stButton button[kind="secondary"] {
    background-color: #1d4550;
    color: #e7faf6;
    border: 1px solid #3b6870;
    border-radius: 10px;
}

/* Efeito ao passar o mouse */
.stButton button[kind="secondary"]:hover {
    background-color: #275864;
    color: #ffffff;
    border-color: #66e0ca;
}

/* Botão principal */
.stButton button[kind="primary"] {
    background-color: #66e0ca;
    color: #071420;
    border: 1px solid #66e0ca;
    border-radius: 10px;
    font-weight: 700;
}

.stButton button[kind="primary"]:hover {
    background-color: #82ead7;
    color: #071420;
    border-color: #82ead7;
}
</style>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # MARCA ORBITCODE
    # ======================================================

    st.markdown(
        """
<div style="display:flex;align-items:center;gap:12px;
            margin-bottom:18px;">
    <span style="display:inline-flex;align-items:center;
                 justify-content:center;width:38px;height:38px;
                 border:2px solid #66e0ca;border-radius:50%;
                 color:#66e0ca;font-weight:800;font-size:14px;">
        &lt;/&gt;
    </span>
    <span style="color:#66e0ca;font-size:21px;
                 font-weight:800;letter-spacing:1px;">
        ORBITCODE
    </span>
</div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # TITULO
    # ======================================================

    st.title("Support Investigator")

    st.caption(
        "Entre na sua conta para continuar."
    )

    # ======================================================
    # CAMPOS DE LOGIN
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
    # BOTOES
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
    # RETORNO PARA AUTENTICACAO
    # ======================================================

    return (
        email,
        senha,
        entrar,
        criar,
        recuperar,
    )
