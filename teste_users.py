from services.users import buscar_usuario_por_email


usuario = buscar_usuario_por_email(
    "elias.nunes@zendesk.com"
)

print(usuario)