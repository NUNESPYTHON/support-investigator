"""
==========================================================
Support Investigator

Arquivo:
authentication.py

Responsabilidade:
Centralizar a autenticação dos usuários
do Support Investigator via Supabase Auth.

Autor:
Elias Nunes
==========================================================
"""

from services.supabase import get_supabase


def criar_usuario(
    email: str,
    senha: str,
    nome: str,
    empresa: str = "",
):
    """
    Cria uma nova conta de usuário.

    Nome e empresa são enviados como metadata
    para o Supabase Auth.

    O trigger do banco cria automaticamente
    o registro correspondente em public.profiles.
    """

    supabase = get_supabase()

    response = supabase.auth.sign_up(
        {
            "email": email.strip(),
            "password": senha,
            "options": {
                "data": {
                    "name": nome.strip(),
                    "company": empresa.strip(),
                },
                "email_redirect_to": "http://localhost:8501",
            },
        }
    )

    return response


def fazer_login(email: str, senha: str):
    """
    Realiza login com e-mail e senha.
    """

    supabase = get_supabase()

    response = supabase.auth.sign_in_with_password(
        {
            "email": email.strip(),
            "password": senha,
        }
    )

    return response


def fazer_logout():
    """
    Encerra a sessão atual do usuário.
    """

    supabase = get_supabase()

    return supabase.auth.sign_out()


def solicitar_recuperacao_senha(email: str):
    """
    Solicita o envio do e-mail de recuperação de senha.
    """

    supabase = get_supabase()

    return supabase.auth.reset_password_for_email(
        email.strip()
    )


def obter_usuario_atual():
    """
    Retorna o usuário autenticado na sessão atual.
    """

    supabase = get_supabase()

    return supabase.auth.get_user()