import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Dimensions } from 'react-native';
import { Text, Button, Provider as PaperProvider } from 'react-native-paper';
import { TabView, SceneMap, TabBar } from 'react-native-tab-view';

const NODEMCU_IP = 'http://192.168.15.8:8080';

export default function App() {
  const [message, setMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');
  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'status', title: 'Status' },
    { key: 'controle', title: 'Controle' },
    { key: 'logs', title: 'Logs' },
  ]);

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

  const sendCommand = (cmd) => {
    fetch(`${NODEMCU_IP}/${cmd}`)
      .then(res => res.text())
      .then(data => {
        setMessage(`📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data}`);
        fetchStatus();
      })
      .catch(error => {
        setMessage(`Erro ao enviar comando ${cmd}: ` + error.message);
      });
  };

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  const StatusRoute = () => (
    <View style={styles.tabContent}>
      <Text style={[styles.statusText, { color: statusColor }]}>{message}</Text>
    </View>
  );

  const ControleRoute = () => (
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

  const LogsRoute = () => (
    <View style={styles.tabContent}>
      <Text style={styles.logsText}>{message}</Text>
    </View>
  );

  const renderScene = SceneMap({
    status: StatusRoute,
    controle: ControleRoute,
    logs: LogsRoute,
  });

  return (
    <PaperProvider>
      <TabView
        navigationState={{ index, routes }}
        renderScene={renderScene}
        onIndexChange={setIndex}
        initialLayout={{ width: Dimensions.get('window').width }}
        renderTabBar={props =>
          <TabBar
            {...props}
            indicatorStyle={{ backgroundColor: 'blue' }}
            style={{ backgroundColor: 'white' }}
            labelStyle={{ color: 'black' }}
          />
        }
      />
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
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