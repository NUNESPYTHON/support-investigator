"""
==========================================================
Support Investigator

Arquivo:
navigation.py

Responsabilidade:
Controlar o estado e a navegação da interface.

Autor:
Elias Nunes
==========================================================
"""


def inicializar_estado(st):
    """
    Inicializa os estados usados pela interface.
    """

    if "active_view" not in st.session_state:

        st.session_state["active_view"] = None

    if "historico_cliente" not in st.session_state:

        st.session_state["historico_cliente"] = None

    if "ticket_selecionado" not in st.session_state:

        st.session_state["ticket_selecionado"] = None


def abrir_ticket(st):
    """
    Define a área de ticket como ativa.
    """

    st.session_state["active_view"] = "ticket"

    st.session_state["historico_cliente"] = None

    st.session_state["ticket_selecionado"] = None


def abrir_historico(st):
    """
    Define a área de histórico como ativa.
    """

    st.session_state["active_view"] = "history"

    st.session_state["ticket_selecionado"] = None


def abrir_exportacao(st):
    """
    Define a área de exportação como ativa.
    """

    st.session_state["active_view"] = "export"

    st.session_state["historico_cliente"] = None

    st.session_state["ticket_selecionado"] = None


def selecionar_ticket(st, ticket_id):
    """
    Seleciona um ticket para visualização.
    """

    st.session_state["ticket_selecionado"] = str(
        ticket_id
    )


def fechar_detalhes(st):
    """
    Fecha os detalhes do ticket selecionado.
    """

    st.session_state["ticket_selecionado"] = None