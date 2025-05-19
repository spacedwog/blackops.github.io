// App.js
import React, { useEffect, useState } from 'react';
import {
  StyleSheet,
  Dimensions,
  ScrollView,
  RefreshControl,
  View,
} from 'react-native';
import {
  Text,
  Button,
  Provider as PaperProvider,
  ActivityIndicator,
} from 'react-native-paper';
import { TabView, TabBar } from 'react-native-tab-view';
import NetInfo from '@react-native-community/netinfo';

const NODEMCU_IP = 'http://192.168.15.138:8080';

export default function App() {
  const [statusMessage, setStatusMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');
  const [diagnosesMessage, setDiagnosesMessage] = useState('Carregando diagnósticos...');
  const [blockedMessage, setBlockedMessage] = useState('Carregando bloqueios...');
  const [searchMessage, setSearchMessage] = useState('Efetuando Pesquisa...');
  const [clientMessage, setClientMessage] = useState('Carregando lista de client...');
  const [wireMessage, setWireMessage] = useState('Carregando dados I2C...');
  const [isSendingCommand, setIsSendingCommand] = useState(false);

  const [refreshingStatus, setRefreshingStatus] = useState(false);
  const [refreshingControle, setRefreshingControle] = useState(false);
  const [refreshingDiagnoses, setRefreshingDiagnoses] = useState(false);
  const [refreshingBlocked, setRefreshingBlocked] = useState(false);
  const [refreshingSearch, setRefreshingSearch] = useState(false);
  const [refreshingClient, setRefreshingClient] = useState(false);
  const [refreshingWire, setRefreshingWire] = useState(false);

  const [index, setIndex] = useState(0);
  const [routes] = useState([
    { key: 'status', title: 'Sts' },
    { key: 'controle', title: 'Cntr' },
    { key: 'diagnoses', title: 'Diag' },
    { key: 'blocked', title: 'Blck' },
    { key: 'search', title: 'Srch'},
    { key: 'client', title: 'Clnt'},
    { key: 'wire', title: 'Wire' },
  ]);

  // ✅ Função genérica para buscar dados
  const fetchData = async (endpoint, setter, fallbackMsg = '') => {
    try {
      const response = await fetch(`${NODEMCU_IP}/${endpoint}`);
      const data = await response.text();
      setter(data || fallbackMsg);
    } catch (error) {
      setter(`Erro ao obter ${endpoint.toLowerCase()}: ${error.message}`);
    }
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

      if (data.includes('STATE:ON')) {
        setStatusMessage(`🤖 NODEMCU conectado\n✅ Led ligado\n${data}`);
        setStatusColor('green');
      } else if (data.includes('STATE:OFF')) {
        setStatusMessage(`🤖 NODEMCU conectado\n❌ Led desligado\n${data}`);
        setStatusColor('red');
      }
      else {
        setStatusMessage('🔄 Status desconhecido: ' + data);
        setStatusColor('gray');
      }
    } catch (error) {
      setStatusMessage('Erro ao conectar: ' + error.message);
      setStatusColor('red');
    }
  };

  const sendCommand = async (cmd) => {
    setIsSendingCommand(true);
    try {
      const response = await fetch(`${NODEMCU_IP}/${cmd}`);
      const data = await response.text();
      const cleanData = data.replace('[ARDUINO]', '').trim();

      setStatusMessage(
        `📤 Comando ${cmd.toUpperCase()} enviado\n📥 Resposta: ${cleanData}`
      );
      fetchStatus();
    } catch (error) {
      setStatusMessage(`Erro ao enviar comando ${cmd}: ` + error.message);
      setStatusColor('red');
    } finally {
      setIsSendingCommand(false);
    }
  };

  // ✅ Atualização automática com espaçamento entre chamadas
  useEffect(() => {
    fetchStatus();
    fetchData('DIAGNOSES', setDiagnosesMessage, 'Nenhum diagnóstico disponível.');
    fetchData('BLOCKED', setBlockedMessage, 'Nenhum bloqueio ativo.');

    const interval = setInterval(() => {
      fetchStatus();
      setTimeout(() => fetchData('DIAGNOSES', setDiagnosesMessage, 'Sem diagnóstico'), 1000);
      setTimeout(() => fetchData('BLOCKED', setBlockedMessage, 'Sem bloqueios'), 2000);
    }, 15000);

    return () => clearInterval(interval);
  }, []);

  const TopStatusBanner = () => (
    <View style={[styles.topBanner, { backgroundColor: statusColor }]}>
      <Text style={styles.bannerText}>{statusMessage}</Text>
    </View>
  );

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
      <TopStatusBanner />
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
      <TopStatusBanner />
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
            await fetchData('DIAGNOSES', setDiagnosesMessage, 'Sem dados');
            setRefreshingDiagnoses(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      <Text style={styles.logsText}>{diagnosesMessage}</Text>
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
            await fetchData('BLOCKED', setBlockedMessage, 'Sem bloqueios');
            setRefreshingBlocked(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      <Text style={styles.logsText}>{blockedMessage}</Text>
    </ScrollView>
  );

  const SearchRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingSearch}
          onRefresh={async () => {
            setRefreshingSearch(true);
            await fetchData('PESQUISA', setSearchMessage, 'Sem dados');
            setRefreshingSearch(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      <Text style={styles.logsText}>{searchMessage}</Text>
    </ScrollView>
  );

  const ClientRoute = () => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshingClient}
          onRefresh={async () => {
            setRefreshingClient(true);
            await fetchData('CLIENTES', setClientMessage, 'Sem dados');
            setRefreshingClient(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      <Text style={styles.logsText}>{clientMessage}</Text>
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
            await fetchData('I2C', setWireMessage, 'Sem dados I2C');
            setRefreshingWire(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      <Text style={styles.logsText}>{wireMessage}</Text>
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
      case 'search':
        return <SearchRoute />;
      case 'client':
        return <ClientRoute />;
      case 'wire':
        return <WireRoute />;
      default:
        return null;
    }
  };

  return (
    <PaperProvider>
      <View style={{ flex: 1 }}>
        <TabView
          navigationState={{ index, routes }}
          renderScene={renderScene}
          onIndexChange={setIndex}
          initialLayout={{ width: Dimensions.get('window').width }}
          renderTabBar={(props) => (
            <TabBar
              {...props}
              indicatorStyle={{ backgroundColor: 'blue' }}
              style={{ backgroundColor: 'blue' }}
              labelStyle={{ color: 'black' }}
            />
          )}
          tabBarPosition="bottom" // <- Adicione isso aqui
        />
      </View>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  tabContent: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: 10,
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
  topBanner: {
    padding: 10,
    marginBottom: 10,
    borderRadius: 5,
  },
  bannerText: {
    color: 'white',
    fontWeight: 'bold',
    textAlign: 'center',
  },
});