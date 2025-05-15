import React, { useEffect, useState } from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { StatusBar } from 'expo-status-bar';

export default function App() {
  const [message, setMessage] = useState('Conectando...');

  useEffect(() => {
    fetch('http://192.168.15.8:8080/STATUS')
      .then(res => res.text()) // <== texto, não JSON
      .then(data => {
        setMessage(data);
      })
      .catch(error => {
        setMessage('Erro ao conectar: ' + error.message);
      });
  }, []);

  return (
    <View style={styles.container}>
      <Text>{message}</Text>
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
});