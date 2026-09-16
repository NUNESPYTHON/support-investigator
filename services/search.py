"""
==========================================================
Support Investigator

Arquivo:
search.py

Responsabilidade:
Centralizar as consultas realizadas pela Search API
da Zendesk.

Autor:
Elias Nunes
==========================================================
"""

from services.auth import montar_url
from services.zendesk import fazer_request


# ==========================================================
# BUSCAR TODOS OS RESULTADOS
# ==========================================================

def buscar_todos_resultados(query):
    """
    Busca todos os resultados de uma consulta na Search API.

    Args:
        query (str): Consulta no formato da Search API.

    Returns:
        list: Lista de resultados encontrados.
    """

    resultados_finais = []

    url = montar_url(
        "/api/v2/search.json"
    )

    params = {
        "query": query
    }

    while url is not None:

        response = fazer_request(
            url,
            params=params
        )

        if response is None:
            break

        data = response.json()

        resultados = data.get(
            "results",
            []
        )

        resultados_finais.extend(
            resultados
        )

        url = data.get(
            "next_page"
        )

        params = None

    return resultados_finais


# ==========================================================
# MONTAR QUERY DE TICKETS
# ==========================================================

def montar_query_tickets(
    user_id,
    status=None,
    data_inicial=None,
    data_final=None,
):
    """
    Monta uma consulta para a Search API.

    Args:
        user_id (int):
            ID do solicitante.

        status (str, optional):
            Status do ticket.

        data_inicial (str, optional):
            Data inicial (YYYY-MM-DD).

        data_final (str, optional):
            Data final (YYYY-MM-DD).

    Returns:
        str
    """

    query = (
        f"type:ticket requester:{user_id}"
    )

    if status:

        query += (
            f" status:{status}"
        )

    if data_inicial:

        query += (
            f" created>={data_inicial}"
        )

    if data_final:

        query += (
            f" created<={data_final}"
        )

    return query