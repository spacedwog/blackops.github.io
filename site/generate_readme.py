import pypandoc
import os

def generate_readme():
    source_file = os.path.join("site", "reference", "index.html")
    output_file = "README.md"

    if not os.path.exists(source_file):
        print(f"❌ Arquivo não encontrado: {source_file}")
        return

    try:
        print("🔄 Convertendo HTML para Markdown...")
        markdown = pypandoc.convert_file(source_file, "md")

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(markdown)

        print(f"✅ README.md gerado com sucesso em: {output_file}")

    except Exception as e:
        print(f"❌ Erro ao converter: {e}")

if __name__ == "__main__":
    generate_readme()