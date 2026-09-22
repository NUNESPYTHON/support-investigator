"""
==========================================================
Support Investigator V2

Arquivo:
subscription.py

Responsabilidade:
Gerenciar a assinatura do usuário no Supabase.

Autor:
Elias Nunes
==========================================================
"""

from typing import Any

import streamlit as st

from services.supabase import (
    get_supabase,
    get_supabase_admin,
)


TABLE_NAME = "subscriptions"


def _get_user_id() -> str | None:
    """
    Retorna o ID do usuário autenticado na sessão
    do Streamlit.
    """

    usuario = st.session_state.get(
        "user"
    )

    if usuario is None:
        return None

    user_id = getattr(
        usuario,
        "id",
        None,
    )

    if not user_id:
        return None

    return str(user_id)


def buscar_assinatura() -> dict[str, Any] | None:
    """
    Busca a assinatura do usuário autenticado
    na sessão atual.
    """

    user_id = _get_user_id()

    if not user_id:
        return None

    supabase = get_supabase()

    response = (
        supabase
        .table(TABLE_NAME)
        .select(
            """
            id,
            user_id,
            stripe_customer_id,
            stripe_subscription_id,
            stripe_price_id,
            subscription_status,
            current_period_start,
            current_period_end,
            cancel_at_period_end,
            created_at,
            updated_at
            """
        )
        .eq(
            "user_id",
            user_id,
        )
        .limit(1)
        .execute()
    )

    if response is None:
        return None

    if not response.data:
        return None

    return response.data[0]


def salvar_assinatura(
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
    stripe_price_id: str | None = None,
    subscription_status: str = "inactive",
    current_period_start: str | None = None,
    current_period_end: str | None = None,
    cancel_at_period_end: bool = False,
) -> dict[str, Any]:
    """
    Cria ou atualiza a assinatura do usuário autenticado
    na sessão do Streamlit.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    return salvar_assinatura_por_user_id(
        user_id=user_id,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        stripe_price_id=stripe_price_id,
        subscription_status=subscription_status,
        current_period_start=current_period_start,
        current_period_end=current_period_end,
        cancel_at_period_end=cancel_at_period_end,
    )


def salvar_assinatura_por_user_id(
    user_id: str,
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
    stripe_price_id: str | None = None,
    subscription_status: str = "inactive",
    current_period_start: str | None = None,
    current_period_end: str | None = None,
    cancel_at_period_end: bool = False,
) -> dict[str, Any]:
    """
    Cria ou atualiza uma assinatura usando um user_id
    informado pelo backend.

    Esta função é destinada ao webhook do Stripe.
    Ela utiliza o cliente administrativo do Supabase.
    """

    if not user_id:
        raise RuntimeError(
            "user_id não informado."
        )

    supabase = get_supabase_admin()

    payload = {
        "user_id": user_id,
        "stripe_customer_id": stripe_customer_id,
        "stripe_subscription_id": stripe_subscription_id,
        "stripe_price_id": stripe_price_id,
        "subscription_status": subscription_status,
        "current_period_start": current_period_start,
        "current_period_end": current_period_end,
        "cancel_at_period_end": cancel_at_period_end,
    }

    response = (
        supabase
        .table(TABLE_NAME)
        .upsert(
            payload,
            on_conflict="user_id",
        )
        .execute()
    )

    if response is None:
        raise RuntimeError(
            "Não foi possível salvar a assinatura."
        )

    if not response.data:
        raise RuntimeError(
            "A assinatura não foi salva."
        )

    return response.data[0]


def assinatura_ativa() -> bool:
    """
    Verifica se o usuário possui uma assinatura ativa.

    Status considerados ativos:
        active
        trialing
    """

    assinatura = buscar_assinatura()

    if not assinatura:
        return False

    status = assinatura.get(
        "subscription_status"
    )

    return status in {
        "active",
        "trialing",
    }


def atualizar_assinatura(
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
    stripe_price_id: str | None = None,
    subscription_status: str | None = None,
    current_period_start: str | None = None,
    current_period_end: str | None = None,
    cancel_at_period_end: bool | None = None,
) -> dict[str, Any] | None:
    """
    Atualiza a assinatura do usuário autenticado
    na sessão do Streamlit.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    return atualizar_assinatura_por_user_id(
        user_id=user_id,
        stripe_customer_id=stripe_customer_id,
        stripe_subscription_id=stripe_subscription_id,
        stripe_price_id=stripe_price_id,
        subscription_status=subscription_status,
        current_period_start=current_period_start,
        current_period_end=current_period_end,
        cancel_at_period_end=cancel_at_period_end,
    )


def atualizar_assinatura_por_user_id(
    user_id: str,
    stripe_customer_id: str | None = None,
    stripe_subscription_id: str | None = None,
    stripe_price_id: str | None = None,
    subscription_status: str | None = None,
    current_period_start: str | None = None,
    current_period_end: str | None = None,
    cancel_at_period_end: bool | None = None,
) -> dict[str, Any] | None:
    """
    Atualiza uma assinatura usando user_id informado
    pelo backend.

    Esta função é destinada ao webhook.
    """

    if not user_id:
        raise RuntimeError(
            "user_id não informado."
        )

    payload: dict[str, Any] = {}

    if stripe_customer_id is not None:

        payload[
            "stripe_customer_id"
        ] = stripe_customer_id

    if stripe_subscription_id is not None:

        payload[
            "stripe_subscription_id"
        ] = stripe_subscription_id

    if stripe_price_id is not None:

        payload[
            "stripe_price_id"
        ] = stripe_price_id

    if subscription_status is not None:

        payload[
            "subscription_status"
        ] = subscription_status

    if current_period_start is not None:

        payload[
            "current_period_start"
        ] = current_period_start

    if current_period_end is not None:

        payload[
            "current_period_end"
        ] = current_period_end

    if cancel_at_period_end is not None:

        payload[
            "cancel_at_period_end"
        ] = cancel_at_period_end

    if not payload:

        return buscar_assinatura_por_user_id(
            user_id
        )

    response = (
        get_supabase_admin()
        .table(TABLE_NAME)
        .update(payload)
        .eq(
            "user_id",
            user_id,
        )
        .execute()
    )

    if response is None:

        return None

    if not response.data:

        return None

    return response.data[0]


def buscar_assinatura_por_user_id(
    user_id: str,
) -> dict[str, Any] | None:
    """
    Busca uma assinatura diretamente pelo user_id.

    Uso exclusivo do backend/webhook.
    """

    if not user_id:
        return None

    response = (
        get_supabase_admin()
        .table(TABLE_NAME)
        .select(
            """
            id,
            user_id,
            stripe_customer_id,
            stripe_subscription_id,
            stripe_price_id,
            subscription_status,
            current_period_start,
            current_period_end,
            cancel_at_period_end,
            created_at,
            updated_at
            """
        )
        .eq(
            "user_id",
            user_id,
        )
        .limit(1)
        .execute()
    )

    if response is None:
        return None

    if not response.data:
        return None

    return response.data[0]


def remover_assinatura() -> bool:
    """
    Remove a assinatura do usuário autenticado.
    """

    user_id = _get_user_id()

    if not user_id:
        raise RuntimeError(
            "Usuário autenticado não encontrado."
        )

    response = (
        get_supabase()
        .table(TABLE_NAME)
        .delete()
        .eq(
            "user_id",
            user_id,
        )
        .execute()
    )

    if response is None:
        return False

    return True