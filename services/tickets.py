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