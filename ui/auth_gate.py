"""
==========================================================
Support Investigator V2

Arquivo:
auth_gate.py

Responsabilidade:
Controlar o fluxo de autenticação da aplicação principal.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.login import render as render_login
from ui.signup import render as render_signup

from services.authentication import (
    criar_usuario,
    fazer_login,
    solicitar_recuperacao_senha,
)

from services.session import (
    usuario_autenticado,
    definir_usuario,
)


def _criar_profile_temporario(usuario):
    """
    Cria um profile básico a partir dos dados disponíveis
    no usuário autenticado.

    O profile definitivo do Supabase será carregado depois,
    sem bloquear o processo de login.
    """

    metadata = getattr(
        usuario,
        "user_metadata",
        None,
    ) or {}

    return {
        "id": getattr(
            usuario,
            "id",
            None,
        ),
        "name": metadata.get(
            "name",
            "",
        ),
        "company": metadata.get(
            "company",
            "",
        ),
        "status": "active",
        "last_login": None,
    }


def _render_login() -> bool:
    """
    Renderiza a tela de login.

    Retorna:
        True  -> login realizado
        False -> permanece no authentication gate
    """

    (
        email,
        senha,
        entrar,
        criar,
        recuperar,
    ) = render_login()

    # ======================================================
    # LOGIN
    # ======================================================

    if entrar:

        if not email.strip():

            st.warning(
                "Please enter your email."
            )

            return False

        if not senha:

            st.warning(
                "Please enter your password."
            )

            return False

        try:

            # --------------------------------------------------
            # AUTENTICAR NO SUPABASE
            # --------------------------------------------------

            resposta = fazer_login(
                email=email,
                senha=senha,
            )

            # --------------------------------------------------
            # VALIDAR RESPOSTA
            # --------------------------------------------------

            if not resposta:

                st.error(
                    "Unable to sign in."
                )

                return False

            if not resposta.user:

                st.error(
                    "Unable to sign in."
                )

                return False

            if not resposta.session:

                st.error(
                    "Login succeeded, but no session was returned."
                )

                return False

            usuario = resposta.user
            sessao = resposta.session

            # --------------------------------------------------
            # SALVAR TOKENS
            # --------------------------------------------------

            st.session_state[
                "supabase_access_token"
            ] = sessao.access_token

            st.session_state[
                "supabase_refresh_token"
            ] = sessao.refresh_token

            # --------------------------------------------------
            # CRIAR PROFILE LOCAL
            #
            # IMPORTANTE:
            # Não fazemos consulta ao banco aqui.
            # Isso evita bloquear o login.
            # --------------------------------------------------

            profile = _criar_profile_temporario(
                usuario
            )

            # --------------------------------------------------
            # SALVAR USUÁRIO NA SESSÃO
            # --------------------------------------------------

            definir_usuario(
                usuario,
                profile,
            )

            # --------------------------------------------------
            # MARCAR AUTENTICAÇÃO
            # --------------------------------------------------

            st.session_state[
                "supabase_authenticated"
            ] = True

            # --------------------------------------------------
            # FORÇAR RESTAURAÇÃO DO ZENDESK
            # --------------------------------------------------

            st.session_state[
                "zendesk_connection_loaded"
            ] = False

            # --------------------------------------------------
            # NÃO USAR st.rerun() AQUI
            #
            # O render_auth_gate() retornará True e
            # o streamlit_app.py continuará normalmente.
            # --------------------------------------------------

            return True

        except Exception as erro:

            st.error(
                f"Login error: {erro}"
            )

            return False

    # ======================================================
    # CRIAR CONTA
    # ======================================================

    if criar:

        st.session_state.auth_screen = (
            "signup"
        )

        st.rerun()

    # ======================================================
    # RECUPERAR SENHA
    # ======================================================

    if recuperar:

        if not email.strip():

            st.warning(
                "Please enter your email address."
            )

        else:

            try:

                solicitar_recuperacao_senha(
                    email=email
                )

                st.success(
                    "Password reset email sent."
                )

            except Exception as erro:

                st.error(
                    f"Password recovery error: {erro}"
                )

    return False


def _render_signup() -> bool:
    """
    Renderiza a criação de conta.
    """

    (
        nome,
        empresa,
        email,
        senha,
        confirmar_senha,
        criar_conta,
        voltar_login,
    ) = render_signup()

    # ======================================================
    # CRIAR CONTA
    # ======================================================

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
                "Please enter your password."
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

                else:

                    st.error(
                        "Unable to create account."
                    )

            except Exception as erro:

                st.error(
                    f"Account creation error: {erro}"
                )

    # ======================================================
    # VOLTAR PARA LOGIN
    # ======================================================

    if voltar_login:

        st.session_state.auth_screen = (
            "login"
        )

        st.rerun()

    return False


def render_auth_gate() -> bool:
    """
    Renderiza login/cadastro enquanto o usuário
    não estiver autenticado.

    Retorna:
        True  -> usuário autenticado
        False -> permanece no authentication gate.
    """

    # ------------------------------------------------------
    # USUÁRIO JÁ AUTENTICADO
    # ------------------------------------------------------

    if usuario_autenticado():

        return True

    # ------------------------------------------------------
    # INICIALIZAR TELA
    # ------------------------------------------------------

    if "auth_screen" not in st.session_state:

        st.session_state.auth_screen = (
            "login"
        )

    # ------------------------------------------------------
    # SIGNUP
    # ------------------------------------------------------

    if st.session_state.auth_screen == "signup":

        return _render_signup()

    # ------------------------------------------------------
    # LOGIN
    # ------------------------------------------------------

    return _render_login()