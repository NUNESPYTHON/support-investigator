"""
==========================================================
Zendesk Investigator

Arquivo:
formatters.py

Responsabilidade:
Centralizar funções de formatação da aplicação.

Autor:
Elias Nunes

==========================================================
"""

"""
==========================================================
Zendesk Investigator

Arquivo:
formatters.py

Responsabilidade:
Centralizar funções de formatação da aplicação.

Autor:
Elias Nunes
==========================================================
"""

from datetime import datetime


def formatar_tempo(minutos):
    """
    Converte minutos em uma representação legível.

    Exemplos:
        18 -> "18 minutos"
        135 -> "2 horas e 15 minutos"
        19080 -> "13 dias e 6 horas"
        None -> "Ainda não respondido"

    Args:
        minutos (int | float | None): Tempo em minutos.

    Returns:
        str: Tempo formatado.
    """

    if minutos is None:
        return "Ainda não respondido"
    

    minutos = int(minutos)

    dias = minutos // (24 * 60)
    minutos_restantes = minutos % (24 * 60)

    horas = minutos_restantes // 60
    minutos_finais = minutos_restantes % 60
    partes = []

    if dias:
        partes.append(
            f"{dias} {'dia' if dias == 1 else 'dias'}"
        )

    if horas:
        partes.append(
            f"{horas} {'hora' if horas == 1 else 'horas'}"
        )

    if minutos_finais:
        partes.append(
            f"{minutos_finais} "
            f"{'minuto' if minutos_finais == 1 else 'minutos'}"
        )

    if not partes:
        return "0 minutos"

    return " e ".join(partes)

def formatar_data(data_iso):
    """
    Converte uma data ISO 8601 para um formato amigável.

    Args:
        data_iso (str): Data no formato ISO 8601.

    Returns:
        str: Data formatada.
    """

    if not data_iso:
        return "Data não informada"

    data = datetime.fromisoformat(
        data_iso.replace("Z", "+00:00")
    )

    data_local = data.astimezone()

    return data_local.strftime(
        "%d/%m/%Y às %H:%M"
    )