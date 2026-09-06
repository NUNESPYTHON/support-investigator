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

    print("1 - Buscar usuário")
    print("2 - Buscar tickets por e-mail")
    print("3 - Buscar ticket por ID")
    print("4 - Consultar primeira resposta")
    print("0 - Sair")

    print("-" * 60)


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
        assunto = ticket.get("subject") or "Sem assunto"

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


def executar_opcao(opcao):
    """
    Executa a ação correspondente à opção escolhida.

    Returns:
        bool:
            True mantém a aplicação rodando.
            False encerra a aplicação.
    """

    if opcao == "1":

        print(
            "\nBusca de usuário ainda está "
            "em desenvolvimento."
        )

    elif opcao == "2":

        buscar_tickets()

    elif opcao == "3":

        print(
            "\nBusca de ticket por ID ainda está "
            "em desenvolvimento."
        )

    elif opcao == "4":

        print(
            "\nConsulta de primeira resposta ainda está "
            "em desenvolvimento."
        )

    elif opcao == "0":

        print("\nAté logo! 👋")
        return False

    else:

        print("\nOpção inválida.")

    return True


def main():
    """Inicia o Investigator."""

    while True:

        mostrar_cabecalho()

        mostrar_menu()

        opcao = input(
            "\nEscolha uma opção: "
        ).strip()

        continuar = executar_opcao(opcao)

        if not continuar:
            break


if __name__ == "__main__":
    main()