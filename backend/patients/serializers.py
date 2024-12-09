#def create(self, validated_data):
#    email = validated_data.pop('email')
#    password = validated_data.pop('password')
#    cpf = validated_data.pop('cpf')

#    user = User.objects.create_user(username=cpf, email=email, password=password)
#    patient = Patient.objects.create(user=user, cpf=cpf, approved=False, **validated_data)
#    return patient