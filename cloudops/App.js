import React, { useEffect, useState } from 'react';
import { StyleSheet, Dimensions, ScrollView, RefreshControl, } from 'react-native';
import { Text, Button, Provider as PaperProvider, ActivityIndicator, } from 'react-native-paper';
import { TabView, TabBar } from 'react-native-tab-view';
import NetInfo from '@react-native-community/netinfo';

const NODEMCU_IP = 'http://192.168.15.138:8080';

export default function App() {
  const [statusMessage, setStatusMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');
  const [diagnosesMessage, setDiagnosesMessage] = useState('Carregando diagnósticos...');
  const [blockedMessage, setBlockedMessage] = useState('Carregando bloqueios...');
  const [isSendingCommand, setIsSendingCommand] = useState(false);
  const [wireMessage, setWireMessage] = useState('Carregando dados I2C...');

  const [refreshingStatus, setRefreshingStatus] = useState(false);
  const [refreshingControle, setRefreshingControle] = useState(false);
  const [refreshingDiagnoses, setRefreshingDiagnoses] = useState(false);
  const [refreshingBlocked, setRefreshingBlocked] = useState(false);
  const [refreshingWire, setRefreshingWire] = useState(false);

  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'status', title: 'Status' },
    { key: 'controle', title: 'Controle' },
    { key: 'diagnoses', title: 'Diagnoses' },
    { key: 'blocked', title: 'Blocked' },
    { key: 'wire', title: 'Wire' },
  ]);

  const formatMessage = (data) => {
    if (data.includes('[ARDUINO]')) {
      return '🤖 Conexão com servidor Arduino estabelecida.\n' + data.replace('[ARDUINO]', '').trim();
    }
    return data;
  };

  const fetchStatus = async () => {
    try {
      const state = await NetInfo.fetch();
      if (!state.isConnected) {
        setStatusMessage('Sem conexão com a internet/Wi-Fi.');
        setStatusColor('gray');
        return;
      }

      const response = await fetch(`${NODEMCU_IP}/STATUS`);
      const data = await response.text();

      if (data.includes('[ARDUINO]')) {
        if (data.includes('STATE:ON')) {
          setStatusMessage('🤖 Conexão com servidor NODEMCU estabelecida.\n✅ Led ligado\n' + data.replace('[ARDUINO]', '').trim());
          setStatusColor('green');
        } else if (data.includes('STATE:OFF')) {
          setStatusMessage('🤖 Conexão com servidor NODEMCU estabelecida.\n❌ Led desligado\n' + data.replace('[ARDUINO]', '').trim());
          setStatusColor('red');
        } else {
          setStatusMessage(formatMessage(data));
          setStatusColor('gray');
        }
      } else {
        setStatusMessage('🔄 Status desconhecido: ' + data);
        setStatusColor('gray');
      }
    } catch (error) {
      setStatusMessage('Erro ao conectar: ' + error.message);
      setStatusColor('red');
    }
  };

  const fetchDiagnoses = async () => {
    try {
      const response = await fetch(`${NODEMCU_IP}/DIAGNOSES`);
      const data = await response.text();
      setDiagnosesMessage(formatMessage(data) || 'Nenhum diagnóstico disponível.');
    } catch (error) {
      setDiagnosesMessage('Erro ao obter diagnósticos: ' + error.message);
    }
  };

  const fetchBlocked = async () => {
    try {
      const response = await fetch(`${NODEMCU_IP}/BLOCKED`);
      const data = await response.text();
      setBlockedMessage(formatMessage(data) || 'Nenhum bloqueio ativo.');
    } catch (error) {
      setBlockedMessage('Erro ao obter bloqueios: ' + error.message);
    }
  };

  const fetchWire = async () => {
    try {
      const response = await fetch(`${NODEMCU_IP}/I2C`);
      const data = await response.text();
      setWireMessage(formatMessage(data) || 'Nenhum dado I2C disponível.');
    } catch (error) {
      setWireMessage('Erro ao obter dados I2C: ' + error.message);
    }
  };

  const sendCommand = (cmd) => {
    setIsSendingCommand(true);
    fetch(`${NODEMCU_IP}/${cmd}`)
      .then((res) => res.text())
      .then((data) => {
        if (data.includes('[ARDUINO]')) {
          setStatusMessage(`♾️ Conexão com servidor NODEMCU estabelecida.\n📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data.replace('[ARDUINO]', '').trim()}`);
        } else {
          setStatusMessage(`📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${data}`);
        }
        fetchStatus();
      })
      .catch((error) => {
        setStatusMessage(`Erro ao enviar comando ${cmd}: ` + error.message);
        setStatusColor('red');
      })
      .finally(() => setIsSendingCommand(false));
  };

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

  const StatusRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingStatus}
          onRefresh={async () => {
            setRefreshingStatus(true);
            await fetchStatus();
            setRefreshingStatus(false);
          }}
        />
      }
    >
      {refreshingStatus && <ActivityIndicator animating size="small" />}
      <Text style={[styles.statusText, { color: statusColor }]}>{statusMessage}</Text>
    </ScrollView>
  );

  const ControleRoute = () => (
    <ScrollView
      contentContainerStyle={styles.tabContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingControle}
          onRefresh={async () => {
            setRefreshingControle(true);
            await fetchStatus();
            setRefreshingControle(false);
          }}
        />
      }
    >
      {refreshingControle && <ActivityIndicator animating size="small" />}
      <Button
        mode="contained"
        onPress={() => sendCommand('LIGAR')}
        disabled={isSendingCommand}
        style={[styles.button, { backgroundColor: 'green' }]}
      >
        {isSendingCommand ? 'Enviando...' : 'LIGAR'}
      </Button>
      <Button
        mode="contained"
        onPress={() => sendCommand('DESLIGAR')}
        disabled={isSendingCommand}
        style={[styles.button, { backgroundColor: 'red' }]}
      >
        {isSendingCommand ? 'Enviando...' : 'DESLIGAR'}
      </Button>
    </ScrollView>
  );

  const DiagnosesRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingDiagnoses}
          onRefresh={async () => {
            setRefreshingDiagnoses(true);
            await fetchDiagnoses();
            setRefreshingDiagnoses(false);
          }}
        />
      }
    >
      {refreshingDiagnoses && <ActivityIndicator animating size="small" />}
      <Text style={styles.logsText}>{diagnosesMessage}</Text>
      <Button mode="outlined" onPress={fetchDiagnoses} style={styles.refreshButton}>
        Atualizar Diagnósticos
      </Button>
    </ScrollView>
  );

  const BlockedRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingBlocked}
          onRefresh={async () => {
            setRefreshingBlocked(true);
            await fetchBlocked();
            setRefreshingBlocked(false);
          }}
        />
      }
    >
      {refreshingBlocked && <ActivityIndicator animating size="small" />}
      <Text style={styles.logsText}>{blockedMessage}</Text>
      <Button mode="outlined" onPress={fetchBlocked} style={styles.refreshButton}>
        Atualizar Bloqueios
      </Button>
    </ScrollView>
  );

  const WireRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingWire}
          onRefresh={async () => {
            setRefreshingWire(true);
            await fetchWire();
            setRefreshingWire(false);
          }}
        />
      }
    >
      {refreshingWire && <ActivityIndicator animating size="small" />}
      <Text style={styles.logsText}>{wireMessage}</Text>
      <Button mode="outlined" onPress={fetchWire} style={styles.refreshButton}>
        Atualizar Dados I2C
      </Button>
    </ScrollView>
  );

  const renderScene = ({ route }) => {
    switch (route.key) {
      case 'status':
        return <StatusRoute />;
      case 'controle':
        return <ControleRoute />;
      case 'diagnoses':
        return <DiagnosesRoute />;
      case 'blocked':
        return <BlockedRoute />;
      case 'wire':
        return <WireRoute />;
      default:
        return null;
    }
  };

  return (
    <PaperProvider>
      <TabView
        navigationState={{ index, routes }}
        renderScene={renderScene}
        onIndexChange={setIndex}
        initialLayout={{ width: Dimensions.get('window').width }}
        renderTabBar={(props) => (
          <TabBar
            {...props}
            indicatorStyle={{ backgroundColor: 'blue' }}
            style={{ backgroundColor: 'white' }}
            labelStyle={{ color: 'black' }}
          />
        )}
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
    marginBottom: 10,
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