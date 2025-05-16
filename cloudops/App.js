import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View, Button } from 'react-native';
import { StatusBar } from 'expo-status-bar';

// IP do NodeMCU (ajuste conforme necessário)
const NODEMCU_IP = 'http://192.168.15.8:8080';

export default function App() {
  const [message, setMessage] = useState('Conectando ao NodeMCU...');
  const [statusColor, setStatusColor] = useState('orange');

  // Verifica o status do relé
  const fetchStatus = () => {
    fetch(`${NODEMCU_IP}/STATUS`)
      .then(res => res.text())
      .then(data => {
        if(data.startsWith("[JAVA]")){
          setMessage("Conectado com o NodeMCU");
          if (data.match('STATE:ON')) {
            setMessage("✅ Relé ligado (NodeMCU)");
            setStatusColor("green");
          } else if (data.match('STATE:OFF')) {
            setMessage("⚠️ Relé desligado (NodeMCU)");
            setStatusColor("red");
          }
        }
        else {
          setMessage("🔄 Status desconhecido: " + data);
          setStatusColor("gray");
        }
      })
      .catch(error => {
        setMessage("Erro ao conectar ao NodeMCU: " + error.message);
        setStatusColor("red");
      });
  };

  // Envia comandos para o relé
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

  useEffect(() => {
    fetchStatus();
    const interval = setInterval(fetchStatus, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <View style={styles.container}>
      <Text style={[styles.statusText, { color: statusColor }]}>{message}</Text>

      <View style={styles.buttonContainer}>
        <Button title="LIGAR" color="green" onPress={() => sendCommand('LIGAR')} />
        <Button title="DESLIGAR" color="red" onPress={() => sendCommand('DESLIGAR')} />
      </View>

      <StatusBar style="auto" />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  statusText: {
    fontSize: 18,
    textAlign: 'center',
    marginBottom: 30,
    marginHorizontal: 20,
  },
  buttonContainer: {
    flexDirection: 'row',
    gap: 20,
  },
});