"""
==========================================================
Zendesk Investigator

Arquivo:
users.py

Responsabilidade:
Consultar informações de usuários na API da Zendesk.

Autor:
Elias Nunes

==========================================================
"""

from services.zendesk import fazer_request
from config.settings import SUBDOMAIN


def buscar_usuario_por_email(email):
    """
    Busca um usuário pelo endereço de e-mail.

    Args:
        email (str): E-mail do usuário.

    Returns:
        dict | None
    """

    url = (
        f"https://{SUBDOMAIN}.zendesk.com"
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