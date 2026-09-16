"""
==========================================================
Support Investigator

Arquivo:
users.py

Responsabilidade:
Consultar informações de usuários na API da Zendesk.

Autor:
Elias Nunes
==========================================================
"""

from services.auth import montar_url
from services.zendesk import fazer_request


# ==========================================================
# BUSCAR USUÁRIO POR E-MAIL
# ==========================================================

def buscar_usuario_por_email(email):
    """
    Busca um usuário pelo endereço de e-mail.

    Args:
        email (str): E-mail do usuário.

    Returns:
        dict | None
    """

    url = montar_url(
        "/api/v2/users/search.json"
    )

    params = {
        "query": email
    }

    response = fazer_request(
        url,
        params=params
    )

    if response is None:
        return None

    data = response.json()

    usuarios = data.get(
        "users",
        []
    )

    if len(usuarios) == 0:
        return None

    usuario = usuarios[0]

    return {
        "id": usuario.get("id"),
        "nome": usuario.get("name"),
        "email": usuario.get("email"),
        "role": usuario.get("role"),
    }


# ==========================================================
# BUSCAR USUÁRIO POR ID
# ==========================================================

def buscar_usuario_por_id(user_id):
    """
    Busca um usuário pelo ID na API da Zendesk.

    Args:
        user_id (int): ID do usuário.

    Returns:
        dict | None
    """

    url = montar_url(
        f"/api/v2/users/{user_id}.json"
    )

    response = fazer_request(
        url
    )

    if response is None:
        return None

    data = response.json()

    usuario = data.get(
        "user"
    )

    if usuario is None:
        return None

    return {
        "id": usuario.get("id"),
        "nome": usuario.get("name"),
        "email": usuario.get("email"),
        "role": usuario.get("role"),
    }