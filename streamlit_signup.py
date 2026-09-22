"""
==========================================================
Support Investigator V2

Arquivo:
streamlit_signup.py

Responsabilidade:
Laboratório da criação de contas.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.signup import render
from services.authentication import criar_usuario


st.set_page_config(
    page_title="Support Investigator - Create Account",
    layout="centered",
)


(
    nome,
    empresa,
    email,
    senha,
    confirmar_senha,
    criar_conta,
    voltar_login,
) = render()


if criar_conta:

    if not nome.strip():

        st.warning(
            "Please enter your name."
        )

    elif not email.strip():

        st.warning(
            "Please enter your email."
        )

    elif not senha:

        st.warning(
            "Please enter a password."
        )

    elif senha != confirmar_senha:

        st.warning(
            "Passwords do not match."
        )

    elif len(senha) < 8:

        st.warning(
            "Password must contain at least 8 characters."
        )

    else:

        try:

            resposta = criar_usuario(
                email=email,
                senha=senha,
                nome=nome,
                empresa=empresa,
                 )

            if resposta.user:

                st.success(
                    "Account created successfully."
                )

                st.info(
                    "Check your email to confirm your account."
                )

        except Exception as e:

            import traceback
            st.exception(e)
            st.code(
                traceback.format_exc()
            )


if voltar_login:

    st.info(
        "Login screen will be connected in the next step."
    )