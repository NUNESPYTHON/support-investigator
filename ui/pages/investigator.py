"""
==========================================================
Support Investigator V2

Arquivo:
investigator.py

Responsabilidade:
Renderizar a página de investigação.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.ticket_details import (
    render as render_ticket_details,
)

from ui.customer_history import (
    render_resumo,
    render_ticket_card,
)

from services.customer_diagnostics import (
    diagnosticar_cliente,
)


def render():
    """
    Renderiza a página Investigator.
    """

    st.markdown(
        "## Investigator"
    )

    st.caption(
        "Investigue tickets e consulte o contexto do cliente."
    )

    col1, col2 = st.columns(2)

    # ======================================================
    # DETALHES DO TICKET
    # ======================================================

    with col1:

        with st.container(border=True):

            st.markdown(
                "### Detalhes do Ticket"
            )

            st.markdown(
                "Consulte rapidamente o status, "
                "responsável, primeira resposta, "
                "última interação e resumo do ticket."
            )

            ticket_id = st.text_input(
                "Número do Ticket",
                key="investigator_ticket_id",
                placeholder="Ex.: 1114",
            )

            diagnosticar = st.button(
                "Consultar",
                use_container_width=True,
                key="investigator_diagnosticar",
            )

    # ======================================================
    # HISTÓRICO DO CLIENTE
    # ======================================================

    with col2:

        with st.container(border=True):

            st.markdown(
                "### Histórico de Interações"
            )

            st.markdown(
                "Consulte os tickets associados "
                "a um cliente."
            )

            email_cliente = st.text_input(
                "E-mail do Cliente",
                key="investigator_email_cliente",
                placeholder="Ex.: cliente@empresa.com",
            )

            consultar = st.button(
                "Consultar",
                use_container_width=True,
                key="investigator_consultar",
            )

    # ======================================================
    # DETALHES DO TICKET
    # ======================================================

    if diagnosticar:

        if not ticket_id:

            st.warning(
                "Informe o número do ticket."
            )

        elif not ticket_id.isdigit():

            st.warning(
                "Informe um número de ticket válido."
            )

        else:

            render_ticket_details(
                ticket_id
            )

    # ======================================================
    # CONSULTAR HISTÓRICO
    # ======================================================

    if consultar:

        if not email_cliente:

            st.warning(
                "Informe o e-mail do cliente."
            )

            st.session_state[
                "investigator_historico_cliente"
            ] = None

            st.session_state[
                "ticket_selecionado"
            ] = None

        else:

            diagnostico_cliente = (
                diagnosticar_cliente(
                    email_cliente.strip()
                )
            )

            if diagnostico_cliente is None:

                st.error(
                    "Nenhum histórico encontrado para este cliente."
                )

                st.session_state[
                    "investigator_historico_cliente"
                ] = None

                st.session_state[
                    "ticket_selecionado"
                ] = None

            else:

                st.session_state[
                    "investigator_historico_cliente"
                ] = diagnostico_cliente

                st.session_state[
                    "ticket_selecionado"
                ] = None

    # ======================================================
    # EXIBIR HISTÓRICO
    # ======================================================

    diagnostico_cliente = st.session_state.get(
        "investigator_historico_cliente"
    )

    if diagnostico_cliente:

        st.divider()

        st.markdown(
            "### Histórico de Interações"
        )

        render_resumo(
            diagnostico_cliente
        )

        st.divider()

        st.markdown(
            "### Últimos tickets"
        )

        for ticket in diagnostico_cliente[
            "ultimos_tickets"
        ]:

            render_ticket_card(
                ticket
            )

        st.divider()

        st.markdown(
            "### Resumo"
        )

        st.info(
            diagnostico_cliente[
                "resumo"
            ]
        )

    # ======================================================
    # TICKET SELECIONADO
    # ======================================================

    ticket_selecionado = st.session_state.get(
        "ticket_selecionado"
    )

    if ticket_selecionado:

        render_ticket_details(
            ticket_selecionado
        )