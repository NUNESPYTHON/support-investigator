import streamlit as st

from ui.navigation import inicializar_estado

from ui.ticket_details import (
    render as render_ticket_details,
)

from ui.zendesk_connection import (
    render as render_zendesk_connection,
)

from ui.customer_history import (
    render_resumo,
    render_ticket_card,
)

from ui.export import (
    render as render_export,
    processar_exportacao,
    render_resultado,
)

from services.customer_diagnostics import (
    diagnosticar_cliente,
)

from services.export import STATUS_MAP

from services.oauth import (
    gerar_url_autorizacao,
    trocar_codigo_por_token,
    salvar_contexto_oauth,
    obter_contexto_oauth,
    remover_contexto_oauth,
    normalizar_subdomain,
)


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Support Investigator",
    page_icon="▪",
    layout="wide",
)


# ==========================================================
# INICIALIZAÇÃO DO ESTADO
# ==========================================================

inicializar_estado(st)


# ==========================================================
# CALLBACK OAUTH
# ==========================================================

query_params = st.query_params

authorization_code = query_params.get("code")
returned_state = query_params.get("state")
oauth_error = query_params.get("error")
oauth_error_description = query_params.get("error_description")


# ----------------------------------------------------------
# ERRO DEVOLVIDO PELO ZENDESK
# ----------------------------------------------------------

if oauth_error:

    mensagem = oauth_error

    if oauth_error_description:
        mensagem += f": {oauth_error_description}"

    st.error(
        f"Falha na autorização do Zendesk: {mensagem}"
    )

    st.query_params.clear()


# ----------------------------------------------------------
# CALLBACK COM AUTHORIZATION CODE
# ----------------------------------------------------------

elif authorization_code:

    # ------------------------------------------------------
    # VALIDAR STATE
    # ------------------------------------------------------

    if not returned_state:

        st.error(
            "O callback OAuth não retornou o parâmetro state."
        )

        st.query_params.clear()

    else:

        # --------------------------------------------------
        # RECUPERAR CONTEXTO DO OAUTH
        # --------------------------------------------------

        oauth_context = obter_contexto_oauth(
            returned_state
        )

        if not oauth_context:

            st.error(
                "A sessão OAuth expirou ou não foi encontrada. "
                "Inicie a conexão novamente."
            )

            st.query_params.clear()

        else:

            expected_state = oauth_context.get(
                "state"
            )

            # ----------------------------------------------
            # VALIDAR STATE
            # ----------------------------------------------

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

                # ------------------------------------------
                # RECUPERAR DADOS DA CONEXÃO
                # ------------------------------------------

                subdomain = oauth_context.get(
                    "subdomain"
                )

                client_kind = oauth_context.get(
                    "client_kind"
                )

                client_id = oauth_context.get(
                    "client_id"
                )

                client_secret = oauth_context.get(
                    "client_secret"
                )

                code_verifier = oauth_context.get(
                    "code_verifier"
                )

                try:

                    # --------------------------------------
                    # TROCAR CODE POR TOKEN
                    # --------------------------------------

                    token_data = trocar_codigo_por_token(

    subdomain=subdomain,

    code=authorization_code,

    client_kind=client_kind,

    client_id=client_id,

    client_secret=client_secret,

    code_verifier=code_verifier,

)

                    # --------------------------------------
                    # SALVAR CONEXÃO
                    # --------------------------------------

                    st.session_state[
                        "zendesk_connected"
                    ] = True

                    st.session_state[
                        "zendesk_access_token"
                    ] = token_data.get(
                        "access_token"
                    )

                    st.session_state[
                        "zendesk_refresh_token"
                    ] = token_data.get(
                        "refresh_token"
                    )

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

                    # --------------------------------------
                    # REMOVER CONTEXTO TEMPORÁRIO
                    # --------------------------------------

                    remover_contexto_oauth(
                        returned_state
                    )

                    # --------------------------------------
                    # LIMPAR URL DO CALLBACK
                    # --------------------------------------

                    st.query_params.clear()

                    st.success(
                        "✅ Zendesk conectado com sucesso!"
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

STATUS_CONFIG = {
    "new": {
        "label": "Novo",
        "background": "#F59E0B",
        "text": "#FFFFFF",
    },
    "open": {
        "label": "Aberto",
        "background": "#DC2626",
        "text": "#FFFFFF",
    },
    "pending": {
        "label": "Pendente",
        "background": "#2563EB",
        "text": "#FFFFFF",
    },
    "hold": {
        "label": "Em espera",
        "background": "#111827",
        "text": "#FFFFFF",
    },
    "solved": {
        "label": "Resolvido",
        "background": "#4B5563",
        "text": "#FFFFFF",
    },
    "closed": {
        "label": "Fechado",
        "background": "#FFFFFF",
        "text": "#1F2937",
    },
}


# ==========================================================
# ESTILO VISUAL
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

        .app-title {
            color: #172554;
            font-size: 2.5rem;
            font-weight: 750;
            letter-spacing: -0.03em;
            margin-bottom: 0.25rem;
        }

        .app-subtitle {
            color: #64748B;
            font-size: 1rem;
            margin-bottom: 2rem;
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
            background-color: rgba(255, 255, 255, 0.96);
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

        .result-box {
            background-color: #FFFFFF;
            border: 1px solid #D9E2EC;
            border-radius: 14px;
            padding: 1.5rem;
            margin-top: 1.5rem;
        }

        .result-title {
            color: #172554;
            font-size: 1.35rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }

        .result-label {
            color: #64748B;
            font-size: 0.82rem;
            margin-bottom: 0.2rem;
        }

        .result-value {
            color: #1E293B;
            font-size: 1rem;
            font-weight: 600;
        }

        .status-badge {
            display: inline-block;
            padding: 0.35rem 0.75rem;
            border-radius: 8px;
            font-size: 0.9rem;
            font-weight: 700;
            margin-top: 0.15rem;
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
# CABEÇALHO
# ==========================================================

st.markdown(
    '<div class="app-title">Support Investigator</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="app-subtitle">'
    'Consulte informações de suporte de forma rápida e objetiva.'
    '</div>',
    unsafe_allow_html=True,
)
# ==========================================================
# CONEXÃO COM ZENDESK
# ==========================================================

# ==========================================================
# STATUS DA CONEXÃO
# ==========================================================

if st.session_state.get("zendesk_connected"):

    connected_subdomain = st.session_state.get(
        "oauth_ctx_subdomain"
    )

    st.success(
        f"🟢 Conectado ao Zendesk: "
        f"{connected_subdomain}.zendesk.com"
    )

    if st.button(
        "Desconectar",
        key="btn_desconectar_zendesk",
        use_container_width=True,
    ):

        for chave in [
            "zendesk_connected",
            "zendesk_access_token",
            "zendesk_refresh_token",
            "zendesk_token_data",
            "oauth_state",
            "oauth_code_verifier",
            "oauth_ctx_subdomain",
            "oauth_ctx_client_kind",
            "oauth_ctx_client_id",
            "oauth_ctx_client_secret",
        ]:
            st.session_state.pop(
                chave,
                None,
            )

        st.rerun()
       




# ==========================================================
# CONEXÃO COM ZENDESK
# ==========================================================

oauth_form = render_zendesk_connection()



# ==========================================================
# INICIAR CONEXÃO OAUTH
# ==========================================================

if oauth_form["conectar"]:

    if not oauth_form["subdomain"].strip():

        st.warning(
            "Informe o subdomínio do Zendesk."
        )

    elif not oauth_form["client_id"].strip():

        st.warning(
            "Informe o Client ID."
        )

    elif (
        oauth_form["client_kind"] == "confidential"
        and not oauth_form["client_secret"]
    ):

        st.warning(
            "Informe o Client Secret."
        )

    else:

        try:

            # --------------------------------------------------
            # GERAR URL DE AUTORIZAÇÃO
            # --------------------------------------------------

            oauth_data = gerar_url_autorizacao(
                subdomain=oauth_form["subdomain"],
                state=None,
                client_kind=oauth_form["client_kind"],
                client_id=oauth_form["client_id"],
            )

            # --------------------------------------------------
            # SALVAR CONTEXTO TEMPORÁRIO DO OAUTH
            # --------------------------------------------------

            salvar_contexto_oauth(
    oauth_data["state"],
    {
        "state": oauth_data["state"],
        "subdomain": normalizar_subdomain(
            oauth_form["subdomain"]
        ),
        "client_kind": oauth_form["client_kind"],
        "client_id": oauth_form["client_id"],
        "client_secret": oauth_form["client_secret"],
        "code_verifier": oauth_data["code_verifier"],
    },
)

            # --------------------------------------------------
            # BOTÃO DE AUTORIZAÇÃO
            # --------------------------------------------------

            st.info(
                "A configuração foi preparada. "
                "Clique abaixo para entrar no Zendesk "
                "e autorizar o Support Investigator."
            )

            st.link_button(
                "Autorizar no Zendesk",
                oauth_data["url"],
                use_container_width=True,
            )

        except Exception as erro:

            st.error(
                f"Não foi possível iniciar o OAuth: {erro}"
            )
 

col1, col2, col3 = st.columns(3)


# ==========================================================
# DIAGNÓSTICO DO TICKET
# ==========================================================

with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="card-title">Detalhes do Ticket</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">'
            'Consulte rapidamente o status, responsável, '
            'primeira resposta, última interação e resumo '
            'de um ticket.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        ticket_id = st.text_input(
            "Número do Ticket",
            key="ticket_id",
            placeholder="Ex.: 1114",
        )

        diagnosticar = st.button(
            "Consultar",
            use_container_width=True,
            key="btn_diagnosticar",
        )


# ==========================================================
# HISTÓRICO DE INTERAÇÕES
# ==========================================================

with col2:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            'Histórico de Interações'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">'
            'Consulte o histórico de tickets associados '
            'a um cliente e visualize sua situação atual.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        email_cliente = st.text_input(
            "E-mail do Cliente",
            key="email_cliente",
            placeholder="Ex.: cliente@empresa.com",
        )

        consultar = st.button(
            "Consultar",
            use_container_width=True,
            key="btn_consultar",
        )


# ==========================================================
# EXPORTAÇÃO
# ==========================================================

with col3:

    with st.container(border=True):

        (
            email_exportacao,
            status_exportacao,
            formato_exportacao,
            gerar_exportacao,
        ) = render_export()


# ==========================================================
# DETALHES DO TICKET
# ==========================================================

if diagnosticar:

    if not ticket_id:

        st.warning(
            "Informe o número do ticket."
        )

    elif not ticket_id.isdigit():

        st.warning(
            "Informe um número de ticket válido."
        )

    else:

        render_ticket_details(
            ticket_id
        )


# ==========================================================
# CONSULTA DO HISTÓRICO DO CLIENTE
# ==========================================================

if consultar:

    if not email_cliente:

        st.warning(
            "Informe o e-mail do cliente."
        )

        st.session_state[
            "historico_cliente"
        ] = None

        st.session_state[
            "ticket_selecionado"
        ] = None

    else:

        diagnostico_cliente = diagnosticar_cliente(
            email_cliente.strip()
        )

        if diagnostico_cliente is None:

            st.error(
                "Nenhum histórico encontrado para este cliente."
            )

            st.session_state[
                "historico_cliente"
            ] = None

            st.session_state[
                "ticket_selecionado"
            ] = None

        else:

            st.session_state[
                "historico_cliente"
            ] = diagnostico_cliente

            st.session_state[
                "ticket_selecionado"
            ] = None


# ==========================================================
# EXIBIÇÃO DO HISTÓRICO
# ==========================================================

diagnostico_cliente = st.session_state.get(
    "historico_cliente"
)

if diagnostico_cliente:

    st.markdown(
        "## Histórico de Interações"
    )

    render_resumo(
        diagnostico_cliente
    )

    st.divider()

    st.markdown(
        "### Últimos tickets"
    )

    for ticket in diagnostico_cliente[
        "ultimos_tickets"
    ]:

        render_ticket_card(
            ticket
        )

    st.divider()

    st.markdown(
        "### Resumo"
    )

    st.info(
        diagnostico_cliente[
            "resumo"
        ]
    )


# ==========================================================
# DETALHES DO TICKET SELECIONADO
# ==========================================================

ticket_selecionado = st.session_state.get(
    "ticket_selecionado"
)

if ticket_selecionado:

    render_ticket_details(
        ticket_selecionado
    )


# ==========================================================
# PROCESSAMENTO DA EXPORTAÇÃO
# ==========================================================

if gerar_exportacao:

    processar_exportacao(
        email_exportacao,
        status_exportacao,
        formato_exportacao,
    )


# ==========================================================
# RESULTADO DA EXPORTAÇÃO
# ==========================================================

render_resultado()


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown(
    
    '<div class="footer">'
    'Support Investigator'
    '</div>',
    unsafe_allow_html=True,
)