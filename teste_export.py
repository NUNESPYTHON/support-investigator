from services.export import exportar_tickets_csv
from services.tickets import buscar_tickets_por_email


print()
print("=" * 60)
print("EXPORTAÇÃO CSV")
print("=" * 60)
print()

email = input(
    "Digite o e-mail do cliente: "
).strip()

print()

print("Escolha o status:")

print("0 - Todos")
print("1 - Novo")
print("2 - Aberto")
print("3 - Pendente")
print("4 - Resolvido")
print("5 - Fechado")

print()

opcao = input(
    "Opção: "
).strip()

status = None
nome_arquivo = "tickets.csv"

if opcao == "1":
    status = "new"
    nome_arquivo = "tickets_novos.csv"

elif opcao == "2":
    status = "open"
    nome_arquivo = "tickets_abertos.csv"

elif opcao == "3":
    status = "pending"
    nome_arquivo = "tickets_pendentes.csv"

elif opcao == "4":
    status = "solved"
    nome_arquivo = "tickets_resolvidos.csv"

elif opcao == "5":
    status = "closed"
    nome_arquivo = "tickets_fechados.csv"

tickets = buscar_tickets_por_email(email)

if not tickets:

    print()

    print("Nenhum ticket encontrado.")

else:

    caminho = exportar_tickets_csv(
        tickets,
        nome_arquivo,
        status=status,
    )

    quantidade = len(
        [
            ticket
            for ticket in tickets
            if status is None
            or ticket.get("status") == status
        ]
    )

    print()

    print("=" * 60)
    print("EXPORTAÇÃO CONCLUÍDA")
    print("=" * 60)

    print()

    print("Arquivo:", caminho)

    print("Quantidade exportada:", quantidade)

    print()

    print("=" * 60)