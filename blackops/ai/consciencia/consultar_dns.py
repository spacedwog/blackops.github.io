# -----------------------------
# consciencia/consultar_dns.py
# -----------------------------
import io
import sys
import time
import socket
import schedule
import threading
import numpy as np
import dns.resolver
import pandas as pd
from pymongo import MongoClient
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.ensemble import IsolationForest
from statsmodels.tsa.holtwinters import ExponentialSmoothing

class DataScienceDNS:
    
    def __init__(self):
        self.dns_data = pd.DataFrame()
        self.history = []
        self.agendamento_ativo = False

    def consultar_dns(self, dominio, timestamp):

        # Faça isso no script principal, com segurança
        if sys.stdout.encoding != 'utf-8':
            sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf-8', buffering=1)

        try:
            ip_resolvido = socket.gethostbyname(dominio)
        except Exception as e:
            ip_resolvido = "Erro: " + str(e)

        consulta = {
            'dominio': dominio,
            'ip': ip_resolvido,
            'timestamp': timestamp,
            'query_count': np.random.randint(1, 100),
            'response_time': np.random.uniform(10, 300)
        }

        # Cálculo de índice de eficiência
        query_count = consulta['query_count']
        response_time = consulta['response_time']

        if query_count > response_time:
            consulta['efficiency_index'] = query_count / response_time
        elif query_count < response_time:
            consulta['efficiency_index'] = response_time * query_count
        else:
            consulta['efficiency_index'] = response_time / query_count

        self.history.append(consulta)
        self.dns_data = pd.DataFrame(self.history)

        descricao = self.dns_data[['query_count', 'response_time', 'efficiency_index']].describe()

        # Previsão apenas com dados suficientes
        if len(self.dns_data) > 5:
            self.previsao_dns()

        self.detectar_anomalias()
        self.clusterizar_dns()

        print(f"\n🧠 Consulta DNS para o domínio: {dominio}")
        print(f"📡 IP Resolvido: {ip_resolvido}")
        print(f"📊 Dados coletados: {consulta}")
        print("\n📈 Estatísticas básicas:")
        print(descricao)

        self.visualizar_metricas()

        return consulta

    def exportar_csv(self, caminho="dados_dns.csv"):
        self.dns_data.to_csv(caminho, index=False)

    def exportar_mongodb(self, uri, db, collection):
        client = MongoClient(uri)
        col = client[db][collection]
        col.insert_many(self.dns_data.to_dict("records"))
        client.close()

    def agendar_coleta(self, dominio, intervalo=10):
        def job():
            now = pd.Timestamp.now()
            self.consultar_dns(dominio, now)

        if not self.agendamento_ativo:
            schedule.every(intervalo).seconds.do(job)
            self.agendamento_ativo = True
            threading.Thread(target=self.executar_agendador, daemon=True).start()

    def executar_agendador(self):
        while True:
            schedule.run_pending()
            time.sleep(1)

    def pesquisa_avancada(self, dominio: str) -> dict:

        resultado = {}
        
        for tipo in ['A', 'AAAA', 'MX', 'NS', 'TXT']:
            try:
                resposta = dns.resolver.resolve(dominio, tipo)
                resultado[tipo] = [r.to_text() for r in resposta]
            except Exception as e:
                resultado[tipo] = f"Erro: {e}"
        return resultado

    def previsao_dns(self):

        if 'timestamp' not in self.dns_data.columns or self.dns_data.empty:
            print("[!] Dados insuficientes para previsão. Faça uma coleta primeiro.")
            return

        self.dns_data['timestamp'] = pd.to_datetime(self.dns_data['timestamp'])
        self.dns_data.set_index('timestamp', inplace=True)
        self.dns_data_resampled = self.dns_data['query_count'].resample('D').sum()

        model = ExponentialSmoothing(self.dns_data_resampled, trend='add', seasonal='add', seasonal_periods=7)
        model_fit = model.fit()
        forecast = model_fit.forecast(steps=7)

        plt.figure(figsize=(10, 6))
        plt.plot(self.dns_data_resampled, label='Consultas Passadas')
        plt.plot(forecast, label='Previsão Próximos 7 dias', linestyle='--')
        plt.title("Previsão de Consultas DNS")
        plt.xlabel("Data")
        plt.ylabel("Consultas")
        plt.legend()
        plt.show()

    def detectar_anomalias(self):
        
        required_columns = {'query_count', 'response_time', 'efficiency_index'}
        if not required_columns.issubset(self.dns_data.columns):
            print("[!] Colunas necessárias ausentes. Realize uma consulta DNS primeiro.")
            return

        isolation_forest = IsolationForest(contamination=0.1)
        self.dns_data['anomalia'] = isolation_forest.fit_predict(
            self.dns_data[['query_count', 'response_time', 'efficiency_index']]
        )

    def clusterizar_dns(self):

        if len(self.dns_data) > 5:
            kmeans = KMeans(n_clusters=3, n_init='auto')
            features = self.dns_data[['query_count', 'response_time', 'efficiency_index']]
            self.dns_data['cluster'] = kmeans.fit_predict(features)

            fig = go.Figure()
            for cluster in range(3):
                cluster_data = self.dns_data[self.dns_data['cluster'] == cluster]
                fig.add_trace(go.Scatter(
                    x=cluster_data['timestamp'],
                    y=cluster_data['query_count'],
                    mode='markers',
                    name=f'Cluster {cluster}'
                ))
            fig.update_layout(title='Clusterização de Consultas DNS',
                              xaxis_title='Data', yaxis_title='Consultas',
                              legend_title="Cluster")
            fig.show()

    def visualizar_metricas(self):

        if 'timestamp' not in self.dns_data.columns and self.dns_data.index.name == 'timestamp':
            self.dns_data = self.dns_data.reset_index()

        self.dns_data['timestamp'] = pd.to_datetime(self.dns_data['timestamp'])
        self.dns_data = self.dns_data.set_index('timestamp')

        # Gráfico Matplotlib
        fig, ax = plt.subplots(figsize=(10, 6))

        self.dns_data['query_count'].plot(ax=ax, label='Consultas', color='b')
        self.dns_data['response_time'].plot(ax=ax, label='Tempo de Resposta', color='r')
        
        ax.set_title("Métricas de Tráfego DNS")
        ax.set_xlabel("Data")
        ax.set_ylabel("Valores")
        ax.legend()
        
        plt.show()

        # Gráfico Plotly
        fig2 = go.Figure()

        fig2.add_trace(go.Scatter(
            x=self.dns_data.index,
            y=self.dns_data['efficiency_index'],
            mode='lines+markers',
            name='Índice de Eficiência',
            line=dict(color='green')
        ))

        fig2.update_layout(
            title='Índice de Eficiência de Consultas DNS',
            xaxis_title='Timestamp',
            yaxis_title='Consultas por Tempo (QPS)',
            legend_title='Métrica'
        )

        fig2.show()