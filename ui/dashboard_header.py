"""
==========================================================
Support Investigator V2

Arquivo:
dashboard_header.py

Responsabilidade:
Cabeçalho principal do Dashboard.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render():
    """
    Renderiza o cabeçalho principal do Dashboard.
    """

    profile = st.session_state.get("profile")

    usuario = st.session_state.get("user")

    nome = "User"
    empresa = "-"
    status = "Active"

    if profile:

        nome = profile.get(
            "name",
            nome,
        )

        empresa = profile.get(
            "company",
            empresa,
        )

        status = profile.get(
            "status",
            status,
        )

    elif usuario:

        metadata = getattr(
            usuario,
            "user_metadata",
            {},
        )

        nome = metadata.get(
            "name",
            getattr(
                usuario,
                "email",
                nome,
            ),
        )

    # ======================================================
    # WELCOME
    # ======================================================

    st.markdown(
        f"""
        <div style="
            margin-top: 0.3rem;
            margin-bottom: 1.4rem;
        ">
            <div style="
                font-size: 1.9rem;
                font-weight: 700;
                color: #172554;
                letter-spacing: -0.02em;
            ">
                Welcome, {nome}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # ======================================================
    # INFORMAÇÕES DO USUÁRIO
    # ======================================================

    col1, col2, col3 = st.columns(3)

    with col1:

        st.caption(
            "Company"
        )

        st.write(
            empresa
        )

    with col2:

        st.caption(
            "Status"
        )

        st.write(
            status
        )

    with col3:

        st.caption(
            "Subscription"
        )

        st.write(
            "Professional"
        )

    st.divider()