"""
==========================================================
Support Investigator V2

Arquivo:
export_page.py

Responsabilidade:
Renderizar a página de exportação.

Autor:
Elias Nunes
==========================================================
"""

import streamlit as st

from ui.export import (
    render as render_export,
    processar_exportacao,
    render_resultado,
)


def render():
    """
    Renderiza a página Export.
    """

    st.markdown(
        "## Export"
    )

    st.caption(
        "Exporte informações de suporte para análise e relatórios."
    )

    (
        email_exportacao,
        status_exportacao,
        formato_exportacao,
        gerar_exportacao,
    ) = render_export()

    if gerar_exportacao:

        processar_exportacao(
            email_exportacao,
            status_exportacao,
            formato_exportacao,
        )

    render_resultado()