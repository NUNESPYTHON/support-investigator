from services.users import buscar_usuario_por_id


usuario = buscar_usuario_por_id(1904605981913)

if usuario is None:
    print("Usuário não encontrado.")
else:
    print("Usuário encontrado:")
    print("ID:", usuario.get("id"))
    print("Nome:", usuario.get("nome"))
    print("Email:", usuario.get("email"))
    print("Role:", usuario.get("role"))