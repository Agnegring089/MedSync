import React, { useEffect, useState, useRef } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Alert, Button } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { getPatientDetails } from '../services/api';
import AuthGuard from '../guards/AuthGuard';

const Home: React.FC = ({ navigation }: any) => {
  const [patientData, setPatientData] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<boolean>(false);

  // Flag para evitar múltiplos redirecionamentos
  const hasRedirected = useRef(false);

  useEffect(() => {
    const fetchPatientData = async () => {
      try {
        const token = await AsyncStorage.getItem('access_token');
        if (!token) {
          if (!hasRedirected.current) {
            hasRedirected.current = true;
            Alert.alert('Erro', 'Token não encontrado.');
            navigation.navigate('Login');
          }
          return;
        }

        const response = await getPatientDetails(token);
        setPatientData(response.data);
        setError(false);
      } catch (error: any) {
        console.error('Erro ao carregar os dados do paciente:', error);

        if (!hasRedirected.current && (error.response?.status === 401 || error.response?.status === 403)) {
          hasRedirected.current = true;
          Alert.alert('Erro', 'Sessão expirada ou token inválido. Faça login novamente.');
          navigation.navigate('Login');
        }
      } finally {
        setLoading(false);
      }
    };

    fetchPatientData();
  }, [navigation]);

  const handleLogout = async () => {
    try {
      await AsyncStorage.clear(); // Limpa todos os tokens e informações do AsyncStorage
      Alert.alert('Logout', 'Você foi desconectado.');
      navigation.navigate('Login'); // Redireciona para a tela de login
    } catch (error) {
      console.error('Erro ao fazer logout:', error);
      Alert.alert('Erro', 'Não foi possível fazer logout.');
    }
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Carregando dados do paciente...</Text>
      </View>
    );
  }

  return (
    <AuthGuard navigation={navigation}>
      <View style={styles.container}>
        {patientData ? (
          <View>
            <Text style={styles.text}>Nome: {patientData.name}</Text>
            <Text style={styles.text}>CPF: {patientData.cpf}</Text>
            <Text style={styles.text}>Data de Nascimento: {patientData.birth_date}</Text>
            <Text style={styles.text}>
              Status: {patientData.status ? 'Ativo' : 'Inativo'}
            </Text>
            {/* Botão de logout */}
            <Button title="Logout" onPress={handleLogout} />
          </View>
        ) : (
          <Text style={styles.errorText}>Não foi possível carregar os dados.</Text>
        )}
      </View>
    </AuthGuard>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 16,
  },
  text: {
    fontSize: 18,
    marginVertical: 8,
  },
  errorText: {
    color: 'red',
    fontSize: 16,
  },
});

export default Home;
