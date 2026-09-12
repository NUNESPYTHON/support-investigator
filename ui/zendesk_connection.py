"""
==========================================================
Support Investigator

Arquivo:
zendesk_connection.py

Responsabilidade:
Exibir a interface de conexão OAuth com o Zendesk.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render():
    """
    Renderiza a interface de conexão OAuth.
    """

    st.markdown(
        "### Conexão com o Zendesk"
    )

    st.caption(
        "Conecte o Support Investigator ao seu ambiente Zendesk."
    )

    subdomain = st.text_input(
        "Subdomínio do Zendesk",
        key="oauth_subdomain",
        placeholder="empresa",
        help=(
            "Informe somente o subdomínio. "
            "Exemplo: empresa.zendesk.com → empresa"
        ),
    )

    client_kind_label = st.radio(
        "Tipo de cliente OAuth",
        [
            "Público",
            "Confidencial",
        ],
        horizontal=True,
        key="oauth_client_kind_label",
    )

    client_id = st.text_input(
        "Client ID",
        key="oauth_client_id",
        placeholder="Identificador do cliente OAuth",
    )

    client_secret = None

    if client_kind_label == "Confidencial":

        client_secret = st.text_input(
            "Client Secret",
            key="oauth_client_secret",
            type="password",
            placeholder="Secret do cliente OAuth",
        )

    conectar = st.button(
        "Conectar ao Zendesk",
        use_container_width=True,
        key="btn_conectar_zendesk",
    )

    client_kind = (
        "public"
        if client_kind_label == "Público"
        else "confidential"
    )

    return {
        "subdomain": subdomain,
        "client_kind": client_kind,
        "client_id": client_id,
        "client_secret": client_secret,
        "conectar": conectar,
    }