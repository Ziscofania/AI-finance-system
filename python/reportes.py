import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from datetime import datetime, timedelta

class FinancialAdvisorAI:
    def __init__(self, user_data):
        """
        Inicializa el asesor financiero con los datos del usuario
        
        Args:
            user_data (dict): Diccionario con los datos financieros del usuario
                Ejemplo:
                {
                    'monthly_income': 3200,
                    'monthly_expenses': 2800,
                    'savings': 5000,
                    'debts': 1500,
                    'financial_goals': {
                        'short_term': {'target': 5000, 'timeframe': 12},
                        'medium_term': {'target': 30000, 'timeframe': 60},
                        'long_term': {'target': 250000, 'timeframe': 240}
                    },
                    'transaction_history': [
                        {'date': '2023-01-15', 'amount': -85.50, 'category': 'alimentos'},
                        {'date': '2023-01-20', 'amount': -45.00, 'category': 'transporte'},
                        # ... más transacciones
                    ]
                }
        """
        self.user_data = user_data
        self.strategy = 'moderate'  # Por defecto
        
    def set_strategy(self, strategy):
        """
        Establece la estrategia de inversión
        
        Args:
            strategy (str): 'conservative', 'moderate' o 'aggressive'
        """
        valid_strategies = ['conservative', 'moderate', 'aggressive']
        if strategy not in valid_strategies:
            raise ValueError(f"Estrategia debe ser una de: {valid_strategies}")
        self.strategy = strategy
    
    def analyze_spending(self):
        """Analiza los patrones de gasto del usuario"""
        if not self.user_data.get('transaction_history'):
            return None
            
        df = pd.DataFrame(self.user_data['transaction_history'])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        
        # Gastos por categoría
        expenses_by_category = df[df['amount'] < 0].groupby('category')['amount'].sum().sort_values()
        
        # Gastos mensuales promedio
        monthly_expenses = df[df['amount'] < 0].groupby('month')['amount'].sum().mean()
        
        return {
            'top_spending_categories': expenses_by_category.head(3).to_dict(),
            'monthly_expenses_avg': round(abs(monthly_expenses), 2)
        }
    
    def predict_future_savings(self, months=12):
        """Predice el ahorro futuro basado en el comportamiento actual"""
        current_savings = self.user_data.get('savings', 0)
        monthly_saving = self.user_data['monthly_income'] - self.user_data['monthly_expenses']
        
        if monthly_saving <= 0:
            return {
                'projection': 'negative',
                'message': 'Tus gastos superan tus ingresos. Necesitas reducir gastos o aumentar ingresos.'
            }
        
        # Proyección lineal simple
        months_arr = np.array(range(1, months+1)).reshape(-1, 1)
        savings = current_savings + (monthly_saving * months_arr)
        
        return {
            'projection': 'positive',
            'months': months_arr.flatten().tolist(),
            'savings': savings.flatten().tolist()
        }
    
    def generate_investment_recommendation(self):
        """Genera recomendaciones de inversión basadas en la estrategia seleccionada"""
        recommendations = {
            'conservative': {
                'allocation': {
                    'high_quality_bonds': 0.5,
                    'dividend_stocks': 0.3,
                    'savings_account': 0.2
                },
                'risk_level': 'Bajo',
                'expected_return': '3-5% anual',
                'description': 'Enfoque en preservar capital con bajo riesgo de pérdida.'
            },
            'moderate': {
                'allocation': {
                    'index_funds': 0.5,
                    'blue_chip_stocks': 0.3,
                    'corporate_bonds': 0.2
                },
                'risk_level': 'Medio',
                'expected_return': '6-8% anual',
                'description': 'Balance entre crecimiento y riesgo moderado.'
            },
            'aggressive': {
                'allocation': {
                    'growth_stocks': 0.6,
                    'crypto': 0.2,
                    'international_etfs': 0.2
                },
                'risk_level': 'Alto',
                'expected_return': '10-15% anual (con alta volatilidad)',
                'description': 'Enfoque en crecimiento agresivo con tolerancia a alta volatilidad.'
            }
        }
        
        return recommendations[self.strategy]
    
    def generate_report(self):
        """Genera un reporte financiero completo"""
        spending_analysis = self.analyze_spending()
        savings_prediction = self.predict_future_savings()
        investment_recommendation = self.generate_investment_recommendation()
        
        # Análisis de metas
        goals_analysis = {}
        for term, goal in self.user_data.get('financial_goals', {}).items():
            target = goal['target']
            timeframe = goal['timeframe']
            monthly_needed = (target - self.user_data.get('savings', 0)) / timeframe
            monthly_saving = self.user_data['monthly_income'] - self.user_data['monthly_expenses']
            
            status = 'on_track' if monthly_saving >= monthly_needed else 'off_track'
            shortfall = max(0, monthly_needed - monthly_saving)
            
            goals_analysis[term] = {
                'target': target,
                'timeframe': timeframe,
                'monthly_needed': round(monthly_needed, 2),
                'status': status,
                'shortfall': round(shortfall, 2) if status == 'off_track' else 0,
                'current_saving': monthly_saving
            }
        
        # Recomendaciones personalizadas
        recommendations = []
        
        # Recomendación 1: Reducción de gastos
        if spending_analysis:
            top_category = next(iter(spending_analysis['top_spending_categories'].items()))
            recommendations.append({
                'type': 'expense_reduction',
                'category': top_category[0],
                'current_spending': abs(top_category[1]),
                'suggested_reduction': round(abs(top_category[1]) * 0.15, 2),
                'potential_saving': round(abs(top_category[1]) * 0.15, 2)
            })
        
        # Recomendación 2: Estrategia de inversión
        recommendations.append({
            'type': 'investment_strategy',
            'strategy': self.strategy,
            'allocation': investment_recommendation['allocation'],
            'expected_return': investment_recommendation['expected_return']
        })
        
        # Recomendación 3: Metas financieras
        for term, analysis in goals_analysis.items():
            if analysis['status'] == 'off_track':
                recommendations.append({
                    'type': 'goal_adjustment',
                    'goal_term': term,
                    'current_shortfall': analysis['shortfall'],
                    'suggestion': f"Incrementar ahorro mensual en ${analysis['shortfall']} o ajustar meta"
                })
        
        return {
            'current_status': {
                'monthly_income': self.user_data['monthly_income'],
                'monthly_expenses': self.user_data['monthly_expenses'],
                'monthly_saving': self.user_data['monthly_income'] - self.user_data['monthly_expenses'],
                'savings': self.user_data.get('savings', 0),
                'debt': self.user_data.get('debts', 0)
            },
            'spending_analysis': spending_analysis,
            'savings_prediction': savings_prediction,
            'goals_analysis': goals_analysis,
            'investment_recommendation': investment_recommendation,
            'personalized_recommendations': recommendations,
            'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'strategy_used': self.strategy
        }

# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo del usuario
    user_data = {
        'monthly_income': 3200,
        'monthly_expenses': 2800,
        'savings': 5000,
        'debts': 1500,
        'financial_goals': {
            'short_term': {'target': 5000, 'timeframe': 12},
            'medium_term': {'target': 30000, 'timeframe': 60},
            'long_term': {'target': 250000, 'timeframe': 240}
        },
        'transaction_history': [
            {'date': '2023-01-15', 'amount': -85.50, 'category': 'alimentos'},
            {'date': '2023-01-20', 'amount': -45.00, 'category': 'transporte'},
            {'date': '2023-01-05', 'amount': -120.00, 'category': 'vivienda'},
            {'date': '2023-01-10', 'amount': -28.00, 'category': 'entretenimiento'},
            {'date': '2023-01-25', 'amount': -75.00, 'category': 'salud'},
            {'date': '2023-02-15', 'amount': -90.00, 'category': 'alimentos'},
            {'date': '2023-02-20', 'amount': -50.00, 'category': 'transporte'},
            {'date': '2023-01-01', 'amount': 3200, 'category': 'ingreso'},
            {'date': '2023-02-01', 'amount': 3200, 'category': 'ingreso'}
        ]
    }
    
    # Crear asesor y generar reporte
    advisor = FinancialAdvisorAI(user_data)
    advisor.set_strategy('moderate')  # Prueba con estrategia moderada
    
    report = advisor.generate_report()
    
    # Mostrar reporte
    print("=== REPORTE FINANCIERO ===")
    print(f"Estrategia: {report['strategy_used'].capitalize()}")
    print(f"Generado el: {report['generated_at']}")
    print("\n--- Estado Actual ---")
    print(f"Ingresos mensuales: ${report['current_status']['monthly_income']}")
    print(f"Gastos mensuales: ${report['current_status']['monthly_expenses']}")
    print(f"Ahorro mensual: ${report['current_status']['monthly_saving']}")
    print(f"Ahorros totales: ${report['current_status']['savings']}")
    print(f"Deudas: ${report['current_status']['debt']}")
    
    print("\n--- Análisis de Gastos ---")
    if report['spending_analysis']:
        print("Categorías con mayor gasto:")
        for cat, amount in report['spending_analysis']['top_spending_categories'].items():
            print(f"- {cat.capitalize()}: ${abs(amount):.2f}")
    
    print("\n--- Recomendaciones de Inversión ---")
    inv_rec = report['investment_recommendation']
    print(f"Estrategia: {inv_rec['description']}")
    print(f"Nivel de riesgo: {inv_rec['risk_level']}")
    print(f"Retorno esperado: {inv_rec['expected_return']}")
    print("Distribución recomendada:")
    for asset, allocation in inv_rec['allocation'].items():
        print(f"- {asset.replace('_', ' ').title()}: {allocation*100:.0f}%")
    
    print("\n--- Análisis de Metas ---")
    for term, goal in report['goals_analysis'].items():
        print(f"\nMeta a {term.replace('_', ' ')} plazo:")
        print(f"- Objetivo: ${goal['target']} en {goal['timeframe']} meses")
        print(f"- Ahorro mensual necesario: ${goal['monthly_needed']:.2f}")
        print(f"- Ahorro mensual actual: ${goal['current_saving']:.2f}")
        if goal['status'] == 'on_track':
            print("- Estado: EN CAMINO (¡Buen trabajo!)")
        else:
            print(f"- Estado: FUERA DE CAMINO (Faltan ${goal['shortfall']:.2f} mensuales)")
    
    print("\n--- Recomendaciones Personalizadas ---")
    for i, rec in enumerate(report['personalized_recommendations'], 1):
        print(f"\n{i}. {rec['type'].replace('_', ' ').title()}:")
        if rec['type'] == 'expense_reduction':
            print(f"Reducir gastos en {rec['category']} en un 15%")
            print(f"Gasto actual: ${rec['current_spending']:.2f} mensuales")
            print(f"Ahorro potencial: ${rec['potential_saving']:.2f} mensuales")
        elif rec['type'] == 'investment_strategy':
            print(f"Estrategia de inversión {rec['strategy']}")
            print(f"Retorno esperado: {rec['expected_return']}")
        elif rec['type'] == 'goal_adjustment':
            print(f"Meta a {rec['goal_term'].replace('_', ' ')} plazo necesita ajuste")
            print(f"Faltan ${rec['current_shortfall']:.2f} mensuales para alcanzar la meta")
            print(f"Sugerencia: {rec['suggestion']}")