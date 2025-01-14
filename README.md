# Projeto MedSync

O **MedSync** é um sistema de gerenciamento de pacientes e prescrições médicas, dividido em duas partes:
- **Interface Web (Django):** Voltada para farmacêuticos gerenciarem pacientes e criarem prescrições.
- **Aplicativo Mobile (React Native):** Voltado para pacientes visualizarem suas prescrições.

---

## Requisitos

### Ferramentas Necessárias
1. **Python 3.10+**
2. **PostgreSQL**
3. **Node.js 16+ e npm**
4. **Expo CLI**

---

## Configuração do Backend (Django)

1. **Clone o repositório**:

   ```bash
   git clone https://github.com/Agnegring089/MedSync.git
   cd MedSync/backend
   ```

2. **Crie e ative um ambiente virtual**:

   **Linux/MacOS:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

   **Windows:**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Instale as dependências**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure o banco de dados**:
   - Certifique-se de que o PostgreSQL esteja instalado e rodando.
   - Crie um banco de dados.
   - Configure as credenciais no arquivo `backend/settings.py`:
     ```python
     DATABASES = {
         'default': {
             'ENGINE': 'django.db.backends.postgresql',
             'NAME': 'nome_do_banco',
             'USER': 'usuario',
             'PASSWORD': 'senha',
             'HOST': 'localhost',
             'PORT': '5432',
         }
     }
     ```

5. **Aplique as migrações**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Crie um superusuário para acessar o admin**:
   ```bash
   python manage.py createsuperuser
   ```

7. **Inicie o servidor Django**:
   ```bash
   python manage.py runserver
   ```

---

## Configuração do Frontend (React Native)

1. **Acesse o diretório do frontend**:
   ```bash
   cd ../frontend
   ```

2. **Instale as dependências**:
   ```bash
   npm install
   ```

3. **Inicie o servidor Expo**:
   ```bash
   npm start
   ```

4. **Teste o aplicativo**:
   - Escaneie o QR Code gerado pelo Expo no terminal usando o aplicativo Expo Go.

---

## Recomendações

### Usar o ngrok para conexão entre backend e frontend
Se a conexão entre o backend (Django) e o frontend (React Native) não estiver funcionando corretamente, você pode utilizar o [ngrok](https://ngrok.com/) para expor o servidor local do Django a uma URL pública acessível pelo Expo.

1. **Instale o ngrok**:
   - Siga as instruções no site oficial do ngrok para instalar.

2. **Inicie o ngrok no terminal, apontando para a porta do servidor Django (8000)**:
   ```bash
   ngrok http 8000
   ```

3. **Atualize as URLs do frontend para utilizar a URL gerada pelo ngrok**:
   - Substitua `localhost:8000` pela URL gerada pelo ngrok (ex.: `https://abcd1234.ngrok.io`).

4. **Certifique-se de que o backend está acessível pela internet e que o Expo consegue se conectar à URL fornecida**.