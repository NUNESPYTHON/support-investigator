"""
==========================================================
Support Investigator V2

Arquivo:
i18n.py

Responsabilidade:
Gerenciar idioma e traduções da aplicação.

Idiomas suportados:
Português
English
Español

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st


# ==========================================================
# IDIOMAS
# ==========================================================

IDIOMAS = {
    "pt": "Português",
    "en": "English",
    "es": "Español",
}


# ==========================================================
# DETECÇÃO DO IDIOMA DO NAVEGADOR
# ==========================================================

def detectar_idioma_navegador() -> str:
    """
    Detecta o idioma preferido do navegador.

    Retorna:
        pt, en ou es
    """

    try:

        locale = st.context.locale

    except Exception:

        locale = None

    if not locale:

        return "pt"

    locale = locale.lower()

    if locale.startswith("pt"):

        return "pt"

    if locale.startswith("es"):

        return "es"

    if locale.startswith("en"):

        return "en"

    return "pt"


# ==========================================================
# INICIALIZAÇÃO DO IDIOMA
# ==========================================================

def inicializar_idioma():
    """
    Define o idioma inicial da aplicação.

    Se o usuário já escolheu manualmente um idioma,
    mantém a escolha.

    Caso contrário, usa o idioma do navegador.
    """

    if "language_code" in st.session_state:

        return

    idioma = detectar_idioma_navegador()

    st.session_state[
        "language_code"
    ] = idioma


# ==========================================================
# DEFINIR IDIOMA
# ==========================================================

def definir_idioma(idioma: str):
    """
    Define o idioma atual.
    """

    if idioma not in IDIOMAS:

        idioma = "pt"

    st.session_state[
        "language_code"
    ] = idioma


# ==========================================================
# OBTER IDIOMA
# ==========================================================

def obter_idioma() -> str:
    """
    Retorna o idioma atual.
    """

    return st.session_state.get(
        "language_code",
        "pt",
    )


# ==========================================================
# NOME DO IDIOMA
# ==========================================================

def obter_nome_idioma() -> str:
    """
    Retorna o nome amigável do idioma atual.
    """

    return IDIOMAS.get(
        obter_idioma(),
        "Português",
    )


# ==========================================================
# TRADUÇÕES
# ==========================================================

TRADUCOES = {

    # ------------------------------------------------------
    # APLICAÇÃO
    # ------------------------------------------------------

    "app_description": {
        "pt": "Consulte informações de suporte de forma rápida e objetiva.",
        "en": "Access support information quickly and efficiently.",
        "es": "Consulte información de soporte de forma rápida y objetiva.",
    },

    "welcome": {
        "pt": "Bem-vindo",
        "en": "Welcome",
        "es": "Bienvenido",
    },

    # ------------------------------------------------------
    # CONTA
    # ------------------------------------------------------

    "account": {
        "pt": "Conta",
        "en": "Account",
        "es": "Cuenta",
    },

    # ------------------------------------------------------
    # NAVEGAÇÃO
    # ------------------------------------------------------

    "navigation": {
        "pt": "Navegação",
        "en": "Navigation",
        "es": "Navegación",
    },

    # ------------------------------------------------------
    # IDIOMA
    # ------------------------------------------------------

    "language": {
        "pt": "Idioma",
        "en": "Language",
        "es": "Idioma",
    },

    # ------------------------------------------------------
    # PÁGINAS
    # ------------------------------------------------------

    "dashboard": {
        "pt": "Início",
        "en": "Dashboard",
        "es": "Panel",
    },

    "zendesk": {
        "pt": "Zendesk",
        "en": "Zendesk",
        "es": "Zendesk",
    },

    "investigator": {
        "pt": "Investigação",
        "en": "Investigator",
        "es": "Investigator",
    },

    "export": {
        "pt": "Exportação",
        "en": "Export",
        "es": "Exportación",
    },

    "billing": {
        "pt": "Assinatura",
        "en": "Subscription",
        "es": "Facturación",
    },

    "settings": {
        "pt": "Configurações",
        "en": "Settings",
        "es": "Configuración",
    },
    # ------------------------------------------------------
    # AÇÕES
    # ------------------------------------------------------

    "logout": {
        "pt": "Sair",
        "en": "Logout",
        "es": "Cerrar sesión",
    },

    "connect_zendesk": {
        "pt": "Conectar ao Zendesk",
        "en": "Connect to Zendesk",
        "es": "Conectar a Zendesk",
    },

    # ------------------------------------------------------
    # INVESTIGAÇÃO
    # ------------------------------------------------------

    "ticket_details": {
        "pt": "Detalhes do Ticket",
        "en": "Ticket Details",
        "es": "Detalles del Ticket",
    },

    "customer_history": {
        "pt": "Histórico de Interações",
        "en": "Interaction History",
        "es": "Historial de Interacciones",
    },

    # ------------------------------------------------------
    # DADOS DO USUÁRIO
    # ------------------------------------------------------

    "company": {
        "pt": "Empresa",
        "en": "Company",
        "es": "Empresa",
    },

    "status": {
        "pt": "Status",
        "en": "Status",
        "es": "Estado",
    },

    # ------------------------------------------------------
    # ASSINATURA
    # ------------------------------------------------------

    "subscription": {
        "pt": "Assinatura",
        "en": "Subscription",
        "es": "Suscripción",
    },
}


# ==========================================================
# FUNÇÃO DE TRADUÇÃO
# ==========================================================

def t(chave: str) -> str:
    """
    Retorna a tradução da chave no idioma atual.
    """

    idioma = obter_idioma()

    traducoes = TRADUCOES.get(
        chave
    )

    if not traducoes:

        return chave

    return traducoes.get(
        idioma,
        traducoes.get(
            "pt",
            chave,
        ),
    )