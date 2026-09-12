"""
==========================================================
Support Investigator

Arquivo:
export.py

Responsabilidade:
Renderizar a interface de exportação e envio por e-mail.

Autor:
Elias Nunes
==========================================================
"""

from pathlib import Path
from tempfile import NamedTemporaryFile

import streamlit as st

from services.email import enviar_arquivo_email
from services.export import (
    STATUS_MAP,
    filtrar_tickets_por_status,
    gerar_csv_bytes,
    gerar_excel_bytes,
)
from services.tickets import buscar_tickets_por_email


def render():

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

    email = st.text_input(
        "E-mail do Cliente",
        key="email_exportacao",
        placeholder="cliente@empresa.com",
    )

    status = st.selectbox(
        "Status",
        list(STATUS_MAP.keys()),
        key="status_exportacao",
    )

    formato = st.selectbox(
        "Formato",
        [
            "CSV",
            "Excel",
        ],
        key="formato_exportacao",
    )

    gerar = st.button(
        "Gerar arquivo",
        use_container_width=True,
        key="btn_exportar",
    )

    return (
        email,
        status,
        formato,
        gerar,
    )


def processar_exportacao(
    email_exportacao,
    status_exportacao,
    formato_exportacao,
):
    """
    Busca os tickets e gera o arquivo de exportação.
    """

    if not email_exportacao.strip():

        st.warning(
            "Informe o e-mail do cliente."
        )

        return

    tickets_exportacao = (
        buscar_tickets_por_email(
            email_exportacao.strip()
        )
    )

    if not tickets_exportacao:

        st.warning(
            "Nenhum ticket encontrado para este cliente."
        )

        return

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

        return

    quantidade = len(
        tickets_filtrados
    )

    st.success(
        f"{quantidade} ticket(s) "
        "pronto(s) para exportação."
    )

    if formato_exportacao == "CSV":

        arquivo_bytes = gerar_csv_bytes(
            tickets_filtrados
        )

        nome_arquivo = (
            "tickets_exportados.csv"
        )

        mime_type = "text/csv"

    else:

        arquivo_bytes = gerar_excel_bytes(
            tickets_filtrados
        )

        nome_arquivo = (
            "tickets_exportados.xlsx"
        )

        mime_type = (
            "application/vnd.openxmlformats-officedocument."
            "spreadsheetml.sheet"
        )

    st.session_state[
        "arquivo_exportacao"
    ] = arquivo_bytes

    st.session_state[
        "nome_arquivo_exportacao"
    ] = nome_arquivo

    st.session_state[
        "mime_type_exportacao"
    ] = mime_type

    st.session_state[
        "formato_arquivo_exportacao"
    ] = formato_exportacao


def render_resultado():

    arquivo_bytes = st.session_state.get(
        "arquivo_exportacao"
    )

    if not arquivo_bytes:

        return

    nome_arquivo = st.session_state.get(
        "nome_arquivo_exportacao"
    )

    mime_type = st.session_state.get(
        "mime_type_exportacao"
    )

    formato_exportacao = st.session_state.get(
        "formato_arquivo_exportacao"
    )

    st.download_button(
        label=f"Baixar {formato_exportacao}",
        data=arquivo_bytes,
        file_name=nome_arquivo,
        mime=mime_type,
        use_container_width=True,
        key="download_exportacao",
    )

    st.divider()

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

    if not enviar_email:

        return

    if not destinatario.strip():

        st.warning(
            "Informe o e-mail do destinatário."
        )

        return

    arquivo_temporario = None

    try:

        extensao = (
            ".csv"
            if formato_exportacao == "CSV"
            else ".xlsx"
        )

        with NamedTemporaryFile(
            suffix=extensao,
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
                f"✅ Arquivo enviado com sucesso para "
                f"{destinatario.strip()}."
            )

            st.toast(
                "E-mail enviado!"
            )

        else:

            st.error(
                "❌ Não foi possível enviar o e-mail. "
                "Verifique o endereço informado e tente novamente."
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