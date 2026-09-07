from services.customer_diagnostics import diagnosticar_cliente


diagnostico = diagnosticar_cliente(
    "elias.nunes@zendesk.com"
)

if diagnostico is None:

    print("Cliente não encontrado.")

else:

    print()
    print("=" * 60)
    print("DIAGNÓSTICO DO CLIENTE")
    print("=" * 60)

    print()

    print("E-mail:", diagnostico["email"])

    print(
        "Total de tickets:",
        diagnostico["total_tickets"]
    )

    print(
        "Abertos:",
        diagnostico["abertos"]
    )

    print(
        "Pendentes:",
        diagnostico["pendentes"]
    )

    print(
        "Resolvidos:",
        diagnostico["resolvidos"]
    )
    print(
            "Fechados:",
            diagnostico["fechados"]
        )
print()
print("Últimos tickets:")
print()

for ticket in diagnostico["ultimos_tickets"]:

    print(
        f"#{ticket.get('id')} | "
        f"{ticket.get('status')} | "
        f"{ticket.get('subject') or 'Sem assunto'}"
    )
    
print()

print("Resumo:")

print(diagnostico["resumo"])

print()
print() 

print("=" * 60)