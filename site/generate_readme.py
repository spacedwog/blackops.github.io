import os
import pypandoc
import streamlit as st

def generate_readme():
    st.markdown("""
        ### Explicação:
        1. **Leitura e Conversão de HTML para Markdown**: O script lê o arquivo HTML de `site/reference/index.html` e o converte para Markdown utilizando a biblioteca `pypandoc`.
        2. **Adição de Cabeçalho e Estrutura**: Após a conversão, ele adiciona um cabeçalho contendo informações sobre o projeto, como uma descrição, navegação e funcionalidades principais.
        3. **Geração do `README.md`**: O script combina o conteúdo convertido com o cabeçalho e gera o arquivo `README.md`.
        4. **Verificação de Arquivo**: Caso o arquivo `index.html` não seja encontrado, o script exibe uma mensagem de erro.

        ### Como Usar:
        1. Salve o código em um arquivo chamado `generate_readme.py`.
        2. Execute o script:
        ```bash
        python generate_readme.py
    """)
    source_file = os.path.join("site", "reference", "index.html")
    output_file = "README.md"

    if not os.path.exists(source_file):
        print(f"❌ Arquivo não encontrado: {source_file}")
        return

    try:
        print("🔄 Convertendo HTML para Markdown...")
        # Converte o HTML em Markdown usando pypandoc
        markdown = pypandoc.convert_file(source_file, "md")

        # Adiciona uma estrutura de navegação e informações adicionais ao Markdown
        header = """
# Projeto BlackOps - Docs

## Descrição

O **Projeto BlackOps** é uma iniciativa focada em cibersegurança e integração de tecnologias, incluindo automação, redes e interfaces inteligentes.

---

## Navegação

* [Início](index.md)
* [Referência](#referencia)
    * [Interface Streamlit](reference/ui/streamlit_interface.md)
    * [OCR RFID](reference/ai/ocr_rfid.md)
    * [Voice Control](reference/ai/voice_control.md)
    * [Relay Control](reference/core/relay_control.md)
    * [GitHub Utils](reference/core/github_utils.md)
    * [Port Scanner](reference/network/port_scanner.md)
    * [Firewall Checker](reference/network/firewall_checker.md)

---

## Funcionalidades

1. **Controle de Relay (GPIO):** Controle físico de relays para automação e testes de hardware.
2. **Verificador de Firewall e Portas:** Ferramenta para escaneamento de portas e verificação de regras de firewall.
3. **Reconhecimento de Voz:** Comandos de voz para interação com o sistema.
4. **OCR e Transmissão de Vídeo:** Captura de vídeo e reconhecimento de texto através de OCR para interface interativa.

---

## Como Usar

1. Clone o repositório:
   ```bash
   git clone https://github.com/seu-usuario/blackops.git
   cd blackops
"""
            # Combina o conteúdo da conversão com o cabeçalho
        full_markdown = header + "\n" + markdown

        # Cria ou sobrescreve o README.md com o conteúdo
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(full_markdown)

        print(f"✅ README.md gerado com sucesso em: {output_file}")

    except Exception as e:
        print(f"❌ Erro ao converter: {e}")
if __name__ == "__main__": generate_readme()