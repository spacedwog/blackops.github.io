import React, { useEffect, useState } from 'react';
import { StyleSheet, View } from 'react-native';
import { Text, Button, Tab, Tabs, Provider as PaperProvider } from 'react-native-paper';

// IP do NodeMCU (ajuste conforme necessário)
const NODEMCU_IP = 'http://192.168.15.8:8080';

export default function App() {
  const [message, setMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');
  const [index, setIndex] = useState(0);

  // Função para buscar status
  const fetchStatus = () => {
    fetch(`${NODEMCU_IP}/STATUS`)
      .then(res => res.text())
      .then(data => {
        if(data.startsWith("[JAVA]")){
          if (data.match('STATE:ON')) {
            setMessage("✅ Relé ligado (NodeMCU)");
            setStatusColor("green");
          } else if (data.match('STATE:OFF')) {
            setMessage("⚠️ Relé desligado (NodeMCU)");
            setStatusColor("red");
          } else {
            setMessage("🔄 Status desconhecido: " + data);
            setStatusColor("gray");
          }
        } else {
          setMessage("🔄 Status desconhecido: " + data);
          setStatusColor("gray");
        }
      })
      .catch(error => {
        setMessage("Erro ao conectar ao NodeMCU: " + error.message);
        setStatusColor("red");
      });
  };

  // Função para enviar comando ao relé
  const sendCommand = (cmd) => {
    fetch(`${NODEMCU_IP}/${cmd}`)
      .then(res => res.text())
      .then(data => {
        setMessage(`📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data}`);
        fetchStatus(); // Atualiza após envio
      })
      .catch(error => {
        setMessage(`Erro ao enviar comando ${cmd}: ` + error.message);
      });
  };

  // Atualiza status a cada 5s
  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <PaperProvider>
      <View style={styles.container}>
        <Tabs
          navigationState={{ index, routes: [
            { key: 'status', title: 'Status' },
            { key: 'controle', title: 'Controle' },
            { key: 'logs', title: 'Logs' },
          ] }}
          onIndexChange={setIndex}
          renderScene={({ route }) => {
            switch (route.key) {
              case 'status':
                return (
                  <View style={styles.tabContent}>
                    <Text style={[styles.statusText, { color: statusColor }]}>{message}</Text>
                  </View>
                );
              case 'controle':
                return (
                  <View style={styles.tabContent}>
                    <Button
                      mode="contained"
                      onPress={() => sendCommand('LIGAR')}
                      style={[styles.button, { backgroundColor: 'green' }]}
                    >
                      LIGAR
                    </Button>
                    <Button
                      mode="contained"
                      onPress={() => sendCommand('DESLIGAR')}
                      style={[styles.button, { backgroundColor: 'red' }]}
                    >
                      DESLIGAR
                    </Button>
                  </View>
                );
              case 'logs':
                return (
                  <View style={styles.tabContent}>
                    <Text style={styles.logsText}>{message}</Text>
                  </View>
                );
              default:
                return null;
            }
          }}
        />
      </View>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  tabContent: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 20,
  },
  statusText: {
    fontSize: 20,
    fontWeight: 'bold',
    textAlign: 'center',
  },
  button: {
    marginVertical: 10,
    width: '70%',
    alignSelf: 'center',
  },
  logsText: {
    fontSize: 16,
    fontFamily: 'monospace',
  },
});