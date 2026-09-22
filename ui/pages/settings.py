"""
==========================================================
Support Investigator V2

Arquivo:
settings.py

Responsabilidade:
Renderizar a página de configurações.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render():
    """
    Renderiza Settings.
    """

    st.markdown(
        "## Settings"
    )

    st.caption(
        "Configurações da sua conta."
    )

    profile = st.session_state.get(
        "profile"
    )

    usuario = st.session_state.get(
        "user"
    )

    nome = "-"
    empresa = "-"
    email = "-"

    if profile:

        nome = profile.get(
            "name",
            nome,
        )

        empresa = profile.get(
            "company",
            empresa,
        )

    if usuario:

        email = getattr(
            usuario,
            "email",
            email,
        )

    st.markdown(
        "### Account"
    )

    col1, col2 = st.columns(2)

    with col1:

        st.text_input(
            "Name",
            value=nome,
            disabled=True,
        )

        st.text_input(
            "Company",
            value=empresa,
            disabled=True,
        )

    with col2:

        st.text_input(
            "Email",
            value=email,
            disabled=True,
        )