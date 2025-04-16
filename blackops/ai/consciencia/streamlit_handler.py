# --------------------------------------
# consciencia/streamlit_handler.py
# --------------------------------------
from .base_query import VoiceGitHubAssistantQuery
from .processor import CommandProcessor

def executar_consciencia_virtual(mongo_uri, database_name, comando, colecao):
    query = VoiceGitHubAssistantQuery(mongo_uri, database_name)
    processor = CommandProcessor()

    query.conectar()
    resultados = query.buscar_por_comando_normalizado(comando, colecao)

    logs = []
    for doc in resultados:
        comando_texto = doc.get("comando_normalizado", "")
        log = processor.process_streamlit(comando_texto)
        logs.append({"comando": comando_texto, "log": log})

    query.desconectar()
    return logs