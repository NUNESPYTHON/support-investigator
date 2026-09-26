"""
==========================================================
Support Investigator V2

Arquivo:
billing.py

Responsabilidade:
Tela de assinatura e gerenciamento da assinatura
do Support Investigator.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from services.subscription import buscar_assinatura
from services.stripe_service import (
    create_checkout_session,
    create_customer_portal_session,
)


def render():
    """
    Renderiza a página de assinatura.
    """

    st.title("Assinatura")

    st.caption(
        "Gerencie sua assinatura do Support Investigator."
    )

    # ======================================================
    # USUÁRIO
    # ======================================================

    usuario = st.session_state.get("user")

    if usuario is None:

        st.error(
            "Usuário autenticado não encontrado."
        )

        return

    email = getattr(
        usuario,
        "email",
        None,
    )

    user_id = getattr(
        usuario,
        "id",
        None,
    )

    # ======================================================
    # ASSINATURA
    # ======================================================

    try:

        assinatura = buscar_assinatura()

    except Exception as erro:

        st.error(
            f"Não foi possível carregar sua assinatura: {erro}"
        )

        return

    # ======================================================
    # SEM ASSINATURA
    # ======================================================

    if not assinatura:

        st.subheader(
            "Support Investigator Pro"
        )

        st.write(
            "Tenha acesso aos recursos de investigação "
            "do Support Investigator."
        )

        st.markdown(
            """
            **Sua assinatura está inativa.**

            Comece seu período de avaliação gratuita
            para continuar usando a plataforma.
            """
        )

        st.divider()

        col1, col2 = st.columns(
            [2, 1]
        )

        with col1:

            st.markdown(
                "### Plano Professional"
            )

            st.write(
                "Assinatura mensal"
            )

            st.write(
                "7 dias grátis"
            )

        with col2:

            st.markdown(
                "### R$ 49,99 / mês"
            )

        st.write("")

        subscribe = st.button(
            "Começar assinatura",
            type="primary",
            use_container_width=True,
            key="billing_subscribe",
        )

        if subscribe:

            try:

                session = create_checkout_session(
                    customer_email=email,
                    user_id=user_id,
                )

                st.link_button(
                    "Continuar para o Stripe Checkout",
                    session.url,
                    use_container_width=True,
                )

                st.success(
                    "Checkout criado com sucesso."
                )

                st.info(
                    "Clique no botão acima para continuar "
                    "com sua assinatura."
                )

            except Exception as erro:

                st.error(
                    f"Não foi possível criar o checkout: {erro}"
                )

        return

    # ======================================================
    # ASSINATURA EXISTENTE
    # ======================================================

    status = assinatura.get(
        "subscription_status",
        "inactive",
    )

    st.subheader(
        "Sua assinatura"
    )

    # ======================================================
    # STATUS
    # ======================================================

    if status in {
        "active",
        "trialing",
    }:

        if status == "trialing":

            st.success(
                "Período de avaliação ativo"
            )

        else:

            st.success(
                "Assinatura ativa"
            )

    elif status == "past_due":

        st.warning(
            "Identificamos um problema com o pagamento. "
            "Atualize sua forma de pagamento para continuar."
        )

    elif status == "canceled":

        st.error(
            "Sua assinatura foi cancelada."
        )

    else:

        st.warning(
            f"Status da assinatura: {status}"
        )

    # ======================================================
    # DETALHES
    # ======================================================

    stripe_customer_id = assinatura.get(
        "stripe_customer_id"
    )

    stripe_subscription_id = assinatura.get(
        "stripe_subscription_id"
    )

    current_period_end = assinatura.get(
        "current_period_end"
    )

    cancel_at_period_end = assinatura.get(
        "cancel_at_period_end"
    )

    st.write(
        "Cliente Stripe:",
        stripe_customer_id or "Não disponível",
    )

    st.write(
        "Assinatura Stripe:",
        stripe_subscription_id or "Não disponível",
    )

    st.write(
        "Fim do período:",
        current_period_end or "Não disponível",
    )

    # ------------------------------------------------------
    # CANCELAMENTO AGENDADO
    # ------------------------------------------------------

    if cancel_at_period_end:

        st.warning(
            "Sua assinatura está programada para ser "
            "encerrada ao final do período atual."
        )

    st.divider()

    # ======================================================
    # CUSTOMER PORTAL
    # ======================================================

    st.subheader(
        "Gerenciar assinatura"
    )

    st.write(
        "Atualize sua forma de pagamento ou gerencie "
        "sua assinatura com segurança pelo Stripe."
    )

    if not stripe_customer_id:

        st.warning(
            "O ID do cliente Stripe ainda não está disponível."
        )

        return

    manage_subscription = st.button(
        "Gerenciar assinatura",
        type="primary",
        use_container_width=True,
        key="billing_manage_subscription",
    )

    if manage_subscription:

        try:

            portal_session = create_customer_portal_session(
                stripe_customer_id=stripe_customer_id,
            )

            st.link_button(
                "Abrir portal da Stripe",
                portal_session.url,
                use_container_width=True,
            )

            st.success(
                "Portal de assinatura criado com sucesso."
            )

            st.info(
                "Use o portal para atualizar seu cartão "
                "ou gerenciar sua assinatura."
            )

        except Exception as erro:

            st.error(
                f"Não foi possível abrir o portal da Stripe: {erro}"
            )