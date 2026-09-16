"""
==========================================================
Support Investigator

Arquivo:
metrics.py

Responsabilidade:
Consultar métricas de tickets na API da Zendesk.

Autor:
Elias Nunes
==========================================================
"""

from services.auth import montar_url
from services.zendesk import fazer_request


# ==========================================================
# BUSCAR MÉTRICAS DO TICKET
# ==========================================================

def buscar_metricas_ticket(ticket_id):
    """
    Busca as métricas de um ticket específico.

    Args:
        ticket_id (int): ID do ticket.

    Returns:
        dict | None
    """

    url = montar_url(
        f"/api/v2/tickets/{ticket_id}/metrics"
    )

    response = fazer_request(
        url
    )

    if response is None:
        return None

    data = response.json()

    return data.get(
        "ticket_metric"
    )