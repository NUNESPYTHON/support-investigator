"""
==========================================================
Support Investigator V2

Arquivo:
streamlit_app.py

Responsabilidade:
Aplicação principal, autenticação, callback OAuth,
controle de acesso por assinatura e navegação.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.navigation import inicializar_estado

from services.session import inicializar_sessao

from services.subscription import assinatura_ativa

from ui.auth_gate import render_auth_gate

from ui.dashboard_sidebar import (
    render as render_dashboard_sidebar,
)

from ui.pages.dashboard import (
    render as render_dashboard,
)

from ui.pages.zendesk import (
    render as render_zendesk,
)

from ui.pages.investigator import (
    render as render_investigator,
)

from ui.pages.export_page import (
    render as render_export_page,
)

from ui.pages.billing import (
    render as render_billing,
)

from ui.pages.settings import (
    render as render_settings,
)

from services.oauth import (
    trocar_codigo_por_token,
    obter_contexto_oauth,
    remover_contexto_oauth,
)

from services.zendesk_connection import (
    salvar_conexao,
    restaurar_conexao_na_sessao,
)


# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="Support Investigator",
    page_icon="▪",
    layout="wide",
)


# ==========================================================
# ESTADO
# ==========================================================

inicializar_estado(st)

inicializar_sessao()


# ==========================================================
# AUTENTICAÇÃO
# ==========================================================

if not render_auth_gate():

    st.stop()


# ==========================================================
# RESTAURAR CONEXÃO ZENDESK
# ==========================================================

if not st.session_state.get(
    "zendesk_connection_loaded",
    False,
):

    try:

        st.write(
            "DEBUG: iniciando restauração da conexão Zendesk..."
        )

        resultado_restauracao = (
            restaurar_conexao_na_sessao()
        )

        st.write(
            "DEBUG: restauração da conexão Zendesk concluída:",
            resultado_restauracao,
        )

    except Exception as erro:

        st.error(
            f"Erro ao restaurar conexão Zendesk: {erro}"
        )

    finally:

        st.session_state[
            "zendesk_connection_loaded"
        ] = True


# ==========================================================
# CALLBACK OAUTH
# ==========================================================

query_params = st.query_params

authorization_code = query_params.get(
    "code"
)

returned_state = query_params.get(
    "state"
)

oauth_error = query_params.get(
    "error"
)

oauth_error_description = query_params.get(
    "error_description"
)


# ==========================================================
# ERRO OAUTH
# ==========================================================

if oauth_error:

    mensagem = oauth_error

    if oauth_error_description:

        mensagem += (
            f": {oauth_error_description}"
        )

    st.error(
        "Falha na autorização do Zendesk: "
        f"{mensagem}"
    )

    st.query_params.clear()


# ==========================================================
# PROCESSAR CALLBACK
# ==========================================================

elif authorization_code:

    if not returned_state:

        st.error(
            "O callback OAuth não retornou "
            "o parâmetro state."
        )

        st.query_params.clear()

    else:

        oauth_context = obter_contexto_oauth(
            returned_state
        )

        if not oauth_context:

            st.error(
                "A sessão OAuth expirou ou "
                "não foi encontrada. "
                "Inicie a conexão novamente."
            )

            st.query_params.clear()

        else:

            expected_state = oauth_context.get(
                "state"
            )

            if returned_state != expected_state:

                st.error(
                    "Falha de segurança: "
                    "o parâmetro state não corresponde "
                    "ao estado esperado."
                )

                remover_contexto_oauth(
                    returned_state
                )

                st.query_params.clear()

            else:

                subdomain = (
                    oauth_context.get(
                        "subdomain"
                    )
                )

                client_kind = (
                    oauth_context.get(
                        "client_kind"
                    )
                )

                client_id = (
                    oauth_context.get(
                        "client_id"
                    )
                )

                client_secret = (
                    oauth_context.get(
                        "client_secret"
                    )
                )

                code_verifier = (
                    oauth_context.get(
                        "code_verifier"
                    )
                )

                try:

                    token_data = (
                        trocar_codigo_por_token(
                            subdomain=subdomain,
                            code=authorization_code,
                            client_kind=client_kind,
                            client_id=client_id,
                            client_secret=client_secret,
                            code_verifier=code_verifier,
                        )
                    )

                    access_token = (
                        token_data.get(
                            "access_token"
                        )
                    )

                    refresh_token = (
                        token_data.get(
                            "refresh_token"
                        )
                    )

                    # ======================================
                    # SALVAR NO BANCO
                    # ======================================

                    salvar_conexao(
                        subdomain=subdomain,
                        client_kind=client_kind,
                        client_id=client_id,
                        client_secret=client_secret,
                        access_token=access_token,
                        refresh_token=refresh_token,
                        token_data=token_data,
                    )

                    # ======================================
                    # SALVAR NA SESSÃO
                    # ======================================

                    st.session_state[
                        "zendesk_connected"
                    ] = bool(
                        access_token
                    )

                    st.session_state[
                        "zendesk_access_token"
                    ] = access_token

                    st.session_state[
                        "zendesk_refresh_token"
                    ] = refresh_token

                    st.session_state[
                        "zendesk_token_data"
                    ] = token_data

                    st.session_state[
                        "oauth_ctx_subdomain"
                    ] = subdomain

                    st.session_state[
                        "oauth_ctx_client_kind"
                    ] = client_kind

                    st.session_state[
                        "oauth_ctx_client_id"
                    ] = client_id

                    st.session_state[
                        "oauth_ctx_client_secret"
                    ] = client_secret

                    st.session_state[
                        "zendesk_connection_loaded"
                    ] = True

                    # ======================================
                    # REMOVER CONTEXTO TEMPORÁRIO
                    # ======================================

                    remover_contexto_oauth(
                        returned_state
                    )

                    # ======================================
                    # LIMPAR CALLBACK
                    # ======================================

                    st.query_params.clear()

                    st.success(
                        "Zendesk conectado com sucesso!"
                    )

                    st.rerun()

                except Exception as erro:

                    remover_contexto_oauth(
                        returned_state
                    )

                    st.error(
                        "Não foi possível concluir "
                        f"a conexão OAuth: {erro}"
                    )

                    st.query_params.clear()


# ==========================================================
# ESTILO
# ==========================================================

st.markdown(
    """
    <style>

        .stApp {
            background: linear-gradient(
                180deg,
                #EEF4FA 0%,
                #F7F9FC 45%,
                #FFFFFF 100%
            );
        }

        .block-container {
            max-width: 1200px;
            padding-top: 3rem;
            padding-bottom: 3rem;
        }

        .card-title {
            color: #172554;
            font-size: 1.15rem;
            font-weight: 700;
            line-height: 1.3;
            margin-bottom: 0.5rem;
        }

        .section-title {
            color: #172554;
            font-size: 1.15rem;
            font-weight: 700;
        }

        .section-description {
            color: #64748B;
            font-size: 0.92rem;
            line-height: 1.5;
        }

        div[data-testid="stVerticalBlockBorderWrapper"] {
            background-color: rgba(
                255,
                255,
                255,
                0.96
            );

            border: 1px solid #D9E2EC;

            border-radius: 14px;

            padding: 1.2rem;
        }

        div.stButton > button {
            width: 100%;
            min-height: 44px;
            border-radius: 9px;
            border: 1px solid #2563EB;
            background-color: #2563EB;
            color: #FFFFFF;
            font-weight: 650;
        }

        div.stButton > button:hover {
            border-color: #1D4ED8;
            background-color: #1D4ED8;
            color: #FFFFFF;
        }

        div[data-testid="stTextInput"] input {
            border-radius: 9px;
            border: 1px solid #CBD5E1;
        }

        div[data-testid="stSelectbox"] div {
            border-radius: 9px;
        }

        .footer {
            text-align: center;
            color: #94A3B8;
            font-size: 0.8rem;
            margin-top: 3rem;
        }

    </style>
    """,
    unsafe_allow_html=True,
)


# ==========================================================
# SIDEBAR
# ==========================================================

secao_atual = render_dashboard_sidebar()


# ==========================================================
# CONTROLE DE ACESSO POR ASSINATURA
# ==========================================================

try:

    possui_assinatura = assinatura_ativa()

except Exception as erro:

    st.error(
        "Unable to verify subscription."
    )

    st.caption(
        f"Subscription verification error: {erro}"
    )

    st.stop()


# ==========================================================
# SEM ASSINATURA
# ==========================================================

if not possui_assinatura:

    # ------------------------------------------------------
    # Billing e Settings continuam acessíveis.
    # Todas as outras áreas ficam bloqueadas.
    # ------------------------------------------------------

    if secao_atual not in {
        "Billing",
        "Settings",
    }:

        st.warning(
            "An active subscription is required "
            "to use Support Investigator."
        )

        st.info(
            "Go to Billing to start your subscription "
            "or free trial."
        )

        render_billing()

        st.stop()


# ==========================================================
# NAVEGAÇÃO
# ==========================================================

if secao_atual == "Dashboard":

    render_dashboard()

elif secao_atual == "Zendesk":

    render_zendesk()

elif secao_atual == "Investigator":

    render_investigator()

elif secao_atual == "Export":

    render_export_page()

elif secao_atual == "Billing":

    render_billing()

elif secao_atual == "Settings":

    render_settings()


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown(
    '<div class="footer">'
    'Support Investigator'
    '</div>',
    unsafe_allow_html=True,
)