from services.oauth import gerar_url_autorizacao


def test_gerar_url_autorizacao():

    resultado = gerar_url_autorizacao(
        subdomain="exemplo",
        client_kind="confidential",
        client_id="abc123",
        redirect_uri="http://localhost:8501",
        scope="tickets:read users:read organizations:read",
        state="test123",
    )

    url = resultado["url"]

    assert "https://exemplo.zendesk.com" in url
    assert "response_type=code" in url
    assert "client_id=abc123" in url
    assert "redirect_uri=http%3A%2F%2Flocalhost%3A8501" in url
    assert "state=test123" in url

    assert resultado["state"] == "test123"

    # Confidential não utiliza PKCE automaticamente
    assert resultado["code_verifier"] is None