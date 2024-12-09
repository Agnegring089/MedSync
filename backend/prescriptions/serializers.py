from rest_framework import serializers
from .models import Prescription, Medication

class MedicationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Medication
        fields = '__all__'

    def validate(self, data):
        medication_type = data.get('medication_type')
        quantity = data.get('quantity')

        if medication_type == 'capsule' and (quantity < 1 or quantity > 1000):
            raise serializers.ValidationError("A quantidade de comprimidos/cápsulas deve estar entre 1 e 1000.")
        if medication_type == 'liquid' and (quantity < 1 or quantity > 1000):
            raise serializers.ValidationError("A quantidade de líquido (ml/gotas) deve estar entre 1 e 1000.")
        if medication_type == 'injectable' and (quantity < 1 or quantity > 100):
            raise serializers.ValidationError("A quantidade de injetáveis deve estar entre 1 e 100.")

        return data

class PrescriptionSerializer(serializers.ModelSerializer):
    medications = MedicationSerializer(many=True)

    class Meta:
        model = Prescription
        fields = '__all__'

    def create(self, validated_data):
        medications_data = validated_data.pop('medications')
        prescription = Prescription.objects.create(**validated_data)
        for medication_data in medications_data:
            Medication.objects.create(prescription=prescription, **medication_data)
        return prescription
