# -----------------------------
# blackops/blackops_api.py
# -----------------------------
from flask import Flask, jsonify, request
from blackops import buscar_comandos_localmente

app = Flask(__name__)

@app.route("/buscar_comandos", methods=["GET"])
def buscar_comandos():
    comando = request.args.get("comando", default="estatísticas de voz")
    resultados = buscar_comandos_localmente(comando)
    return jsonify(resultados)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8502)