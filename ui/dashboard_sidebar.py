"""
==========================================================
Support Investigator V2

Arquivo:
dashboard_sidebar.py

Responsabilidade:
Barra lateral principal da aplicação.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from services.i18n import (
    IDIOMAS,
    definir_idioma,
    inicializar_idioma,
    obter_idioma,
    t,
)

from services.session import limpar_sessao


def render():
    """
    Renderiza a Sidebar.
    """

    # ======================================================
    # INICIALIZAR IDIOMA
    # ======================================================

    inicializar_idioma()

    # ======================================================
    # USUÁRIO
    # ======================================================

    profile = st.session_state.get("profile")
    usuario = st.session_state.get("user")

    nome = "User"
    empresa = "-"

    if profile:

        nome = profile.get(
            "name",
            nome,
        )

        empresa = profile.get(
            "company",
            empresa,
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
    # PRODUTO
    # ======================================================

    st.sidebar.markdown(
        "### Technical Support Intelligence"
    )

    st.sidebar.caption(
        "Investigate faster. Understand more. Resolve with confidence."
    )

    st.sidebar.divider()

    # ======================================================
    # CONTA
    # ======================================================

    st.sidebar.markdown(
        f"#### {t('account')}"
    )

    st.sidebar.write(
        f"**{nome}**"
    )

    st.sidebar.caption(
        empresa
    )

    st.sidebar.divider()

    # ======================================================
    # NAVEGAÇÃO
    # ======================================================

    secoes = {
        "Dashboard": t("dashboard"),
        "Zendesk": t("zendesk"),
        "Investigator": t("investigator"),
        "Export": t("export"),
        "Billing": t("billing"),
        "Settings": t("settings"),
    }

    opcoes_internas = list(
        secoes.keys()
    )

    opcoes_exibicao = list(
        secoes.values()
    )

    secao_atual = st.session_state.get(
        "dashboard_navigation",
        "Dashboard",
    )

    indice_secao = opcoes_internas.index(
        secao_atual
    )

    secao_exibicao = st.sidebar.radio(
        t("navigation"),
        options=opcoes_exibicao,
        index=indice_secao,
        label_visibility="collapsed",
    )

    secao = opcoes_internas[
        opcoes_exibicao.index(
            secao_exibicao
        )
    ]

    st.session_state[
        "dashboard_navigation"
    ] = secao

    st.sidebar.divider()

    # ======================================================
    # IDIOMA
    # ======================================================

    idioma_atual = obter_idioma()

    opcoes_idioma = list(
        IDIOMAS.keys()
    )

    if idioma_atual not in opcoes_idioma:

        idioma_atual = opcoes_idioma[0]

    indice_idioma = opcoes_idioma.index(
        idioma_atual
    )

    idioma = st.sidebar.selectbox(
        t("language"),
        opcoes_idioma,
        index=indice_idioma,
        format_func=lambda codigo: IDIOMAS[codigo],
        key="dashboard_language",
    )

    # ======================================================
    # ALTERAÇÃO DE IDIOMA
    # ======================================================

    if idioma != idioma_atual:

        definir_idioma(
            idioma
        )

        st.session_state.language_code = idioma

        st.rerun()

    # ======================================================
    # LOGOUT
    # ======================================================

    st.sidebar.divider()

    if st.sidebar.button(
        t("logout"),
        use_container_width=True,
        key="sidebar_logout",
    ):

        limpar_sessao()

        st.session_state.clear()

        st.rerun()

    return secao