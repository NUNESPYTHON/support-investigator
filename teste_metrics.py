from services.metrics import buscar_metricas_ticket
from utils.formatters import formatar_tempo


metricas = buscar_metricas_ticket(1114)

if metricas is None:
    print("Métricas não encontradas.")
else:
    print()
    print("=" * 60)
    print("MÉTRICAS DO TICKET")
    print("=" * 60)

    print()

    reply_time = metricas.get(
        "reply_time_in_minutes"
    )

    if reply_time:
        print(
            "Primeira resposta (calendário):",
            formatar_tempo(
                reply_time.get("calendar")
            )
        )

        print(
            "Primeira resposta (horário de operação):",
            formatar_tempo(
                reply_time.get("business")
            )
        )
    else:
        print(
            "Primeira resposta: Ainda não respondido"
        )

    print()
    print("=" * 60)