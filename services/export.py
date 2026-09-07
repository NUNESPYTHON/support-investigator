"""
==========================================================
Support Investigator

Arquivo:
export.py

Responsabilidade:
Preparar dados de tickets para exportação em CSV e Excel.

Autor:
Elias Nunes
==========================================================
"""

import csv
import io

from openpyxl import Workbook


STATUS_MAP = {
    "Todos": None,
    "Novo": "new",
    "Aberto": "open",
    "Pendente": "pending",
    "Resolvido": "solved",
    "Fechado": "closed",
}


def filtrar_tickets_por_status(tickets, status=None):
    """
    Filtra tickets pelo status informado.

    Args:
        tickets (list): Lista de tickets.
        status (str | None): Status da API Zendesk.

    Returns:
        list: Tickets filtrados.
    """

    if status is None:
        return tickets

    return [
        ticket
        for ticket in tickets
        if ticket.get("status") == status
    ]


def preparar_linhas_exportacao(tickets):
    """
    Converte tickets para linhas de exportação.

    Returns:
        list: Linhas contendo ID, status e assunto.
    """

    linhas = []

    for ticket in tickets:

        linhas.append(
            [
                ticket.get("id"),
                ticket.get("status"),
                ticket.get("subject") or "Sem assunto",
            ]
        )

    return linhas


def gerar_csv_bytes(tickets):
    """
    Gera o conteúdo CSV em memória.

    Returns:
        bytes: Conteúdo do CSV.
    """

    buffer = io.StringIO(
        newline=""
    )

    writer = csv.writer(buffer)

    writer.writerow(
        [
            "Ticket ID",
            "Status",
            "Assunto",
        ]
    )

    for linha in preparar_linhas_exportacao(tickets):
        writer.writerow(linha)

    return buffer.getvalue().encode(
        "utf-8-sig"
    )


def gerar_excel_bytes(tickets):
    """
    Gera um arquivo Excel em memória.

    Returns:
        bytes: Conteúdo do arquivo XLSX.
    """

    workbook = Workbook()

    worksheet = workbook.active

    worksheet.title = "Tickets"

    worksheet.append(
        [
            "Ticket ID",
            "Status",
            "Assunto",
        ]
    )

    for linha in preparar_linhas_exportacao(tickets):
        worksheet.append(linha)

    worksheet.freeze_panes = "A2"

    worksheet.column_dimensions["A"].width = 15
    worksheet.column_dimensions["B"].width = 15
    worksheet.column_dimensions["C"].width = 60

    buffer = io.BytesIO()

    workbook.save(buffer)

    return buffer.getvalue()


def exportar_tickets_csv(
    tickets,
    caminho_arquivo,
    status=None,
):
    """
    Exporta tickets para um arquivo CSV.

    Mantida para compatibilidade com os testes
    anteriores do projeto.
    """

    tickets_filtrados = filtrar_tickets_por_status(
        tickets,
        status,
    )

    with open(
        caminho_arquivo,
        "wb",
    ) as arquivo:

        arquivo.write(
            gerar_csv_bytes(tickets_filtrados)
        )

    return caminho_arquivo