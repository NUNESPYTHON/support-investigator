from services.users import buscar_usuario_por_email
from services.search import (
    montar_query_tickets,
    buscar_todos_resultados,
)


def buscar_tickets_por_email(email):
    """
    Busca todos os tickets de um usuário.

    Args:
        email (str): E-mail do solicitante.

    Returns:
        list
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
        dict | None
    """

    from config.settings import SUBDOMAIN
    from services.zendesk import fazer_request

    url = (
        f"https://{SUBDOMAIN}.zendesk.com"
        f"/api/v2/tickets/{ticket_id}.json"
    )

    response = fazer_request(
    url,
    params={"include": "slas"}
)

    if response is None:
        return None

    data = response.json()

    return data.get("ticket")