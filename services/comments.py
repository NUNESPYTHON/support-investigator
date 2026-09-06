"""
==========================================================
Zendesk Investigator

Arquivo:
comments.py

Responsabilidade:
Consultar as interações e comentários públicos
de tickets na API da Zendesk.

Autor:
Elias Nunes
==========================================================
"""

from config.settings import SUBDOMAIN
from services.zendesk import fazer_request
from services.users import buscar_usuario_por_id
from utils.formatters import formatar_data


def buscar_ultima_interacao(ticket_id):
    """
    Busca a última interação pública de um ticket.

    Args:
        ticket_id (int): ID do ticket.

    Returns:
        dict | None
    """

    url = (
        f"https://{SUBDOMAIN}.zendesk.com"
        f"/api/v2/tickets/{ticket_id}/comments"
    )

    params = {
        "sort": "-created_at",
        "per_page": 100,
    }

    while url is not None:

        response = fazer_request(
            url,
            params=params
        )

        if response is None:
            return None

        data = response.json()

        comentarios = data.get(
            "comments",
            []
        )

        for comentario in comentarios:

            if comentario.get("public") is True:
                autor = buscar_usuario_por_id(
                comentario.get("author_id")
)

                return {
                    "id": comentario.get("id"),
                    "autor": (
    autor.get("nome")
    if autor
    else "Não identificado"
),

"autor_id": comentario.get("author_id"),
                    "data": formatar_data(
    comentario.get("created_at")
),
                    "texto": (
                        comentario.get("plain_body")
                        or comentario.get("body")
                        or ""
                    ),
                }

        url = data.get("next_page")

        params = None

    return None