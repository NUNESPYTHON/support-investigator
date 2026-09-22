"""
==========================================================
Support Investigator V2

Arquivo:
dashboard.py

Responsabilidade:
Renderizar a página principal do Dashboard.

Autor:
Elias Nunes
==========================================================
"""

from ui.dashboard_header import (
    render as render_dashboard_header,
)


def render():
    """
    Renderiza o Dashboard.
    """

    render_dashboard_header()