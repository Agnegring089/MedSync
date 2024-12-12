import axios from 'axios';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Configuração do Axios
const api = axios.create({
  baseURL: 'https://lucky-crawdad-factual.ngrok-free.app/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Interceptadores para debug
api.interceptors.request.use(request => {
  console.log('Iniciando Requisição:', request);
  return request;
});

api.interceptors.response.use(
  response => {
    console.log('Resposta Recebida:', response);
    return response;
  },
  error => {
    console.log('Erro na Requisição:', error.response || error.message);
    return Promise.reject(error);
  }
);

export default api;

// Exemplo de funções
export const loginPatient = async (data: { username: string; password: string }) => {
  return api.post('/login/', data);
};
