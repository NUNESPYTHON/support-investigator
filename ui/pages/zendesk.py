"""
==========================================================
Support Investigator V2

Arquivo:
zendesk.py

Responsabilidade:
Renderizar a página de conexão com o Zendesk.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.zendesk_connection import (
    render as render_zendesk_connection,
)

from services.oauth import (
    gerar_url_autorizacao,
    salvar_contexto_oauth,
    normalizar_subdomain,
)

from services.zendesk_connection import (
    remover_conexao,
)


def render():
    """
    Renderiza a página Zendesk.
    """

    st.markdown(
        "## Zendesk"
    )

    st.caption(
        "Conecte o Support Investigator "
        "ao seu ambiente Zendesk."
    )

    # ======================================================
    # CONEXÃO EXISTENTE
    # ======================================================

    if st.session_state.get(
        "zendesk_connected"
    ):

        connected_subdomain = (
            st.session_state.get(
                "oauth_ctx_subdomain"
            )
        )

        st.success(
            "Conectado ao Zendesk: "
            f"{connected_subdomain}.zendesk.com"
        )

        if st.button(
            "Desconectar",
            key="btn_desconectar_zendesk",
            use_container_width=True,
        ):

            try:

                remover_conexao()

            except Exception as erro:

                st.error(
                    "Não foi possível remover "
                    f"a conexão: {erro}"
                )

                return

            for chave in [
                "zendesk_connected",
                "zendesk_access_token",
                "zendesk_refresh_token",
                "zendesk_token_data",
                "oauth_state",
                "oauth_code_verifier",
                "oauth_ctx_subdomain",
                "oauth_ctx_client_kind",
                "oauth_ctx_client_id",
                "oauth_ctx_client_secret",
            ]:

                st.session_state.pop(
                    chave,
                    None,
                )

            st.session_state[
                "zendesk_connection_loaded"
            ] = True

            st.success(
                "Conexão removida."
            )

            st.rerun()

        st.divider()

    # ======================================================
    # FORMULÁRIO
    # ======================================================

    oauth_form = render_zendesk_connection()

    if not oauth_form.get(
        "conectar"
    ):

        return

    # ======================================================
    # VALIDAÇÃO
    # ======================================================

    subdomain = (
        oauth_form.get(
            "subdomain",
            "",
        )
        .strip()
    )

    client_kind = oauth_form.get(
        "client_kind"
    )

    client_id = (
        oauth_form.get(
            "client_id",
            "",
        )
        .strip()
    )

    client_secret = oauth_form.get(
        "client_secret"
    )

    if not subdomain:

        st.warning(
            "Informe o subdomínio do Zendesk."
        )

        return

    if not client_id:

        st.warning(
            "Informe o Client ID."
        )

        return

    if (
        client_kind == "confidential"
        and not client_secret
    ):

        st.warning(
            "Informe o Client Secret."
        )

        return

    # ======================================================
    # INICIAR OAUTH
    # ======================================================

    try:

        oauth_data = gerar_url_autorizacao(
            subdomain=subdomain,
            state=None,
            client_kind=client_kind,
            client_id=client_id,
        )

        salvar_contexto_oauth(
            oauth_data["state"],
            {
                "state": oauth_data["state"],
                "subdomain": normalizar_subdomain(
                    subdomain
                ),
                "client_kind": client_kind,
                "client_id": client_id,
                "client_secret": client_secret,
                "code_verifier": oauth_data[
                    "code_verifier"
                ],
            },
        )

        st.info(
            "A configuração foi preparada. "
            "Clique abaixo para entrar no Zendesk "
            "e autorizar o Support Investigator."
        )

        st.link_button(
            "Autorizar no Zendesk",
            oauth_data["url"],
            use_container_width=True,
        )

    except Exception as erro:

        st.error(
            "Não foi possível iniciar o OAuth: "
            f"{erro}"
        )