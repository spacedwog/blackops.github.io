import React, { useEffect, useState } from 'react';
import { StyleSheet, View, Dimensions, ScrollView } from 'react-native';
import { Text, Button, Provider as PaperProvider } from 'react-native-paper';
import { TabView, SceneMap, TabBar } from 'react-native-tab-view';
import { RNCamera } from 'react-native-camera';
import NetInfo from "@react-native-community/netinfo";

const NODEMCU_IP = 'http://192.168.15.138:8080';

export default function App() {
  const [isCameraOn, setIsCameraOn] = useState(false);
  const [statusMessage, setStatusMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');

  const [diagnosesMessage, setDiagnosesMessage] = useState('Carregando diagnósticos...');
  const [blockedMessage, setBlockedMessage] = useState('Carregando bloqueios...');

  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'status', title: 'Status' },
    { key: 'controle', title: 'Controle' },
    { key: 'diagnoses', title: 'Diagnoses' },
    { key: 'blocked', title: 'Blocked' },
    { key: 'camera', title: 'Câmera' },
  ]);

  // Função para formatar mensagens que contenham [JAVA]
  const formatJavaMessage = (data) => {
    if (data.includes('[JAVA]')) {
      return "♨️ Conexão com servidor Java estabelecida.\n" + data.replace('[JAVA]', '').trim();
    }
    return data;
  };

  // Função para obter STATUS
  const fetchStatus = async () => {
    try {
      const state = await NetInfo.fetch();

      if (!state.isConnected) {
        setStatusMessage("Sem conexão com a internet/Wi-Fi.");
        setStatusColor("gray");
        return;
      }

      const response = await fetch(`${NODEMCU_IP}/STATUS`);
      const data = await response.text();

      if (data.includes('[JAVA]')) {
        if (data.includes('STATE:ON')) {
          setStatusMessage("♨️ Conexão com servidor Java estabelecida.\n✅ Relé ligado (NodeMCU)");
          setStatusColor("green");
        } else if (data.includes('STATE:OFF')) {
          setStatusMessage("♨️ Conexão com servidor Java estabelecida.\n⚠️ Relé desligado (NodeMCU)");
          setStatusColor("red");
        } else {
          setStatusMessage(formatJavaMessage(data));
          setStatusColor("gray");
        }
      } else {
        setStatusMessage("🔄 Status desconhecido: " + data);
        setStatusColor("gray");
      }

    } catch (error) {
      setStatusMessage("Erro ao conectar: " + error.message);
      setStatusColor("red");
    }
  };

  // Função para obter DIAGNOSES
  const fetchDiagnoses = async () => {
    try {
      const response = await fetch(`${NODEMCU_IP}/DIAGNOSES`);
      const data = await response.text();
      setDiagnosesMessage(formatJavaMessage(data) || 'Nenhum diagnóstico disponível.');
    } catch (error) {
      setDiagnosesMessage("Erro ao obter diagnósticos: " + error.message);
    }
  };

  // Função para obter BLOCKED
  const fetchBlocked = async () => {
    try {
      const response = await fetch(`${NODEMCU_IP}/BLOCKED`);
      const data = await response.text();
      setBlockedMessage(formatJavaMessage(data) || 'Nenhum bloqueio ativo.');
    } catch (error) {
      setBlockedMessage("Erro ao obter bloqueios: " + error.message);
    }
  };

  // Envia comandos LIGAR/DESLIGAR
  const sendCommand = (cmd) => {
    fetch(`${NODEMCU_IP}/${cmd}`)
      .then(res => res.text())
      .then(data => {
        if (data.includes('[JAVA]')) {
          setStatusMessage(`🔗 Conexão com servidor Java estabelecida.\n📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data.replace('[JAVA]', '').trim()}`);
        } else {
          setStatusMessage(`📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data}`);
        }
        fetchStatus();
      })
      .catch(error => {
        setStatusMessage(`Erro ao enviar comando ${cmd}: ` + error.message);
        setStatusColor('red');
      });
  };

  // Atualiza dados periodicamente
  useEffect(() => {
    fetchStatus();
    fetchDiagnoses();
    fetchBlocked();
    const interval = setInterval(() => {
      fetchStatus();
      fetchDiagnoses();
      fetchBlocked();
    }, 5000);
    return () => clearInterval(interval);
  }, []);

  // Componentes para cada aba
  const StatusRoute = () => (
    <View style={styles.tabContent}>
      <Text style={[styles.statusText, { color: statusColor }]}>{statusMessage}</Text>
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

  const DiagnosesRoute = () => (
    <ScrollView style={styles.scrollContent}>
      <Text style={styles.logsText}>{diagnosesMessage}</Text>
      <Button mode="outlined" onPress={fetchDiagnoses} style={styles.refreshButton}>
        Atualizar Diagnósticos
      </Button>
    </ScrollView>
  );

  const BlockedRoute = () => (
    <ScrollView style={styles.scrollContent}>
      <Text style={styles.logsText}>{blockedMessage}</Text>
      <Button mode="outlined" onPress={fetchBlocked} style={styles.refreshButton}>
        Atualizar Bloqueios
      </Button>
    </ScrollView>
  );

  const CameraRoute = () => (
    <View style={styles.tabContent}>
      <Button
        mode="contained"
        onPress={() => setIsCameraOn(!isCameraOn)}
        style={styles.button}
      >
        {isCameraOn ? 'Desligar Câmera' : 'Ligar Câmera'}
      </Button>
      {isCameraOn && (
        <RNCamera
          style={{ flex: 1, width: '100%', marginTop: 10 }}
          type={RNCamera.Constants.Type.back}
          captureAudio={false}
        />
      )}
    </View>
  );

  const renderScene = SceneMap({
    status: StatusRoute,
    controle: ControleRoute,
    diagnoses: DiagnosesRoute,
    blocked: BlockedRoute,
    camera: CameraRoute,
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
  scrollContent: {
    flex: 1,
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
  refreshButton: {
    marginTop: 20,
    alignSelf: 'center',
    width: '60%',
  },
  logsText: {
    fontSize: 16,
    fontFamily: 'monospace',
  },
});