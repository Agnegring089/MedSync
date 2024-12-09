import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configuração da instância Axios
const api = axios.create({
  baseURL: 'https://lucky-crawdad-factual.ngrok-free.app/api/',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Função para renovar o token
const refreshAccessToken = async () => {
  try {
    const refreshToken = await AsyncStorage.getItem('refresh_token');
    if (!refreshToken) throw new Error('Refresh token não encontrado');

    const response = await api.post('/token/refresh/', { refresh: refreshToken });
    const { access } = response.data;

    await AsyncStorage.setItem('access_token', access);
    api.defaults.headers.common['Authorization'] = `Bearer ${access}`;
    return access;
  } catch (error) {
    console.error('Erro ao renovar o token:', error);
    throw error;
  }
};

// Interceptador para lidar com erros 401
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config;

    // Ignorar requisições de login ou se o erro não for 401
    if (originalRequest.url.includes('/login/') || error.response?.status !== 401) {
      return Promise.reject(error);
    }

    try {
      console.log('Tentando renovar o token...');
      await refreshAccessToken();

      // Repetir a requisição original após a renovação do token
      originalRequest.headers['Authorization'] = `Bearer ${await AsyncStorage.getItem('access_token')}`;
      return api.request(originalRequest);
    } catch (tokenError) {
      console.error('Falha ao renovar o token. Redirecionando para login.');
      AsyncStorage.clear(); // Limpa os tokens se a renovação falhar
      throw tokenError;
    }
  }
);

export default api;

// Funções de exemplo já existentes
export const loginPatient = async (data: { username: string; password: string }) => {
  return api.post('/login/', data);
};

export const getPatientDetails = async (token: string): Promise<any> => {
  return api.get('/me/', {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
};
