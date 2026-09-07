from services.email import enviar_arquivo_email


arquivo = "tickets.csv"

destinatario = "SEU_EMAIL_DE_TESTE"

assunto = "Zendesk Investigator - Teste de exportação"

corpo = """Olá,

Este é um teste do Zendesk Investigator.

O arquivo CSV está anexado a este e-mail.

Atenciosamente,
Zendesk Investigator
"""


resultado = enviar_arquivo_email(
    arquivo,
    destinatario,
    assunto,
    corpo,
)


if resultado:

    print()
    print("=" * 60)
    print("E-MAIL ENVIADO COM SUCESSO")
    print("=" * 60)
    print()
    print("Arquivo:", arquivo)
    print("Destinatário:", destinatario)
    print()
    print("=" * 60)

else:

    print()
    print("Falha no envio do e-mail.")