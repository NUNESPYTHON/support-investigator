"""
===========================================================
Zendesk Investigator
===========================================================

Versão:
MVP 0.1

Missão:
Reduzimos o tempo de investigação para que você passe mais
tempo resolvendo problemas do que procurando informações.

Autor:
Elias Nunes

===========================================================
"""


from config.settings import (
    SUBDOMAIN,
    EMAIL,
)


def main():

    print("=" * 60)
    print("🔎 Zendesk Investigator")
    print("=" * 60)

    print()

    print("Subdomain:", SUBDOMAIN)

    print("Email:", EMAIL)


if __name__ == "__main__":
    main()