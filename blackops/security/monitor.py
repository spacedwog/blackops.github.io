# -----------------------------
# security/monitor.py
# -----------------------------
import os
import json
import psutil
import random
import subprocess
import streamlit as st
from datetime import datetime
from collections import Counter
from security.database import MongoDBHandler  # Importando o manipulador do MongoDB

class CyberSecurityMonitor:
    dados_ameacas = []

    @classmethod
    def registrar_ameacas_detectadas(cls, ips_suspeitos):
        mongodb = MongoDBHandler()  # cria dentro do método
        for ip in set(ips_suspeitos):
            risco = "baixo" if ips_suspeitos.count(ip) <= 2 else "elevado"
            detalhes = f"Detectado múltiplas vezes ({ips_suspeitos.count(ip)} ocorrências)"
            mongodb.registrar_ameaca(ip=ip, risco=risco, detalhes=detalhes)

    @classmethod
    def registrar_ameaca(cls, ip, status):
        """Registra uma ameaça no monitor com IP, status e hora da detecção."""
        cls.dados_ameacas.append({
            "ip": ip,
            "status": status,
            "hora": datetime.now().strftime("%H:%M:%S")
        })

    @classmethod
    def exibir_visual_cyberpunk(cls):
        """Exibe o radar estilo cyberpunk com as ameaças detectadas."""
        data = cls.dados_ameacas

        if not data:
            st.warning("⚠️ Nenhuma ameaça detectada ainda.")
            return

        points = [{
            "x": random.randint(10, 90),
            "y": random.randint(10, 90),
            "info": f"IP: {entry['ip']}<br>Status: {entry['status']}<br>Hora: {entry['hora']}"
        } for entry in data]

        # Estilo cyberpunk (fundo preto e pontos vermelhos neon)
        html = """
        <style>
            .radar-container {
                position: relative;
                width: 100%;
                height: 500px;
                background-color: black;
                border: 2px solid #ff004c;
                border-radius: 12px;
                overflow: hidden;
            }
            .radar-point {
                position: absolute;
                width: 12px;
                height: 12px;
                border-radius: 50%;
                background-color: #ff004c;
                box-shadow: 0 0 10px #ff004c, 0 0 20px #ff004c;
                transition: transform 0.2s ease-in-out;
            }
            .radar-point:hover::after {
                content: attr(data-info);
                position: absolute;
                top: 20px;
                left: 20px;
                background: rgba(255, 0, 76, 0.9);
                color: white;
                padding: 8px;
                border-radius: 8px;
                white-space: nowrap;
                font-size: 13px;
                z-index: 999;
                pointer-events: none;
            }
        </style>
        <div class="radar-container">
        """

        for point in points:
            html += f"""
            <div class="radar-point" style="top: {point['y']}%; left: {point['x']}%;" 
                 data-info="{point['info']}"></div>
            """

        html += "</div>"

        st.markdown(html, unsafe_allow_html=True)

    @classmethod
    def exibir_lista_ameacas(cls):
        mongodb = MongoDBHandler()  # cria aqui também

        st.subheader("📜 Histórico de Ameaças Registradas")
        ameacas = mongodb.listar_ameacas()

        if not ameacas:
            st.info("✅ Nenhuma ameaça registrada.")
            return

        for i, ameaca in enumerate(ameacas, 1):
            st.markdown(f"""
                <div style='background-color:#111111;padding:10px;margin-bottom:10px;border-left: 4px solid #f44336;'>
                    <strong>🔻 IP:</strong> {ameaca['ip']}<br>
                    <strong>Risco:</strong> {ameaca['risco'].upper()}<br>
                    <strong>Detalhes:</strong> {ameaca.get('detalhes', 'Não informado')}<br>
                    <small><strong>Registrado em:</strong> {ameaca['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}</small>
                </div>
            """, unsafe_allow_html=True)

        if st.button("🗑️ Limpar Histórico de Ameaças", key="btn_limpar_ameacas"):
            mongodb.apagar_todas()
            st.success("🧹 Histórico apagado com sucesso!")


    @classmethod
    def listar_conexoes(cls):

        st.subheader("🌐 Conexões de Rede Atuais")
        conexoes = psutil.net_connections(kind='inet')
        processos = []
        for c in conexoes:
            if c.status == "ESTABLISHED" and c.raddr:
                processo = {
                    "PID": c.pid,
                    "Local": f"{c.laddr.ip}:{c.laddr.port}",
                    "Remoto": f"{c.raddr.ip}:{c.raddr.port}",
                    "Status": c.status
                }
                processos.append(processo)

        if processos:
            st.table(processos)
        else:
            st.info("🔍 Nenhuma conexão ativa detectada.")
        return processos

    @classmethod
    def detectar_ips_suspeitos(cls, conexoes):
        
        st.subheader("🚨 Detecção de IPs Remotos Suspeitos")
        ips_suspeitos = []
        todos_ips = []

        for conn in conexoes:
            ip = conn["Remoto"].split(":")[0]
            todos_ips.append(ip)
            if not ip.startswith(("127.", "192.", "10.", "172.")):  # não local
                ips_suspeitos.append(ip)

        frequencias = Counter(ips_suspeitos)
        if not frequencias:
            st.success("✅ Nenhuma conexão suspeita identificada.")
        else:
            for ip, count in frequencias.items():
                alerta = "⚠️" if count < 3 else "🛑"
                st.warning(f"{alerta} IP suspeito: `{ip}` com {count} conexões simultâneas")

        return todos_ips, ips_suspeitos

    @classmethod
    def verificar_portas_escutando(cls):

        st.subheader("🔌 Portas Locais Escutando (LISTEN)")
        escutando = []
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == "LISTEN" and conn.laddr:
                escutando.append(f"{conn.laddr.ip}:{conn.laddr.port}")

        if escutando:
            for porta in escutando:
                st.info(f"• {porta}")
        else:
            st.success("✅ Nenhuma porta em escuta detectada.")
        return escutando

    @classmethod
    def gerar_log_json(cls, conexoes, ips_suspeitos, escutando):

        st.subheader("📤 Exportar Log Estruturado (JSON)")

        log_data = {
            "timestamp": str(datetime.now()),
            "conexoes_estabelecidas": conexoes,
            "ips_suspeitos": list(set(ips_suspeitos)),
            "portas_escutando": escutando
        }

        os.makedirs("logs", exist_ok=True)
        caminho = "logs/log_segurança.json"
        with open(caminho, "w") as f:
            json.dump(log_data, f, indent=4)

        st.success(f"📁 Log estruturado salvo em: `{caminho}`")

    @classmethod
    def resposta_mitigacao(cls, ips_suspeitos):

        st.subheader("🧱 Resposta e Mitigação (Simulada)")

        if not ips_suspeitos:
            st.success("✅ Nenhuma ação necessária. Ambiente considerado seguro.")
            return

        for ip in set(ips_suspeitos):
            risco = "baixo" if ips_suspeitos.count(ip) <= 2 else "elevado"
            cor = "🟡" if risco == "baixo" else "🔴"
            st.markdown(f"{cor} **IP:** `{ip}` | **Risco:** `{risco.upper()}`")

            if risco == "elevado":
                st.code(f"sudo iptables -A INPUT -s {ip} -j DROP", language="bash")
                st.info(f"Simulação: bloqueio sugerido para IP `{ip}` via firewall.")
            else:
                st.text(f"Recomenda-se monitoramento contínuo para o IP {ip}.")

        # Dentro do método resposta_mitigacao
        if st.button("📬 Simular Envio de Alerta para Admin", key=f"btn_alerta_admin_{ip}"):
            data = {
                "timestamp": str(datetime.now()),
                "ips_bloqueados": list(set(ips_suspeitos)),
                "acao": "bloqueio_sugerido",
                "notificacao": "alerta_administrador"
            }
            st.json(data)
            st.success("📨 Alerta de segurança simulado enviado ao administrador (SOC).")

    @classmethod
    def executar_resposta_mitigacao_completa(cls):

        st.markdown("""
            <style>
            .painel-cyberpunk {
                background-color: #000000;
                padding: 20px;
                border-radius: 10px;
                color: #39ff14;
                font-family: 'Courier New', monospace;
                box-shadow: 0 0 15px #39ff14;
            }
            </style>
        """, unsafe_allow_html=True)

        st.markdown("<div class='painel-cyberpunk'>", unsafe_allow_html=True)
        st.header("🌐 Painel Cyberpunk: Mitigação de Ameaças")

        if not cls.dados_ameacas:
            st.success("✅ Nenhuma ameaça registrada. Ambiente estável.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        ips_detectados = [entrada["ip"] for entrada in cls.dados_ameacas]
        cls.resposta_mitigacao(ips_detectados)
        cls.registrar_ameacas_detectadas(ips_detectados)

        st.markdown("</div>", unsafe_allow_html=True)

    @classmethod
    def exibir_monitoramento(cls):

        st.header("🛡️ Módulo de Cibersegurança")

        if st.button("🔄 Abrir Painel DNS"):
            try:
                comando = "./executar_paineldns.ps1"
                resultado = subprocess.run(
                    ["powershell", "-Command", comando],
                    capture_output=True,
                    text=True,
                    shell=True
                )
                st.code(resultado.stdout or resultado.stderr)
            except Exception as e:
                st.error(f"Erro ao executar: {e}")

        aba_conexao, aba_ips, aba_portas, aba_mitigacao = st.tabs(["🌐 Conexões", "🚨 IPs Suspeitos", "🔌 Portas Escutando", "🧱 Resposta de Mitigação"])

        with aba_conexao:
            # 1. Conexões
            conexoes = cls.listar_conexoes()
        with aba_ips:
            # 2. IPs suspeitos
            todos_ips, ips_suspeitos = cls.detectar_ips_suspeitos(conexoes)
        with aba_portas:
            # 3. Portas escutando
            escutando = cls.verificar_portas_escutando()

        # 4. Exportar JSON
        if st.button("📁 Gerar e Exportar Log de Segurança"):
            cls.gerar_log_json(conexoes, ips_suspeitos, escutando)

        with aba_mitigacao:
            # 5. Etapa de Resposta e Mitigação
            cls.resposta_mitigacao(ips_suspeitos)