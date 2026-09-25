"""
==========================================================
Support Investigator V2

Arquivo:
webhook_server.py

Responsabilidade:
Receber e processar webhooks enviados pelo Stripe.

Autor:
Elias Nunes
==========================================================
"""

import os
from datetime import datetime, timezone

import stripe

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException, Request

from services.subscription import (
    salvar_assinatura_por_user_id,
    atualizar_assinatura_por_user_id,
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

load_dotenv()

STRIPE_SECRET_KEY = os.getenv(
    "STRIPE_SECRET_KEY"
)

STRIPE_WEBHOOK_SECRET = os.getenv(
    "STRIPE_WEBHOOK_SECRET"
)


if not STRIPE_SECRET_KEY:
    raise RuntimeError(
        "STRIPE_SECRET_KEY não configurada."
    )


stripe.api_key = STRIPE_SECRET_KEY


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI(
    title="Support Investigator Stripe Webhook"
)


# ==========================================================
# HEALTH CHECK
# ==========================================================

@app.get("/")
async def health_check():
    return {
        "status": "ok",
        "service": "stripe-webhook",
    }


# ==========================================================
# AUXILIARES
# ==========================================================

def _timestamp_to_iso(timestamp):
    """
    Converte timestamp Unix do Stripe para ISO 8601.
    """

    if timestamp is None:
        return None

    return datetime.fromtimestamp(
        timestamp,
        tz=timezone.utc,
    ).isoformat()


def _get_metadata_dict(obj) -> dict:
    """
    Converte metadata do Stripe para dict.

    A biblioteca Stripe pode retornar metadata
    como StripeObject em vez de dict.
    """

    metadata = getattr(
        obj,
        "metadata",
        None,
    )

    if metadata is None:
        return {}

    if isinstance(
        metadata,
        dict,
    ):
        return metadata

    try:

        return metadata.to_dict()

    except AttributeError:

        return {}


def _extract_user_id_from_subscription(
    subscription,
) -> str | None:
    """
    Obtém o user_id armazenado na metadata
    da assinatura.
    """

    metadata = _get_metadata_dict(
        subscription
    )

    print("=" * 60)
    print("SUBSCRIPTION METADATA")
    print(metadata)
    print("=" * 60)

    user_id = metadata.get(
        "user_id"
    )

    if not user_id:
        return None

    return str(user_id)


def _extract_price_id(
    subscription,
) -> str | None:
    """
    Obtém o Price ID da assinatura.
    """

    items = getattr(
        subscription,
        "items",
        None,
    )

    if items is None:
        return None

    data = getattr(
        items,
        "data",
        None,
    )

    if not data:
        return None

    first_item = data[0]

    price = getattr(
        first_item,
        "price",
        None,
    )

    if price is None:
        return None

    return getattr(
        price,
        "id",
        None,
    )


def _extract_subscription_period(
    subscription,
):
    """
    Obtém current_period_start e
    current_period_end.

    Dependendo do formato do evento Stripe,
    esses campos podem estar diretamente no
    objeto subscription ou no primeiro
    subscription item.
    """

    current_period_start_timestamp = getattr(
        subscription,
        "current_period_start",
        None,
    )

    current_period_end_timestamp = getattr(
        subscription,
        "current_period_end",
        None,
    )

    items = getattr(
        subscription,
        "items",
        None,
    )

    items_data = (
        getattr(
            items,
            "data",
            [],
        )
        if items
        else []
    )

    first_item = (
        items_data[0]
        if items_data
        else None
    )

    if first_item:

        if not current_period_start_timestamp:

            current_period_start_timestamp = getattr(
                first_item,
                "current_period_start",
                None,
            )

        if not current_period_end_timestamp:

            current_period_end_timestamp = getattr(
                first_item,
                "current_period_end",
                None,
            )

    return (
        current_period_start_timestamp,
        current_period_end_timestamp,
    )


def _extract_cancel_at_period_end(
    subscription,
    current_period_end_timestamp=None,
):
    """
    Determina se o cancelamento está agendado
    para o final do período.

    A Stripe pode retornar:
        cancel_at_period_end = True

    ou, em alguns eventos:
        cancel_at = current_period_end
        cancel_at_period_end = False

    Neste segundo caso, tratamos o cancelamento
    como agendado para o final do período.
    """

    cancel_at_period_end = bool(
        getattr(
            subscription,
            "cancel_at_period_end",
            False,
        )
    )

    cancel_at = getattr(
        subscription,
        "cancel_at",
        None,
    )

    if (
        cancel_at
        and current_period_end_timestamp
        and cancel_at == current_period_end_timestamp
    ):
        cancel_at_period_end = True

    return cancel_at_period_end


def _log_subscription_state(
    status,
    current_period_start,
    current_period_end,
    cancel_at_period_end,
):
    """
    Registra no log o estado salvo da assinatura.
    """

    print(
        "[Stripe Webhook] Status:",
        status,
    )

    print(
        "[Stripe Webhook] Current period start:",
        current_period_start,
    )

    print(
        "[Stripe Webhook] Current period end:",
        current_period_end,
    )

    print(
        "[Stripe Webhook] Cancel at period end:",
        cancel_at_period_end,
    )


# ==========================================================
# STRIPE WEBHOOK
# ==========================================================

@app.post("/webhook")
async def stripe_webhook(
    request: Request,
):
    """
    Recebe, valida e processa eventos do Stripe.
    """

    if not STRIPE_WEBHOOK_SECRET:
        raise HTTPException(
            status_code=500,
            detail="Stripe webhook secret not configured.",
        )

    payload = await request.body()

    signature = request.headers.get(
        "stripe-signature"
    )

    if not signature:
        raise HTTPException(
            status_code=400,
            detail="Stripe-Signature header missing.",
        )

    # ======================================================
    # VALIDAR EVENTO
    # ======================================================

    try:

        event = stripe.Webhook.construct_event(
            payload,
            signature,
            STRIPE_WEBHOOK_SECRET,
        )

    except ValueError as erro:

        print(
            "[Stripe Webhook] Invalid payload:",
            erro,
        )

        raise HTTPException(
            status_code=400,
            detail="Invalid payload.",
        )

    except stripe.error.SignatureVerificationError as erro:

        print(
            "[Stripe Webhook] Invalid signature:",
            erro,
        )

        raise HTTPException(
            status_code=400,
            detail="Invalid Stripe signature.",
        )

    # ======================================================
    # EVENTO
    # ======================================================

    event_type = event.type

    print(
        f"[Stripe Webhook] Event received: {event_type}"
    )

    # ======================================================
    # CHECKOUT COMPLETED
    # ======================================================

    if event_type == "checkout.session.completed":

        session = event.data.object

        user_id = getattr(
            session,
            "client_reference_id",
            None,
        )

        customer_id = getattr(
            session,
            "customer",
            None,
        )

        subscription_id = getattr(
            session,
            "subscription",
            None,
        )

        print(
            "[Stripe Webhook] checkout.session.completed"
        )

        print(
            "User ID:",
            user_id,
        )

        print(
            "Session ID:",
            session.id,
        )

        print(
            "Customer ID:",
            customer_id,
        )

        print(
            "Subscription ID:",
            subscription_id,
        )

    # ======================================================
    # SUBSCRIPTION CREATED
    # ======================================================

    elif event_type == "customer.subscription.created":

        subscription = event.data.object

        user_id = _extract_user_id_from_subscription(
            subscription
        )

        customer_id = getattr(
            subscription,
            "customer",
            None,
        )

        subscription_id = getattr(
            subscription,
            "id",
            None,
        )

        status = getattr(
            subscription,
            "status",
            "inactive",
        )

        price_id = _extract_price_id(
            subscription
        )

        (
            current_period_start_timestamp,
            current_period_end_timestamp,
        ) = _extract_subscription_period(
            subscription
        )

        current_period_start = _timestamp_to_iso(
            current_period_start_timestamp
        )

        current_period_end = _timestamp_to_iso(
            current_period_end_timestamp
        )

        cancel_at_period_end = (
            _extract_cancel_at_period_end(
                subscription,
                current_period_end_timestamp,
            )
        )

        print(
            "[Stripe Webhook] customer.subscription.created"
        )

        print(
            "User ID:",
            user_id,
        )

        print(
            "Customer ID:",
            customer_id,
        )

        print(
            "Subscription ID:",
            subscription_id,
        )

        print(
            "Price ID:",
            price_id,
        )

        print(
            "Status:",
            status,
        )

        # --------------------------------------------------
        # SALVAR NO SUPABASE
        # --------------------------------------------------

        if not user_id:

            print(
                "[Stripe Webhook] "
                "user_id não encontrado na metadata."
            )

        else:

            resultado = salvar_assinatura_por_user_id(
                user_id=user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                stripe_price_id=price_id,
                subscription_status=status,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                cancel_at_period_end=cancel_at_period_end,
            )

            print(
                "[Stripe Webhook] Subscription saved:",
                resultado.get("id"),
            )

            _log_subscription_state(
                status=status,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                cancel_at_period_end=cancel_at_period_end,
            )

    # ======================================================
    # SUBSCRIPTION UPDATED
    # ======================================================

    elif event_type == "customer.subscription.updated":

        subscription = event.data.object

        user_id = _extract_user_id_from_subscription(
            subscription
        )

        if not user_id:

            print(
                "[Stripe Webhook] "
                "user_id não encontrado na metadata."
            )

        else:

            customer_id = getattr(
                subscription,
                "customer",
                None,
            )

            subscription_id = getattr(
                subscription,
                "id",
                None,
            )

            status = getattr(
                subscription,
                "status",
                "inactive",
            )

            price_id = _extract_price_id(
                subscription
            )

            (
                current_period_start_timestamp,
                current_period_end_timestamp,
            ) = _extract_subscription_period(
                subscription
            )

            current_period_start = _timestamp_to_iso(
                current_period_start_timestamp
            )

            current_period_end = _timestamp_to_iso(
                current_period_end_timestamp
            )

            cancel_at_period_end = (
                _extract_cancel_at_period_end(
                    subscription,
                    current_period_end_timestamp,
                )
            )

            print(
                "[Stripe Webhook] "
                "customer.subscription.updated"
            )

            print(
                "User ID:",
                user_id,
            )

            print(
                "Customer ID:",
                customer_id,
            )

            print(
                "Subscription ID:",
                subscription_id,
            )

            print(
                "Price ID:",
                price_id,
            )

            print(
                "Status:",
                status,
            )

            print(
                "Current period start:",
                current_period_start,
            )

            print(
                "Current period end:",
                current_period_end,
            )

            print(
                "Cancel at period end:",
                cancel_at_period_end,
            )

            resultado = atualizar_assinatura_por_user_id(
                user_id=user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                stripe_price_id=price_id,
                subscription_status=status,
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                cancel_at_period_end=cancel_at_period_end,
            )

            print(
                "[Stripe Webhook] Subscription updated:",
                resultado.get("id")
                if resultado
                else None,
            )

    # ======================================================
    # SUBSCRIPTION DELETED
    # ======================================================

    elif event_type == "customer.subscription.deleted":

        subscription = event.data.object

        user_id = _extract_user_id_from_subscription(
            subscription
        )

        if not user_id:

            print(
                "[Stripe Webhook] "
                "user_id não encontrado na metadata."
            )

        else:

            customer_id = getattr(
                subscription,
                "customer",
                None,
            )

            subscription_id = getattr(
                subscription,
                "id",
                None,
            )

            price_id = _extract_price_id(
                subscription
            )

            (
                current_period_start_timestamp,
                current_period_end_timestamp,
            ) = _extract_subscription_period(
                subscription
            )

            current_period_start = _timestamp_to_iso(
                current_period_start_timestamp
            )

            current_period_end = _timestamp_to_iso(
                current_period_end_timestamp
            )

            resultado = atualizar_assinatura_por_user_id(
                user_id=user_id,
                stripe_customer_id=customer_id,
                stripe_subscription_id=subscription_id,
                stripe_price_id=price_id,
                subscription_status="canceled",
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                cancel_at_period_end=False,
            )

            print(
                "[Stripe Webhook] Subscription canceled:",
                resultado.get("id")
                if resultado
                else None,
            )

            _log_subscription_state(
                status="canceled",
                current_period_start=current_period_start,
                current_period_end=current_period_end,
                cancel_at_period_end=False,
            )

    # ======================================================
    # PAYMENT FAILED
    # ======================================================

    elif event_type == "invoice.payment_failed":

        invoice = event.data.object

        print(
            "[Stripe Webhook] invoice.payment_failed"
        )

        print(
            "Invoice ID:",
            invoice.id,
        )

        print(
            "Customer ID:",
            getattr(
                invoice,
                "customer",
                None,
            ),
        )

    # ======================================================
    # OUTROS
    # ======================================================

    else:

        print(
            "[Stripe Webhook] Event ignored:",
            event_type,
        )

    # ======================================================
    # RESPOSTA
    # ======================================================

    return {
        "received": True,
        "event_type": event_type,
    }