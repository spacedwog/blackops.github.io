# --------------------------------------
# consciencia/main_consciousness.py
# --------------------------------------
from processor import CommandProcessor
from base_query import VoiceGitHubAssistantQuery

class VoiceConsciousness:
    def __init__(self, mongo_uri, database_name):
        self.query = VoiceGitHubAssistantQuery(mongo_uri, database_name)
        self.processor = CommandProcessor()

    def iniciar(self):
        self.query.conectar()

        comandos = self.query.buscar_por_comando_normalizado("estatistica de voz")
        for comando_doc in comandos:
            comando_texto = comando_doc.get("comando_normalizado", "")
            print(f"\n🧠 Comando detectado: {comando_texto}")
            self.processor.process(comando_texto)

        self.query.desconectar()

# Execução direta
if __name__ == "__main__":
    vc = VoiceConsciousness(
        mongo_uri="mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/",
        database_name="voice_github_assistant"
    )
    vc.iniciar()