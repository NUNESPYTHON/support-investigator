"""
==========================================================
Support Investigator

Arquivo:
customer_history.py

Responsabilidade:
Renderizar o histórico de interações do cliente.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


def render_resumo(diagnostico_cliente):
    """
    Exibe o resumo geral do cliente.
    """

    resultado_col1, resultado_col2 = st.columns(2)

    with resultado_col1:

        st.caption("E-mail")

        st.write(
            f"**{diagnostico_cliente['email']}**"
        )

        st.caption("Total de tickets")

        st.write(
            f"**{diagnostico_cliente['total_tickets']}**"
        )

        st.caption("Abertos")

        st.write(
            f"**{diagnostico_cliente['abertos']}**"
        )

    with resultado_col2:

        st.caption("Pendentes")

        st.write(
            f"**{diagnostico_cliente['pendentes']}**"
        )

        st.caption("Resolvidos")

        st.write(
            f"**{diagnostico_cliente['resolvidos']}**"
        )

        st.caption("Fechados")

        st.write(
            f"**{diagnostico_cliente['fechados']}**"
        )


def render_ticket_card(ticket):
    """
    Renderiza um ticket do histórico.
    """

    ticket_id = ticket.get("id")

    status = (
        ticket.get("status") or ""
    ).lower()

    assunto = (
        ticket.get("subject")
        or "Sem assunto"
    )

    if status == "new":

        st.warning(
            f"🟠 #{ticket_id} • Novo"
        )

    elif status == "open":

        st.error(
            f"🔴 #{ticket_id} • Aberto"
        )

    elif status == "pending":

        st.info(
            f"🔵 #{ticket_id} • Pendente"
        )

    elif status == "hold":

        st.warning(
            f"🟣 #{ticket_id} • Em espera"
        )

    elif status == "solved":

        st.success(
            f"🟢 #{ticket_id} • Resolvido"
        )

    elif status == "closed":

        st.caption(
            f"⚫ #{ticket_id} • Fechado"
        )

    else:

        st.write(
            f"#{ticket_id} • {status}"
        )

    st.write(
        f"**Assunto:** {assunto}"
    )

    if st.button(
        "Ver detalhes",
        key=f"abrir_ticket_{ticket_id}",
        use_container_width=True,
    ):

        st.session_state[
            "ticket_selecionado"
        ] = str(ticket_id)

        st.rerun()