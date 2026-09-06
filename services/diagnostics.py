"""
==========================================================
Zendesk Investigator

Arquivo:
diagnostics.py

Responsabilidade:
Montar um diagnóstico consolidado de um ticket.

Autor:
Elias Nunes
==========================================================
"""

from services.metrics import buscar_metricas_ticket
from services.tickets import buscar_ticket_por_id
from services.users import buscar_usuario_por_id
from utils.formatters import formatar_tempo


def gerar_resumo(ticket, primeira_resposta):
    """
    Gera um resumo executivo com base nas informações do ticket.

    Args:
        ticket (dict): Dados do ticket.
        primeira_resposta (str): Tempo da primeira resposta.

    Returns:
        str
    """

    status = ticket.get("status")

    if status == "pending":
        return (
            "O suporte respondeu ao cliente. "
            "Neste momento estamos aguardando "
            "um retorno."
        )

    if status == "open":
        return (
            "O ticket está em atendimento."
        )

    if status == "new":
        return (
            "O ticket ainda não recebeu atendimento."
        )

    if status == "closed":
        return (
            "O atendimento foi concluído."
        )

    return "Status não identificado."

def diagnosticar_ticket(ticket_id):
    """
    Busca um ticket e reúne informações importantes
    para o diagnóstico.

    Args:
        ticket_id (int): ID do ticket.

    Returns:
        dict | None
    """

    # ------------------------------------------------------
    # 1. Busca o ticket
    # ------------------------------------------------------

    ticket = buscar_ticket_por_id(ticket_id)

    if ticket is None:
        return None

    # ------------------------------------------------------
    # 2. Busca o solicitante
    # ------------------------------------------------------

    requester = buscar_usuario_por_id(
        ticket.get("requester_id")
    )

    # ------------------------------------------------------
    # 3. Busca o responsável
    # ------------------------------------------------------

    assignee = None

    assignee_id = ticket.get("assignee_id")

    if assignee_id is not None:
        assignee = buscar_usuario_por_id(
            assignee_id
        )

    # ------------------------------------------------------
    # 4. Busca as métricas
    # ------------------------------------------------------

    metricas = buscar_metricas_ticket(ticket_id)

    primeira_resposta = "Ainda não respondido"

    if metricas:

        reply_time = metricas.get(
            "reply_time_in_minutes"
        )

        if reply_time:

            primeira_resposta = formatar_tempo(
                reply_time.get("business")
            )
            resumo = gerar_resumo(
    ticket,
    primeira_resposta
)

    # ------------------------------------------------------
    # 5. Monta o diagnóstico
    # ------------------------------------------------------

    return {
        "ticket_id": ticket.get("id"),

        "status": ticket.get("status"),

        "assunto": (
            ticket.get("subject")
            or "Sem assunto"
        ),

        "solicitante": (
            requester.get("nome")
            if requester
            else "Não identificado"
        ),

        "responsavel": (
            assignee.get("nome")
            if assignee
            else "Não atribuído"
        ),

        "primeira_resposta": primeira_resposta,
        "resumo": resumo,
    }
         