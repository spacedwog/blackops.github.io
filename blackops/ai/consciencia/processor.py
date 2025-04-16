# --------------------------------------
# consciencia/processor.py
# --------------------------------------
class CommandProcessor:
    def process(self, comando):
        comando = comando.lower()

        if comando == "estatistica de voz":
            self.estatistica_de_voz()
        else:
            print(f"🤖 Comando não reconhecido: '{comando}'")

    def process_streamlit(self, comando):
        comando = comando.lower()

        if comando == "estatistica de voz":
            return self.estatistica_de_voz_streamlit()
        else:
            return f"🤖 Comando não reconhecido: '{comando}'"

    def estatistica_de_voz(self):
        print("🎤 Número de interações: 24")
        print("🗂️ Temas mais recorrentes: ['github', 'voz', 'cibersegurança']")

    def estatistica_de_voz_streamlit(self):
        return "🎤 Interações: 24 | Temas populares: GitHub, voz, cibersegurança"