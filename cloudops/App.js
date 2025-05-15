import React, { useEffect, useState } from 'react';
import { Button, StyleSheet, Text, View } from 'react-native';
import * as AuthSession from 'expo-auth-session';
import { StatusBar } from 'expo-status-bar';

// Dados do seu GitHub App
const CLIENT_ID = 'Iv23lir3gWXCKZ170nzC';
const REDIRECT_URI = AuthSession.makeRedirectUri(); // redirecionamento seguro

const discovery = {
  authorizationEndpoint: 'https://github.com/login/oauth/authorize',
  tokenEndpoint: 'https://github.com/login/oauth/access_token',
};

export default function App() {
  const [message, setMessage] = useState('Conectando...');
  const [userInfo, setUserInfo] = useState(null);

  const handleOAuthLogin = async () => {
    const authUrl = `${discovery.authorizationEndpoint}?client_id=${CLIENT_ID}&scope=read:user`;

    const result = await AuthSession.startAsync({ authUrl });

    if (result.type === 'success') {
      const { code } = result.params;

      // Envia o código para seu backend para trocar pelo access_token
      const tokenResponse = await fetch('http://192.168.15.8:8080/github/token', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      });

      const { access_token } = await tokenResponse.json();

      // Usa o token para acessar a API do GitHub
      const userResponse = await fetch('https://api.github.com/user', {
        headers: { Authorization: `token ${access_token}` },
      });
      const user = await userResponse.json();
      setUserInfo(user);
      setMessage(`Bem-vindo, ${user.login}`);
    } else {
      setMessage('Autenticação cancelada');
    }
  };

  useEffect(() => {
    fetch('http://192.168.15.8:8080/STATUS')
      .then(res => res.text())
      .then(data => {
        if (data.startsWith('[JAVA]')) {
          setMessage('Conexão com o JAVA estabelecida');
        }
      })
      .catch(error => {
        setMessage('Erro ao conectar: ' + error.message);
      });
  }, []);

  return (
    <View style={styles.container}>
      <Text>{message}</Text>
      {userInfo && <Text>ID GitHub: {userInfo.id}</Text>}
      <Button title="Entrar com GitHub" onPress={handleOAuthLogin} />
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