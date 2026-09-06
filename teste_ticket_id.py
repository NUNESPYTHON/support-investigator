from services.tickets import buscar_ticket_por_id


ticket = buscar_ticket_por_id(1114)

if ticket is None:
    print("Ticket não encontrado.")
else:
    print("Ticket encontrado:")
    print("ID:", ticket.get("id"))
    print("Status:", ticket.get("status"))
    print("Assunto:", ticket.get("subject"))
    print("Requester ID:", ticket.get("requester_id"))
    print("Assignee ID:", ticket.get("assignee_id"))
    