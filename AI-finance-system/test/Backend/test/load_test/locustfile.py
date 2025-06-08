from locust import HttpUser, task, between
import json
import random

class FinanceSystemUser(HttpUser):
    wait_time = between(1, 3)  # Tiempo de espera entre peticiones
    
    # Datos de prueba para Juan Pérez
    valid_credentials = {
        "email": "juan.perez@example.com",
        "password": "123456"  # Ajustar según el hash real
    }
    
    @task(5)  # Mayor peso a login (5:1)
    def login(self):
        """Prueba de carga para el endpoint de login"""
        response = self.client.post(
            "/api/auth/login",
            json=self.valid_credentials,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            self.token = response.json().get("token")
    
    @task(1)
    def register(self):
        """Prueba de carga para registro de usuarios"""
        user_id = random.randint(1000, 9999)
        new_user = {
            "email": f"test_user_{user_id}@example.com",
            "password": f"Test@Pass{user_id}",
            "first_name": f"Test{user_id}",
            "last_name": "User",
            "birth_date": "1990-01-01",
            "phone": f"+54911{random.randint(1000000, 9999999)}"
        }
        
        self.client.post(
            "/api/auth/register",
            json=new_user,
            headers={"Content-Type": "application/json"}
        )
    
    @task(3)  # Prueba de endpoints protegidos
    def get_financial_data(self):
        """Prueba de carga para endpoints que requieren autenticación"""
        if hasattr(self, 'token'):
            self.client.get(
                "/api/finance/data",
                headers={
                    "Authorization": f"Bearer {self.token}",
                    "Content-Type": "application/json"
                }
            )
    
    @task(2)  # Prueba de IA
    def analyze_with_ai(self):
        """Prueba de carga para el módulo de IA"""
        test_data = {
            "income": random.randint(1000, 5000),
            "expenses": random.randint(500, 4500),
            "savings": random.randint(0, 2000),
            "timestamp": "2023-01-01"
        }
        
        self.client.post(
            "/api/ia/process",
            json=test_data,
            headers={"Content-Type": "application/json"}
        )