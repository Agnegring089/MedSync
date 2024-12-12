import React, { useState, useEffect } from 'react';
import { View, Text, TextInput, Button, StyleSheet, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import api from '../services/api';

const Login: React.FC = ({ navigation }: any) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState<boolean>(false);

  // Verifica se há um token válido ao carregar a tela
  useEffect(() => {
    const checkAuth = async () => {
      const token = await AsyncStorage.getItem('access_token');
      if (token) {
        try {
          // Verifica se o token ainda é válido
          const response = await api.get('/me/', {
            headers: {
              Authorization: `Bearer ${token}`,
            },
          });

          if (response.status === 200) {
            navigation.navigate('Home');
          }
        } catch (error) {
          console.error('Token inválido ou expirado:', error);
          await AsyncStorage.clear(); // Limpa tokens inválidos
        }
      }
    };
    checkAuth();
  }, [navigation]);

  // Função para realizar o login
  const handleLogin = async () => {
    if (!username || !password) {
      Alert.alert('Erro', 'Por favor, preencha todos os campos.');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/login/', { username, password });
      const { access, refresh } = response.data;

      // Salva os tokens no AsyncStorage
      await AsyncStorage.setItem('access_token', access);
      await AsyncStorage.setItem('refresh_token', refresh);

      Alert.alert('Bem-vindo', 'Login realizado com sucesso.');
      navigation.navigate('Home');
    } catch (error: any) {
      console.error('Erro ao fazer login:', error);
      if (error.response && error.response.status === 401) {
        Alert.alert('Erro', 'Credenciais inválidas.');
      } else {
        Alert.alert('Erro', 'Não foi possível alcançar o servidor.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>Login</Text>
      <TextInput
        style={styles.input}
        placeholder="Usuário"
        value={username}
        onChangeText={setUsername}
        autoCapitalize="none"
      />
      <TextInput
        style={styles.input}
        placeholder="Senha"
        secureTextEntry
        value={password}
        onChangeText={setPassword}
        autoCapitalize="none"
      />
      <Button
        title={loading ? 'Entrando...' : 'Entrar'}
        onPress={handleLogin}
        disabled={loading}
      />
      <Button
        title="Cadastre-se"
        onPress={() => navigation.navigate('Register')}
        color="gray"
      />
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    padding: 16,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 16,
    textAlign: 'center',
  },
  input: {
    height: 40,
    borderColor: 'gray',
    borderWidth: 1,
    marginBottom: 12,
    paddingHorizontal: 8,
    borderRadius: 5,
  },
});

export default Login;
