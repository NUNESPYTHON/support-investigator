from services.search import buscar_todos_resultados


query = 'type:ticket "Postman"'

resultados = buscar_todos_resultados(query)

print("Quantidade de resultados:", len(resultados))

for resultado in resultados:
    print(
        "ID:", resultado.get("id"),
        "| Status:", resultado.get("status"),
        "| Assunto:", resultado.get("subject")
    )