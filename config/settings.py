"""
==========================================================
Zendesk Investigator

Arquivo:
settings.py

Responsabilidade:
Centralizar todas as configurações da aplicação.

Autor:
Elias Nunes

==========================================================
"""

# ==========================================================
# CONFIGURAÇÕES DA ZENDESK
# ==========================================================

SUBDOMAIN = ""

EMAIL = ""

API_TOKEN = ""

"""
==========================================================
Zendesk Investigator

Arquivo:
settings.py

Responsabilidade:
Carregar as configurações da aplicação.

Autor:
Elias Nunes
==========================================================
"""

import os
from pathlib import Path

from dotenv import load_dotenv


# Localização da pasta raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Localização do arquivo .env
ENV_FILE = BASE_DIR / ".env"

# Carrega explicitamente o arquivo .env
load_dotenv(ENV_FILE)


# Configurações da Zendesk
SUBDOMAIN = os.getenv("ZENDESK_SUBDOMAIN")
EMAIL = os.getenv("ZENDESK_EMAIL")
API_TOKEN = os.getenv("ZENDESK_API_TOKEN")