import streamlit as st

from services.customer_diagnostics import diagnosticar_cliente
from services.diagnostics import diagnosticar_ticket
from services.email import enviar_arquivo_email
from services.export import (
    STATUS_MAP,
    filtrar_tickets_por_status,
    gerar_csv_bytes,
    gerar_excel_bytes,
)
from services.tickets import buscar_tickets_por_email


# ==========================================================
# CONFIGURAÇÃO DA PÁGINA
# ==========================================================

st.set_page_config(
    page_title="Support Investigator",
    page_icon="▪",
    layout="wide",
)


# ==========================================================
# CORES DOS STATUS
# ==========================================================

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
# COLUNAS
# ==========================================================

col1, col2, col3 = st.columns(3)


# ==========================================================
# DIAGNÓSTICO DO TICKET
# ==========================================================

with col1:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            'Diagnóstico do Ticket'
            '</div>',
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
            "Diagnosticar",
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
# RESULTADO DO HISTÓRICO DO CLIENTE
# ==========================================================

if consultar:

    if not email_cliente:

        st.warning(
            "Informe o e-mail do cliente."
        )

    else:

        diagnostico_cliente = diagnosticar_cliente(
            email_cliente.strip()
        )

        if diagnostico_cliente is None:

            st.error(
                "Nenhum histórico encontrado para este cliente."
            )

        else:

            st.markdown(
                "## Histórico de Interações"
            )

            resultado_col1, resultado_col2 = st.columns(2)

            with resultado_col1:

                st.caption("E-mail")

                st.write(
                    f"**{diagnostico_cliente['email']}**"
                )

                st.caption("Total de tickets")

                st.write(
                    f"**{diagnostico_cliente['total_tickets']}**"
                )

                st.caption("Abertos")

                st.write(
                    f"**{diagnostico_cliente['abertos']}**"
                )

            with resultado_col2:

                st.caption("Pendentes")

                st.write(
                    f"**{diagnostico_cliente['pendentes']}**"
                )

                st.caption("Resolvidos")

                st.write(
                    f"**{diagnostico_cliente['resolvidos']}**"
                )

                st.caption("Fechados")

                st.write(
                    f"**{diagnostico_cliente['fechados']}**"
                )

            st.divider()

            st.markdown("### Últimos tickets")

            for ticket in diagnostico_cliente[
                "ultimos_tickets"
            ]:

                st.write(
                    f"**#{ticket.get('id')}** | "
                    f"{ticket.get('status')} | "
                    f"{ticket.get('subject') or 'Sem assunto'}"
                )

            st.divider()

            st.markdown("### Resumo")

            st.info(
                diagnostico_cliente["resumo"]
            )


# ==========================================================
# EXPORTAÇÃO
# ==========================================================

with col3:

    with st.container(border=True):

        st.markdown(
            '<div class="section-title">'
            'Exportação'
            '</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            '<div class="section-description">'
            'Exporte os tickets em CSV ou Excel.'
            '</div>',
            unsafe_allow_html=True,
        )

        st.write("")

        email_exportacao = st.text_input(
            "E-mail do Cliente",
            key="email_exportacao",
            placeholder="cliente@empresa.com",
        )

        status_exportacao = st.selectbox(
            "Status",
            list(STATUS_MAP.keys()),
            key="status_exportacao",
        )

        formato_exportacao = st.selectbox(
            "Formato",
            [
                "CSV",
                "Excel",
            ],
            key="formato_exportacao",
        )

        gerar_exportacao = st.button(
            "Gerar arquivo",
            use_container_width=True,
            key="btn_exportar",
        )


# ==========================================================
# PROCESSAMENTO DA EXPORTAÇÃO
# ==========================================================

if gerar_exportacao:

    if not email_exportacao:

        st.warning(
            "Informe o e-mail do cliente."
        )

    else:

        tickets_exportacao = (
            buscar_tickets_por_email(
                email_exportacao.strip()
            )
        )

        if not tickets_exportacao:

            st.warning(
                "Nenhum ticket encontrado para este cliente."
            )

        else:

            status_api = STATUS_MAP[
                status_exportacao
            ]

            tickets_filtrados = (
                filtrar_tickets_por_status(
                    tickets_exportacao,
                    status_api,
                )
            )

            if not tickets_filtrados:

                st.warning(
                    "Nenhum ticket encontrado "
                    f"com o status '{status_exportacao}'."
                )

            else:

                quantidade = len(
                    tickets_filtrados
                )

                st.success(
                    f"{quantidade} ticket(s) "
                    "pronto(s) para exportação."
                )

                if formato_exportacao == "CSV":

                    arquivo_bytes = (
                        gerar_csv_bytes(
                            tickets_filtrados
                        )
                    )

                    nome_arquivo = (
                        "tickets_exportados.csv"
                    )

                    mime_type = "text/csv"

                else:

                    arquivo_bytes = (
                        gerar_excel_bytes(
                            tickets_filtrados
                        )
                    )

                    nome_arquivo = (
                        "tickets_exportados.xlsx"
                    )

                    mime_type = (
                        "application/vnd.openxmlformats-officedocument."
                        "spreadsheetml.sheet"
                    )

                # --------------------------------------------------
                # DOWNLOAD
                # --------------------------------------------------

                st.download_button(
                    label=f"Baixar {formato_exportacao}",
                    data=arquivo_bytes,
                    file_name=nome_arquivo,
                    mime=mime_type,
                    use_container_width=True,
                    key="download_exportacao",
                )

                st.divider()

               

                # --------------------------------------------------
                # ENVIO POR E-MAIL
                # --------------------------------------------------

                st.markdown(
                    "### Enviar por e-mail (opcional)"
                )

                destinatario = st.text_input(
                    "Destinatário",
                    key="email_destinatario",
                    placeholder="gerente@empresa.com",
                )

                enviar_email = st.button(
                    "Enviar arquivo",
                    use_container_width=True,
                    key="btn_enviar_email",
                )
    if enviar_email:

     if not destinatario:

        st.warning(
            "Informe o e-mail do destinatário."
        )

    else:

        from tempfile import NamedTemporaryFile
        from pathlib import Path

        arquivo_temporario = None

        try:

            with NamedTemporaryFile(
                suffix=(
                    ".csv"
                    if formato_exportacao == "CSV"
                    else ".xlsx"
                ),
                delete=False,
            ) as arquivo_temp:

                arquivo_temp.write(
                    arquivo_bytes
                )

                arquivo_temporario = (
                    arquivo_temp.name
                )

            resultado = enviar_arquivo_email(
                arquivo_temporario,
                destinatario.strip(),
                "Support Investigator - Exportação",
                (
                    "Olá,\n\n"
                    "Segue em anexo o arquivo "
                    "gerado pelo Support Investigator.\n\n"
                    "Atenciosamente,\n"
                    "Support Investigator"
                ),
            )

            if resultado:

                st.success(
                    "Arquivo enviado com sucesso."
                )

            else:

                st.error(
                    "Não foi possível enviar o arquivo."
                )

        except Exception as erro:

            st.error(
                f"Erro ao enviar o arquivo: {erro}"
            )

        finally:

            if arquivo_temporario:

                caminho_temporario = Path(
                    arquivo_temporario
                )

                if caminho_temporario.exists():

                    caminho_temporario.unlink()

            
# ==========================================================
# RESULTADO DO DIAGNÓSTICO
# ==========================================================

# ==========================================================
# RESULTADO DO DIAGNÓSTICO
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

        diagnostico = diagnosticar_ticket(
            int(ticket_id)
        )

        if diagnostico is None:

            st.error(
                "Ticket não encontrado."
            )

        else:

            with st.container(border=True):

                st.subheader(
                    "Resumo Executivo"
                )

                resultado_col1, resultado_col2 = st.columns(2)

                # --------------------------------------------------
                # COLUNA 1
                # --------------------------------------------------

                with resultado_col1:

                    st.caption("Ticket")

                    st.write(
                        f"**{diagnostico['ticket_id']}**"
                    )

                    st.caption("Status")

                    status = diagnostico["status"]

                    status_config = STATUS_CONFIG.get(
                        status,
                        {
                            "label": status,
                            "background": "#64748B",
                            "text": "#FFFFFF",
                        },
                    )

                    status_style = (
                        f"background-color: "
                        f"{status_config['background']}; "
                        f"color: "
                        f"{status_config['text']};"
                    )

                    if status == "closed":

                        status_style += (
                            "border: 1px solid #CBD5E1;"
                        )

                    st.markdown(
                        f'<span class="status-badge" '
                        f'style="{status_style}">'
                        f'{status_config["label"]}'
                        f'</span>',
                        unsafe_allow_html=True,
                    )

                    st.write("")

                    st.caption("Solicitante")

                    st.write(
                        f"**{diagnostico['solicitante']}**"
                    )

                    st.caption("Responsável")

                    st.write(
                        f"**{diagnostico['responsavel']}**"
                    )

                # --------------------------------------------------
                # COLUNA 2
                # --------------------------------------------------

                with resultado_col2:

                    st.caption("Assunto")

                    st.write(
                        f"**{diagnostico['assunto']}**"
                    )

                    st.caption("Primeira resposta")

                    st.write(
                        f"**{diagnostico['primeira_resposta']}**"
                    )

                st.divider()

                # --------------------------------------------------
                # RESUMO
                # --------------------------------------------------

                st.markdown("### Resumo")

                st.info(
                    diagnostico["resumo"]
                )

                # --------------------------------------------------
                # ÚLTIMA INTERAÇÃO
                # --------------------------------------------------

                ultima = diagnostico.get(
                    "ultima_interacao"
                )

                st.markdown("### Última interação")

                if ultima:

                    st.write(
                        f"**Autor:** {ultima['autor']}"
                    )

                    st.write(
                        f"**Data:** {ultima['data']}"
                    )

                    st.write(
                        ultima["texto"]
                    )

                else:

                    st.info(
                        "Nenhuma interação encontrada."
                    )


# ==========================================================
# RODAPÉ
# ==========================================================

st.markdown(
    '<div class="footer">'
    'Support Investigator'
    '</div>',
    unsafe_allow_html=True,
)