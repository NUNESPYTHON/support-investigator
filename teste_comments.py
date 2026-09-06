from services.comments import buscar_ultima_interacao


interacao = buscar_ultima_interacao(1114)

if interacao is None:

    print("Nenhuma interação pública encontrada.")

else:

    print()
    print("=" * 60)
    print("ÚLTIMA INTERAÇÃO")
    print("=" * 60)

    print()
    print("Autor:", interacao["autor"])
    print("Data:", interacao["data"])
    print("Texto:", interacao["texto"])

    print()
    print("=" * 60)