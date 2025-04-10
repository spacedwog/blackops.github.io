import pytest
from unittest.mock import patch, MagicMock
from github_dashboard import GitHubDashboard

# Dados simulados
user_data_mock = {
    "avatar_url": "https://example.com/avatar.png",
    "name": "John Doe",
    "login": "johndoe",
    "html_url": "https://github.com/johndoe",
    "location": "Internet",
    "email": "john@example.com",
    "bio": "Just a test user",
    "repos_url": "https://api.github.com/users/johndoe/repos",
    "public_repos": 10,
    "followers": 50
}

@pytest.fixture
def dashboard():
    return GitHubDashboard(user_data=user_data_mock)

def test_inicializacao(dashboard):
    assert dashboard.user_data["login"] == "johndoe"

@patch("github_dashboard.requests.get")
def test_exibir_repositorios_publicos(mock_get, dashboard):
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [
        {"name": "repo1", "html_url": "https://github.com/repo1", "stargazers_count": 5},
        {"name": "repo2", "html_url": "https://github.com/repo2", "stargazers_count": 3}
    ]

    # Simula o ambiente do Streamlit
    with patch("streamlit.markdown"), patch("streamlit.subheader"):
        dashboard.exibir_repositorios_publicos()

@patch("github_dashboard.requests.get")
def test_exibir_lista_repositorios(mock_get, dashboard):
    mock_get.return_value.json.return_value = [
        {
            "name": "repo1",
            "description": "desc1",
            "stargazers_count": 1,
            "forks_count": 2,
            "html_url": "https://github.com/repo1",
            "language": "Python",
            "updated_at": "2025-04-10T00:00:00Z"
        }
    ]
    with patch("streamlit.subheader"), patch("streamlit.dataframe"):
        dashboard.exibir_lista_repositorios()

def test_modelo_regressao(dashboard):
    with patch("streamlit.subheader"), patch("streamlit.text"), patch("streamlit.write"):
        dashboard.exibir_data_science_resumo()

@patch("github_dashboard.serial.Serial")
def test_enviar_comando_serial(mock_serial, dashboard):
    ser_mock = MagicMock()
    mock_serial.return_value.__enter__.return_value = ser_mock
    dashboard.enviar_comando("COM1", 9600, b"RESTART\n", log := [])
    assert "RESTART" in log[0]

def test_decodificar_resposta_utf8(dashboard):
    log = []
    raw = b"OK\n"
    decoded = dashboard.decodificar_resposta(raw, log)
    assert decoded.strip() == "OK"
    assert "UTF-8" in log[0]

def test_decodificar_resposta_latin1(dashboard):
    log = []
    raw = b"\xe9"  # é em Latin1
    decoded = dashboard.decodificar_resposta(raw, log)
    assert "Latin-1" in log[0]