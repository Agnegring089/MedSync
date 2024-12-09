import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, Alert } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface AuthGuardProps {
  children: React.ReactNode;
  navigation: any;
}

const AuthGuard = ({ children, navigation }: AuthGuardProps) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);
  const [hasRedirected, setHasRedirected] = useState(false); // Evita múltiplos redirecionamentos

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const token = await AsyncStorage.getItem('access_token');
        if (token) {
          setIsAuthenticated(true);
        } else {
          setIsAuthenticated(false);
        }
      } catch (error) {
        console.error('Erro ao verificar autenticação:', error);
        Alert.alert('Erro', 'Erro ao verificar autenticação. Tente novamente.');
        setIsAuthenticated(false);
      }
    };

    checkAuth();
  }, []);

  useEffect(() => {
    if (isAuthenticated === false && !hasRedirected) {
      setHasRedirected(true); // Marca que o redirecionamento foi realizado
      navigation.navigate('Login');
    }
  }, [isAuthenticated, hasRedirected, navigation]);

  if (isAuthenticated === null) {
    // Mostra um indicador de carregamento enquanto verifica a autenticação
    return (
      <View style={{ flex: 1, justifyContent: 'center', alignItems: 'center' }}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Verificando autenticação...</Text>
      </View>
    );
  }

  return <>{isAuthenticated ? children : null}</>;
};

export default AuthGuard;
