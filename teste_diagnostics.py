from services.diagnostics import diagnosticar_ticket


diagnostico = diagnosticar_ticket(1114)

if diagnostico is None:

    print("Ticket não encontrado.")

else:

    print()
    print("=" * 60)
    print("🔎 RESUMO EXECUTIVO DO TICKET")
    print("=" * 60)

    print()

    print(f"🎫 Ticket: {diagnostico['ticket_id']}")

    print(f"🟡 Status: {diagnostico['status']}")

    print(f"📝 Assunto: {diagnostico['assunto']}")

    print(f"📧 Solicitante: {diagnostico['solicitante']}")

    print(
        f"👤 Responsável: {diagnostico['responsavel']}"
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

    print()

    print("-" * 60)

    print()

    print("💬 Última interação")

    print()

    ultima = diagnostico["ultima_interacao"]

if ultima:

    print(f"👤 Autor: {ultima['autor']}")

    print(f"📅 Data: {ultima['data']}")

    print()

    print(f"💬 {ultima['texto']}")

else:

    print("Nenhuma interação encontrada.") 

    print()

    print("=" * 60)