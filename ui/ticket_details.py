"""
==========================================================
Support Investigator

Arquivo:
ticket_details.py

Responsabilidade:
Consultar e exibir os detalhes de um ticket.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from services.diagnostics import diagnosticar_ticket


def render(ticket_id):

    diagnostico = diagnosticar_ticket(
        int(ticket_id)
    )

    if diagnostico is None:

        st.error(
            "Ticket não encontrado."
        )

        return

    st.markdown(
        f"## Detalhes do Ticket #{ticket_id}"
    )

    with st.container(border=True):

        detalhe_col1, detalhe_col2 = (
            st.columns(2)
        )

        with detalhe_col1:

            st.caption("Status")

            st.write(
                f"**{diagnostico['status']}**"
            )

            st.caption("Solicitante")

            st.write(
                f"**{diagnostico['solicitante']}**"
            )

            st.caption("Responsável")

            st.write(
                f"**{diagnostico['responsavel']}**"
            )

        with detalhe_col2:

            st.caption("Assunto")

            st.write(
                f"**{diagnostico['assunto']}**"
            )

            st.caption("Primeira resposta")

            st.write(
                f"**{diagnostico['primeira_resposta']}**"
            )

        st.divider()

        st.markdown(
            "### Resumo"
        )

        st.info(
            diagnostico["resumo"]
        )

        st.markdown(
            "### Última interação"
        )

        ultima = diagnostico.get(
            "ultima_interacao"
        )

        if ultima:

            st.write(
                f"**Autor:** {ultima['autor']}"
            )

            st.write(
                f"**Data:** {ultima['data']}"
            )

            st.write(
                ultima["texto"]
            )

        else:

            st.info(
                "Nenhuma interação encontrada."
            )