"""
==========================================================
Support Investigator V2

Arquivo:
stripe_service.py

Responsabilidade:
Integração do Support Investigator com o Stripe.

Autor:
Elias Nunes
==========================================================
"""

import os

import stripe
from dotenv import load_dotenv


load_dotenv()


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

STRIPE_SECRET_KEY = os.getenv(
    "STRIPE_SECRET_KEY"
)

STRIPE_PRICE_ID = os.getenv(
    "STRIPE_PRICE_ID"
)

STRIPE_SUCCESS_URL = os.getenv(
    "STRIPE_SUCCESS_URL",
    "http://localhost:8501/?billing=success",
)

STRIPE_CANCEL_URL = os.getenv(
    "STRIPE_CANCEL_URL",
    "http://localhost:8501/?billing=cancel",
)

STRIPE_PORTAL_RETURN_URL = os.getenv(
    "STRIPE_PORTAL_RETURN_URL",
    "http://localhost:8501/?billing=portal",
)

STRIPE_TRIAL_DAYS = 7


# ==========================================================
# VALIDAÇÃO
# ==========================================================

if not STRIPE_SECRET_KEY:

    raise RuntimeError(
        "STRIPE_SECRET_KEY não configurada."
    )


if not STRIPE_PRICE_ID:

    raise RuntimeError(
        "STRIPE_PRICE_ID não configurado."
    )


# ==========================================================
# STRIPE
# ==========================================================

stripe.api_key = STRIPE_SECRET_KEY


# ==========================================================
# CHECKOUT
# ==========================================================

def create_checkout_session(
    customer_email: str | None = None,
    user_id: str | None = None,
):
    """
    Cria uma sessão do Stripe Checkout
    para uma assinatura recorrente com
    7 dias de teste gratuito.

    O user_id do Support Investigator é
    enviado ao Stripe para permitir que
    o webhook identifique o usuário.
    """

    params = {
        "mode": "subscription",

        "line_items": [
            {
                "price": STRIPE_PRICE_ID,
                "quantity": 1,
            }
        ],

        "success_url": STRIPE_SUCCESS_URL,

        "cancel_url": STRIPE_CANCEL_URL,

        "subscription_data": {
            "trial_period_days": STRIPE_TRIAL_DAYS,
            "metadata": {},
        },
    }

    # ------------------------------------------------------
    # E-MAIL
    # ------------------------------------------------------

    if customer_email:

        params["customer_email"] = (
            customer_email
        )

    # ------------------------------------------------------
    # IDENTIFICADOR DO USUÁRIO
    # ------------------------------------------------------

    if user_id:

        params["client_reference_id"] = user_id

        params[
            "subscription_data"
        ][
            "metadata"
        ][
            "user_id"
        ] = user_id

    # ------------------------------------------------------
    # CRIAR SESSION
    # ------------------------------------------------------

    session = stripe.checkout.Session.create(
        **params
    )

    return session


# ==========================================================
# CUSTOMER PORTAL
# ==========================================================

def create_customer_portal_session(
    stripe_customer_id: str,
    return_url: str | None = None,
):
    """
    Cria uma sessão do Stripe Customer Portal.

    O cliente poderá usar o portal para:
    - atualizar o cartão;
    - gerenciar a assinatura;
    - cancelar a assinatura;
    - atualizar informações de cobrança.

    Args:
        stripe_customer_id:
            ID do cliente na Stripe.

        return_url:
            URL para a qual o cliente retornará
            após sair do Customer Portal.

    Returns:
        stripe.billing_portal.Session:
            Sessão criada pelo Stripe.
    """

    if not stripe_customer_id:

        raise ValueError(
            "Stripe Customer ID não informado."
        )

    portal_return_url = (
        return_url
        or STRIPE_PORTAL_RETURN_URL
    )

    session = stripe.billing_portal.Session.create(
        customer=stripe_customer_id,
        return_url=portal_return_url,
    )

    return session