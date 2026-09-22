"""
==========================================================
Support Investigator V2

Arquivo:
billing.py

Responsabilidade:
Tela de Billing e assinatura do Support Investigator.

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
    Renderiza a página de Billing.
    """

    st.title("Billing")

    st.caption(
        "Manage your Support Investigator subscription."
    )

    # ======================================================
    # USUÁRIO
    # ======================================================

    usuario = st.session_state.get("user")

    if usuario is None:

        st.error(
            "Authenticated user not found."
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
            f"Unable to load subscription: {erro}"
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
            "Get access to the Support Investigator features."
        )

        st.markdown(
            """
            **Your subscription is currently inactive.**

            Subscribe to continue using the platform.
            """
        )

        st.divider()

        col1, col2 = st.columns(
            [2, 1]
        )

        with col1:

            st.markdown(
                "### Professional Plan"
            )

            st.write(
                "Monthly subscription"
            )

            st.write(
                "7-day free trial"
            )

        with col2:

            st.markdown(
                "### R$ 49.99 / month"
            )

        st.write("")

        subscribe = st.button(
            "Subscribe",
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
                    "Continue to Stripe Checkout",
                    session.url,
                    use_container_width=True,
                )

                st.success(
                    "Checkout created successfully."
                )

                st.info(
                    "Click the button above to continue to Stripe Checkout."
                )

            except Exception as erro:

                st.error(
                    f"Unable to create checkout session: {erro}"
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
        "Current subscription"
    )

    # ======================================================
    # STATUS
    # ======================================================

    if status in {
        "active",
        "trialing",
    }:

        st.success(
            f"Subscription status: {status}"
        )

    elif status == "past_due":

        st.warning(
            "Your subscription has a payment issue. "
            "Please update your payment method."
        )

    elif status == "canceled":

        st.error(
            "Your subscription has been canceled."
        )

    else:

        st.warning(
            f"Subscription status: {status}"
        )

    # ======================================================
    # DETALHES
    # ======================================================

    st.write(
        "Stripe Customer ID:",
        assinatura.get(
            "stripe_customer_id"
        ),
    )

    st.write(
        "Stripe Subscription ID:",
        assinatura.get(
            "stripe_subscription_id"
        ),
    )

    st.write(
        "Current period end:",
        assinatura.get(
            "current_period_end"
        ),
    )

    st.write(
        "Cancel at period end:",
        assinatura.get(
            "cancel_at_period_end"
        ),
    )

    st.divider()

    # ======================================================
    # CUSTOMER PORTAL
    # ======================================================

    st.subheader(
        "Manage your subscription"
    )

    st.write(
        "Update your payment method or manage your subscription "
        "through Stripe."
    )

    stripe_customer_id = assinatura.get(
        "stripe_customer_id"
    )

    if not stripe_customer_id:

        st.warning(
            "Stripe Customer ID is not available yet."
        )

        return

    manage_subscription = st.button(
        "Manage Subscription",
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
                "Open Stripe Customer Portal",
                portal_session.url,
                use_container_width=True,
            )

            st.success(
                "Customer Portal created successfully."
            )

            st.info(
                "Click the button above to manage your subscription."
            )

        except Exception as erro:

            st.error(
                f"Unable to open Customer Portal: {erro}"
            )