# Documentación de Pruebas - Lógica Core

## Módulo de pruebas

- Archivo principal: `test/core/test_main.py`

## Objetivos

- Validar funciones y endpoints principales.
- Verificar manejo correcto de errores.
- Comprobar integridad de datos.

## Registro de pruebas

# Pruebas Unitarias - Sistema de Autenticación

## Archivo: `test_main.py`
**Ubicación:** `tests/backend/core/test_main.py`

## Objetivo
Verificar el correcto funcionamiento del sistema de autenticación (login y registro) mediante pruebas automatizadas.

## Estructura del Test

```python
import unittest
from unittest.mock import patch, MagicMock
import json
from datetime import datetime
import sys
import os

# Añadir el directorio principal al path para las importaciones
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..')))

# Importaciones específicas (ajusta según tu estructura real)
from app import create_app  # Importa tu aplicación Flask/FastAPI
from models.user import User  # Importa tu modelo de usuario
from database import db  # Importa tu instancia de base de datos

class TestAuthSystem(unittest.TestCase):
    def setUp(self):
        """Configuración inicial para cada test"""
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # Usamos DB en memoria para pruebas
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Insertar usuario de prueba (Juan Pérez)
            test_user = User(
                email='juan.perez@example.com',
                password_hash='$2a$10$8vZP5uVz7J3tYd4q9XrB0e.9mZ1lLk2Nf3pDo7sQhGvY6W1cXyHjK',
                first_name='Juan',
                last_name='Pérez',
                birth_date=datetime.strptime('1985-07-15', '%Y-%m-%d').date(),
                phone='+5491145678901',
                created_at=datetime.strptime('2023-01-15 09:30:00', '%Y-%m-%d %H:%M:%S'),
                is_active=True,
                avatar_url='https://ejemplo.com/avatars/juanperez.jpg'
            )
            db.session.add(test_user)
            db.session.commit()

    def tearDown(self):
        """Limpieza después de cada test"""
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_successful_login(self):
        """Test para login exitoso con las credenciales de Juan Pérez"""
        # Datos de login válidos (ajusta la contraseña según lo que espera tu sistema)
        response = self.client.post('/login', json={
            'email': 'juan.perez@example.com',
            'password': '123456'  # Sustituye por la contraseña real que corresponde al hash
        })
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('access_token', response.json)
        self.assertIn('user', response.json)
        self.assertEqual(response.json['user']['email'], 'juan.perez@example.com')

    def test_invalid_password(self):
        """Test para contraseña incorrecta"""
        response = self.client.post('/login', json={
            'email': 'juan.perez@example.com',
            'password': 'contrasena_incorrecta'
        })
        
        self.assertEqual(response.status_code, 401)
        self.assertIn('error', response.json)

    def test_nonexistent_user(self):
        """Test para usuario no existente"""
        response = self.client.post('/login', json={
            'email': 'no.existe@example.com',
            'password': 'alguna_contrasena'
        })
        
        self.assertEqual(response.status_code, 404)
        self.assertIn('error', response.json)

    @patch('services.auth.send_welcome_email')
    def test_user_registration(self, mock_email):
        """Test para registro de nuevo usuario"""
        mock_email.return_value = True
        
        new_user = {
            'email': 'nuevo.usuario@example.com',
            'password': 'NuevaContrasena123!',
            'first_name': 'Ana',
            'last_name': 'Gómez',
            'birth_date': '1990-05-20',
            'phone': '+5491187654321'
        }
        
        response = self.client.post('/register', json=new_user)
        
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', response.json)
        
        # Verificar que el usuario existe en la base de datos
        with self.app.app_context():
            user = User.query.filter_by(email='nuevo.usuario@example.com').first()
            self.assertIsNotNone(user)
            self.assertEqual(user.first_name, 'Ana')

if __name__ == '__main__':
    unittest.main()
```

Configuración Inicial

    setUp():

        Crea una aplicación Flask/FastAPI en modo testing

        Configura una base de datos SQLite en memoria

        Inserta el usuario de prueba "Juan Pérez"

    tearDown():

        Limpia la base de datos después de cada test

Casos de Prueba Implementados
1. Login Exitoso
python

def test_successful_login(self):
    # Prueba el login con credenciales válidas
    # Verifica:
    # - Código de respuesta 200
    # - Presencia de access_token
    # - Datos correctos del usuario

2. Login con Credenciales Inválidas
python

def test_invalid_password(self):
    # Prueba el login con contraseña incorrecta
    # Verifica:
    # - Código de error 401
    # - Mensaje de error

3. Usuario Inexistente
python

def test_nonexistent_user(self):
    # Prueba login con usuario no registrado
    # Verifica:
    # - Código de error 404
    # - Mensaje de error

4. Registro de Usuario
python

@patch('services.main.send_welcome_email')
def test_user_registration(self, mock_email):
    # Prueba el registro de nuevos usuarios
    # Verifica:
    # - Código de éxito 201
    # - Creación en base de datos
    # - Mock del servicio de email

Datos de Prueba

Usuario base para pruebas:
python

{
    "email": "juan.perez@example.com",
    "password_hash": "$2a$10$8vZP5uVz7J3tYd4q9XrB0e...",
    "first_name": "Juan",
    "last_name": "Pérez",
    # ... (otros campos)
}

Requisitos para Ejecución

    Dependencias:
    bash

pip install unittest2 pytest flask-sqlalchemy

Variables de entorno:

    TESTING=True
    DATABASE_URI=sqlite:///:memory:

Ejecución
bash

# Ejecutar todas las pruebas
python -m pytest tests/backend/core/test_main.py -v

# Ejecutar prueba específica
python -m pytest tests/backend/core/test_main.py::TestMainSystem::test_successful_login -v