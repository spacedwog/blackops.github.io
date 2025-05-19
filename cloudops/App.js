import React, { useEffect, useState } from 'react';
import {
  StyleSheet,
  Dimensions,
  ScrollView,
  RefreshControl,
  View,
  Animated,
  TouchableWithoutFeedback,
} from 'react-native';
import {
  Text,
  Button,
  Provider as PaperProvider,
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
    { key: 'status', title: 'Status' },
    { key: 'controle', title: 'Controle' },
    { key: 'diagnoses', title: 'Diagnoses' },
    { key: 'blocked', title: 'Blocked' },
    { key: 'search', title: 'Search' },
    { key: 'client', title: 'Client' },
    { key: 'wire', title: 'Wire' },
  ]);

  const [animation] = useState(new Animated.Value(1));
  const [backgroundImage, setBackgroundImage] = useState(require('./assets/futuristic-bg.jpg'));

  const handleBackgroundPress = () => {
    Animated.sequence([
      Animated.timing(animation, {
        toValue: 0.95,
        duration: 100,
        useNativeDriver: true,
      }),
      Animated.timing(animation, {
        toValue: 1,
        duration: 100,
        useNativeDriver: true,
      }),
    ]).start();
  };

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
        setBackgroundImage(require('./assets/bg-on.jpg'));
      } else if (data.includes('STATE:OFF')) {
        setStatusMessage(`🤖 NODEMCU conectado\n❌ Led desligado\n${data}`);
        setStatusColor('red');
        setBackgroundImage(require('./assets/bg-off.jpg'));
      } else {
        setStatusMessage('🔄 Status desconhecido: ' + data);
        setStatusColor('gray');
        setBackgroundImage(require('./assets/futuristic-bg.jpg'));
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

  const createRefreshableScroll = (refreshing, setRefreshing, fetcher, content) => (
    <ScrollView
      style={styles.scrollContent}
      refreshControl={
        <RefreshControl
          refreshing={refreshing}
          onRefresh={async () => {
            setRefreshing(true);
            await fetcher();
            setRefreshing(false);
          }}
        />
      }
    >
      <TopStatusBanner />
      {content}
    </ScrollView>
  );

  const StatusRoute = () => createRefreshableScroll(refreshingStatus, setRefreshingStatus, fetchStatus, null);

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

  const DiagnosesRoute = () =>
    createRefreshableScroll(refreshingDiagnoses, setRefreshingDiagnoses,
      () => fetchData('DIAGNOSES', setDiagnosesMessage, 'Sem dados'),
      <Text style={styles.logsText}>{diagnosesMessage}</Text>
    );

  const BlockedRoute = () =>
    createRefreshableScroll(refreshingBlocked, setRefreshingBlocked,
      () => fetchData('BLOCKED', setBlockedMessage, 'Sem bloqueios'),
      <Text style={styles.logsText}>{blockedMessage}</Text>
    );

  const SearchRoute = () =>
    createRefreshableScroll(refreshingSearch, setRefreshingSearch,
      () => fetchData('PESQUISA', setSearchMessage, 'Sem dados'),
      <Text style={styles.logsText}>{searchMessage}</Text>
    );

  const ClientRoute = () =>
    createRefreshableScroll(refreshingClient, setRefreshingClient,
      () => fetchData('CLIENTES', setClientMessage, 'Sem dados'),
      <Text style={styles.logsText}>{clientMessage}</Text>
    );

  const WireRoute = () =>
    createRefreshableScroll(refreshingWire, setRefreshingWire,
      () => fetchData('I2C', setWireMessage, 'Sem dados I2C'),
      <Text style={styles.logsText}>{wireMessage}</Text>
    );

  const renderScene = ({ route }) => {
    switch (route.key) {
      case 'status': return <StatusRoute />;
      case 'controle': return <ControleRoute />;
      case 'diagnoses': return <DiagnosesRoute />;
      case 'blocked': return <BlockedRoute />;
      case 'search': return <SearchRoute />;
      case 'client': return <ClientRoute />;
      case 'wire': return <WireRoute />;
      default: return null;
    }
  };

  return (
    <PaperProvider>
      <TouchableWithoutFeedback onPress={handleBackgroundPress}>
        <Animated.ImageBackground
          source={backgroundImage}
          style={[styles.background, { transform: [{ scale: animation }] }]}
          resizeMode="cover"
        >
          <View style={{ flex: 1, backgroundColor: 'rgba(0,0,0,0.6)' }}>
            <TabView
              navigationState={{ index, routes }}
              renderScene={renderScene}
              onIndexChange={setIndex}
              initialLayout={{ width: Dimensions.get('window').width }}
              renderTabBar={(props) => (
                <TabBar
                  {...props}
                  indicatorStyle={{ backgroundColor: '#00ffff' }}
                  style={{ backgroundColor: 'rgba(0,0,0,0.5)' }}
                  labelStyle={{ color: '#00ffff' }}
                />
              )}
            />
          </View>
        </Animated.ImageBackground>
      </TouchableWithoutFeedback>
    </PaperProvider>
  );
}

const styles = StyleSheet.create({
  background: {
    flex: 1,
    width: '100%',
    height: '100%',
  },
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
  button: {
    marginBottom: 10,
    marginVertical: 10,
    width: '70%',
    alignSelf: 'center',
  },
  logsText: {
    fontSize: 16,
    fontFamily: 'monospace',
    color: 'white',
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