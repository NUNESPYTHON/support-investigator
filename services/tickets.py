"""
==========================================================
Support Investigator

Arquivo:
tickets.py

Responsabilidade:
Funções relacionadas à busca de tickets.

Autor:
Elias Nunes
==========================================================
"""

from config.settings import SUBDOMAIN
from services.search import (
    buscar_todos_resultados,
    montar_query_tickets,
)
from services.users import buscar_usuario_por_email
from services.zendesk import fazer_request


def buscar_tickets_por_email(email):
    """
    Busca todos os tickets de um usuário.

    Args:
        email (str): E-mail do solicitante.

    Returns:
        list: Lista de tickets encontrados.
    """

    usuario = buscar_usuario_por_email(email)

    if usuario is None:
        return []

    query = montar_query_tickets(
        user_id=usuario["id"]
    )

    tickets = buscar_todos_resultados(query)

    return tickets


def buscar_ticket_por_id(ticket_id):
    """
    Busca um ticket específico pelo ID.

    Args:
        ticket_id (int): ID do ticket.

    Returns:
        dict | None: Ticket encontrado ou None.
    """

    url = (
        f"https://{SUBDOMAIN}.zendesk.com"
        f"/api/v2/tickets/{ticket_id}.json"
    )

    response = fazer_request(
        url,
        params={"include": "slas"},
    )

    if response is None:
        return None

    data = response.json()

    return data.get("ticket")