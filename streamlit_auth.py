"""
==========================================================
Support Investigator V2

Arquivo:
streamlit_auth.py

Responsabilidade:
Autenticação do usuário e acesso ao perfil.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.login import render
from services.authentication import (
    fazer_login,
    solicitar_recuperacao_senha,
)
from services.supabase import get_supabase


st.set_page_config(
    page_title="Support Investigator",
    layout="centered",
)


# --------------------------------------------------------
# Inicialização da sessão
# --------------------------------------------------------

if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "user" not in st.session_state:
    st.session_state.user = None

if "profile" not in st.session_state:
    st.session_state.profile = None


# --------------------------------------------------------
# Tela de login
# --------------------------------------------------------

email, senha, entrar, criar, recuperar = render()


# --------------------------------------------------------
# Criar conta
# --------------------------------------------------------

if criar:
    st.info(
        "Account creation is available from the sign-up screen."
    )


# --------------------------------------------------------
# Login
# --------------------------------------------------------

if entrar:

    try:

        resposta = fazer_login(
            email=email,
            senha=senha,
        )

        if not resposta.user:
            st.error(
                "Unable to sign in."
            )

        elif not resposta.session:
            st.error(
                "Login succeeded, but no session was returned."
            )

        else:

            usuario = resposta.user
            sessao = resposta.session

            # Cria o cliente Supabase
            supabase = get_supabase()

            # Registra a sessão nesse cliente
            supabase.auth.set_session(
                sessao.access_token,
                sessao.refresh_token,
            )

            # Busca o perfil do usuário autenticado
            profile_response = (
                supabase
                .table("profiles")
                .select(
                    "id, name, company, status, last_login"
                )
                .eq(
                    "id",
                    usuario.id,
                )
                .maybe_single()
                .execute()
            )

            profile = profile_response.data

            if not profile:

                st.error(
                    "User profile not found."
                )

            else:

                # Guarda os dados na sessão do Streamlit
                st.session_state.authenticated = True
                st.session_state.user = usuario
                st.session_state.profile = profile

                # Mostra o resultado
                st.success(
                    f"Welcome, {profile['name']}"
                )

                if profile.get("company"):
                    st.write(
                        f"Company: {profile['company']}"
                    )

                st.write(
                    f"Status: {profile['status']}"
                )


    except Exception as e:

        st.error(
            f"Login error: {e}"
        )


# --------------------------------------------------------
# Recuperação de senha
# --------------------------------------------------------

if recuperar:

    try:

        if not email.strip():

            st.warning(
                "Please enter your email address."
            )

        else:

            solicitar_recuperacao_senha(
                email=email
            )

            st.success(
                "Password reset email sent."
            )

    except Exception as e:

        st.error(
            f"Password recovery error: {e}"
        )