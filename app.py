"""
==========================================================
Zendesk Investigator

Arquivo:
app.py

Responsabilidade:
Ponto de entrada da aplicação e interface inicial
do Investigator no terminal.

Autor:
Elias Nunes
==========================================================
"""

from services.customer_diagnostics import diagnosticar_cliente
from services.diagnostics import diagnosticar_ticket
from services.tickets import buscar_tickets_por_email


def mostrar_cabecalho():
    """Exibe o cabeçalho principal da aplicação."""

    print()
    print("=" * 60)
    print("🔎 Zendesk Investigator")
    print("=" * 60)

    print()
    print(
        "Reduzimos o tempo de investigação para que você passe"
    )
    print(
        "mais tempo resolvendo problemas do que procurando"
    )
    print(
        "informações."
    )

    print()
    print("-" * 60)


def mostrar_menu():
    """Exibe as opções disponíveis."""

    print("1 - Histórico de interações do cliente")
    print("2 - Buscar tickets por e-mail")
    print("3 - Diagnosticar ticket")
    print("4 - Consultar primeira resposta")
    print("0 - Sair")

    print("-" * 60)


def historico_cliente():
    """Solicita o e-mail e exibe o histórico do cliente."""

    print()

    email = input(
        "Digite o e-mail do cliente: "
    ).strip()

    if not email:

        print("\nE-mail não informado.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

        return

    diagnostico = diagnosticar_cliente(email)

    print()

    if diagnostico is None:

        print("Cliente não encontrado.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

        return

    print("=" * 60)
    print("👤 HISTÓRICO DE INTERAÇÕES DO CLIENTE")
    print("=" * 60)

    print()

    print(
        f"📧 E-mail: {diagnostico['email']}"
    )

    print(
        f"🎫 Total de tickets: "
        f"{diagnostico['total_tickets']}"
    )

    print(
        f"🟢 Abertos: "
        f"{diagnostico['abertos']}"
    )

    print(
        f"🔵 Pendentes: "
        f"{diagnostico['pendentes']}"
    )

    print(
        f"⚫ Resolvidos: "
        f"{diagnostico['resolvidos']}"
    )

    print(
        f"⚪ Fechados: "
        f"{diagnostico['fechados']}"
    )

    print()

    print("-" * 60)

    print()

    print("🎫 Últimos tickets")

    print()

    for ticket in diagnostico["ultimos_tickets"]:

        print(
            f"#{ticket.get('id')} | "
            f"{ticket.get('status')} | "
            f"{ticket.get('subject') or 'Sem assunto'}"
        )

    print()

    print("-" * 60)

    print()

    print("📝 Resumo")

    print()

    print(diagnostico["resumo"])

    print()

    print("=" * 60)

    input(
        "\nPressione Enter para voltar ao menu..."
    )


def buscar_tickets():
    """Solicita um e-mail e exibe os tickets encontrados."""

    print()

    email = input(
        "Digite o e-mail do cliente: "
    ).strip()

    if not email:

        print("\nE-mail não informado.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

        return

    tickets = buscar_tickets_por_email(email)

    print()

    print("=" * 60)
    print("RESULTADO DA CONSULTA")
    print("=" * 60)

    if not tickets:

        print()
        print("Nenhum ticket encontrado.")
        print()

        input(
            "Pressione Enter para voltar ao menu..."
        )

        return

    print()

    print(
        f"Tickets encontrados: {len(tickets)}"
    )

    print()

    for ticket in tickets:

        ticket_id = ticket.get("id")

        status = ticket.get("status")

        assunto = (
            ticket.get("subject")
            or "Sem assunto"
        )

        print(
            f"#{ticket_id} | "
            f"{status} | "
            f"{assunto}"
        )

    print()

    print("=" * 60)

    input(
        "\nPressione Enter para voltar ao menu..."
    )


def diagnosticar():
    """Solicita um ID de ticket e exibe o resumo executivo."""

    print()

    ticket_id = input(
        "Digite o ID do ticket: "
    ).strip()

    if not ticket_id.isdigit():

        print("\nID de ticket inválido.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

        return

    diagnostico = diagnosticar_ticket(
        int(ticket_id)
    )

    print()

    if diagnostico is None:

        print("Ticket não encontrado.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

        return

    print("=" * 60)
    print("🔎 RESUMO EXECUTIVO DO TICKET")
    print("=" * 60)

    print()

    print(
        f"🎫 Ticket: "
        f"{diagnostico['ticket_id']}"
    )

    print(
        f"🟡 Status: "
        f"{diagnostico['status']}"
    )

    print(
        f"📝 Assunto: "
        f"{diagnostico['assunto']}"
    )

    print(
        f"📧 Solicitante: "
        f"{diagnostico['solicitante']}"
    )

    print(
        f"👤 Responsável: "
        f"{diagnostico['responsavel']}"
    )

    print(
        f"⏱ Primeira resposta: "
        f"{diagnostico['primeira_resposta']}"
    )

    print()

    print("-" * 60)

    print()

    print("📝 Resumo")

    print()

    print(diagnostico["resumo"])

    print()

    print("-" * 60)

    print()

    print("💬 Última interação")

    print()

    ultima = diagnostico["ultima_interacao"]

    if ultima:

        print(
            f"👤 Autor: "
            f"{ultima['autor']}"
        )

        print(
            f"📅 Data: "
            f"{ultima['data']}"
        )

        print()

        print(
            f"💬 {ultima['texto']}"
        )

    else:

        print(
            "Nenhuma interação encontrada."
        )

    print()

    print("=" * 60)

    input(
        "\nPressione Enter para voltar ao menu..."
    )


def executar_opcao(opcao):
    """
    Executa a ação correspondente à opção escolhida.

    Returns:
        bool:
            True mantém a aplicação rodando.
            False encerra a aplicação.
    """

    if opcao == "1":

        historico_cliente()

    elif opcao == "2":

        buscar_tickets()

    elif opcao == "3":

        diagnosticar()

    elif opcao == "4":

        print(
            "\nConsulta de primeira resposta "
            "ainda está em desenvolvimento."
        )

        input(
            "\nPressione Enter para voltar ao menu..."
        )

    elif opcao == "0":

        print("\nAté logo! 👋")

        return False

    else:

        print("\nOpção inválida.")

        input(
            "\nPressione Enter para voltar ao menu..."
        )

    return True


def main():
    """Inicia o Investigator."""

    while True:

        mostrar_cabecalho()

        mostrar_menu()

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        continuar = executar_opcao(
            opcao
        )

        if not continuar:

            break


if __name__ == "__main__":
    main()