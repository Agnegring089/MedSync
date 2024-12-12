import React, { useEffect, useState } from 'react';
import { View, Text, StyleSheet, ActivityIndicator, Alert, ScrollView } from 'react-native';
import api from '../services/api';

interface PatientData {
  name: string;
  cpf: string;
  birth_date: string;
  status: boolean;
  prescriptions: Prescription[];
}

interface Prescription {
  id: number;
  date: string;
  doctor_name: string;
  medications: Medication[];
}

interface Medication {
  name: string;
  dose: string;
  quantity: number;
  frequency: string;
  duration_days: number;
  medication_type: string;
}

const Home: React.FC = () => {
  const [patientData, setPatientData] = useState<PatientData | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const fetchPatientData = async () => {
    try {
      const response = await api.get('/me/');
      setPatientData(response.data);
      setError(null);
    } catch (error) {
      console.error('Erro ao carregar os dados do paciente:', error);
      setError('Erro ao carregar os dados. Tente novamente.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    setLoading(true);
    fetchPatientData();
  }, []);

  if (loading) {
    return (
      <View style={styles.container}>
        <ActivityIndicator size="large" color="#0000ff" />
        <Text>Carregando dados...</Text>
      </View>
    );
  }

  if (error) {
    return (
      <View style={styles.container}>
        <Text style={styles.errorText}>{error}</Text>
      </View>
    );
  }

  return (
    <ScrollView style={styles.scrollContainer}>
      <View style={styles.container}>
        {patientData && (
          <>
            <Text style={styles.sectionTitle}>Informações do Paciente</Text>
            <Text style={styles.text}>Nome: {patientData.name}</Text>
            <Text style={styles.text}>CPF: {patientData.cpf}</Text>
            <Text style={styles.text}>Data de Nascimento: {patientData.birth_date}</Text>
            <Text style={styles.text}>
              Status: {patientData.status ? 'Ativo' : 'Inativo'}
            </Text>

            <Text style={styles.sectionTitle}>Prescrições</Text>
            {patientData.prescriptions.length > 0 ? (
              patientData.prescriptions.map((prescription) => (
                <View key={prescription.id} style={styles.prescriptionContainer}>
                  <Text style={styles.prescriptionText}>
                    Data: {prescription.date}
                  </Text>
                  <Text style={styles.prescriptionText}>
                    Médico: {prescription.doctor_name}
                  </Text>
                  <Text style={styles.sectionSubtitle}>Medicamentos:</Text>
                  {prescription.medications.map((medication, index) => (
                    <View key={index} style={styles.medicationContainer}>
                      <Text style={styles.medicationText}>
                        Nome: {medication.name}
                      </Text>
                      <Text style={styles.medicationText}>
                        Dose: {medication.dose}
                      </Text>
                      <Text style={styles.medicationText}>
                        Quantidade: {medication.quantity}
                      </Text>
                      <Text style={styles.medicationText}>
                        Frequência: {medication.frequency} vezes ao dia
                      </Text>
                      <Text style={styles.medicationText}>
                        Duração: {medication.duration_days} dias
                      </Text>
                      <Text style={styles.medicationText}>
                        Tipo: {medication.medication_type}
                      </Text>
                    </View>
                  ))}
                </View>
              ))
            ) : (
              <Text style={styles.errorText}>Nenhuma prescrição encontrada.</Text>
            )}
          </>
        )}
      </View>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  scrollContainer: {
    flex: 1,
    backgroundColor: '#fff',
  },
  container: {
    flex: 1,
    alignItems: 'center',
    padding: 16,
  },
  sectionTitle: {
    fontSize: 20,
    fontWeight: 'bold',
    marginVertical: 12,
    textAlign: 'center',
  },
  sectionSubtitle: {
    fontSize: 18,
    fontWeight: '600',
    marginVertical: 8,
  },
  text: {
    fontSize: 16,
    marginBottom: 8,
  },
  prescriptionContainer: {
    marginBottom: 16,
    padding: 16,
    borderWidth: 1,
    borderColor: '#ddd',
    borderRadius: 8,
    width: '100%',
  },
  prescriptionText: {
    fontSize: 16,
    marginBottom: 4,
  },
  medicationContainer: {
    marginBottom: 8,
    paddingLeft: 8,
  },
  medicationText: {
    fontSize: 14,
    marginBottom: 2,
  },
  errorText: {
    color: 'red',
    fontSize: 16,
    marginBottom: 8,
  },
});

export default Home;
