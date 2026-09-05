from services.tickets import buscar_tickets_por_email


tickets = buscar_tickets_por_email(
    "elias.nunes@zendesk.com"
)

print("Quantidade:", len(tickets))

print()

for ticket in tickets:

    print(
        "ID:", ticket.get("id"),
        "| Status:", ticket.get("status"),
        "| Assunto:", ticket.get("subject"),
    )