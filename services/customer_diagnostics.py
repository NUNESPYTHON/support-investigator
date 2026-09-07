"""
==========================================================
Zendesk Investigator

Arquivo:
customer_diagnostics.py

Responsabilidade:
Montar um diagnóstico consolidado de um cliente.

Autor:
Elias Nunes
==========================================================
"""

from services.tickets import buscar_tickets_por_email


def gerar_resumo_cliente(total, abertos, pendentes, resolvidos, fechados):
    """
    Gera um resumo executivo do histórico de interações do cliente.

    Args:
        total (int): Total de tickets.
        abertos (int): Tickets abertos.
        pendentes (int): Tickets pendentes.
        resolvidos (int): Tickets resolvidos.
        fechados (int): Tickets fechados.

    Returns:
        str: Resumo do histórico do cliente.
    """

    ativos = abertos + pendentes

    if ativos > 0:
        return (
            f"O cliente possui {ativos} tickets que "
            "ainda necessitam acompanhamento."
        )

    if total > 0 and fechados == total:
        return (
            "Todos os tickets do cliente foram concluídos."
        )

    if resolvidos > 0:
        return (
            f"O cliente possui {resolvidos} tickets "
            "resolvidos e nenhum ticket ativo."
        )

    return "Não há tickets ativos para acompanhamento."


def diagnosticar_cliente(email):
    """
    Busca os tickets de um cliente e consolida
    informações importantes para consulta rápida.
    """

    tickets = buscar_tickets_por_email(email)

    if not tickets:
        return None

    total = len(tickets)

    abertos = 0
    pendentes = 0
    resolvidos = 0
    fechados = 0

    for ticket in tickets:

        status = ticket.get("status")

        if status == "open":
            abertos += 1

        elif status == "pending":
            pendentes += 1

        elif status == "solved":
            resolvidos += 1

        elif status == "closed":
            fechados += 1

    resumo = gerar_resumo_cliente(
        total,
        abertos,
        pendentes,
        resolvidos,
        fechados
    )

    return {
        "email": email,
        "total_tickets": total,
        "abertos": abertos,
        "pendentes": pendentes,
        "resolvidos": resolvidos,
        "fechados": fechados,
        "ultimos_tickets": tickets[:3],
        "resumo": resumo,
    }