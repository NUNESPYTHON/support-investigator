"""
==========================================================
Support Investigator

Arquivo:
settings.py

Responsabilidade:
Centralizar e carregar todas as configurações da aplicação.

Autor:
Elias Nunes
==========================================================
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# ==========================================================
# DIRETÓRIOS E ARQUIVO .ENV
# ==========================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ENV_FILE = BASE_DIR / ".env"

load_dotenv(ENV_FILE)


# ==========================================================
# CONFIGURAÇÕES DA ZENDESK
# ==========================================================

SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")

EMAIL = os.getenv("ZENDESK_EMAIL")

API_TOKEN = os.getenv("ZENDESK_API_TOKEN")


# ==========================================================
# CONFIGURAÇÕES OAUTH
# ==========================================================

ZENDESK_OAUTH_CLIENT_ID = os.getenv(
    "ZENDESK_OAUTH_CLIENT_ID"
)

ZENDESK_OAUTH_CLIENT_SECRET = os.getenv(
    "ZENDESK_OAUTH_CLIENT_SECRET"
)

ZENDESK_OAUTH_REDIRECT_URI = os.getenv(
    "ZENDESK_OAUTH_REDIRECT_URI"
)