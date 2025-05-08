import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
from typing import Dict, List, Tuple, Optional

class FinancialHealthAnalyzer:
    """
    Sistema de IA para evaluar salud financiera, progreso de metas y ofrecer recomendaciones.
    """
    
    def __init__(self, financial_data: Dict):
        """
        Inicializa el analizador con datos financieros.
        
        Args:
            financial_data (Dict): Datos financieros en formato:
                {
                    "transactions": List[Dict],  # Todas las transacciones
                    "budgets": List[Dict],       # Presupuestos por categoría
                    "savings_goals": List[Dict], # Metas de ahorro
                    "income_sources": List[Dict] # Fuentes de ingresos
                }
        """
        self.data = financial_data
        self.transactions_df = self._prepare_transaction_data()
        self.budgets_df = self._prepare_budget_data()
        self.goals_df = self._prepare_goals_data()
        self.income_df = self._prepare_income_data()
        
        # Configuración inicial
        self.emergency_fund_months = 3  # Meses de gastos para fondo de emergencia
        self.risk_profile = "moderate"  # Perfil de riesgo (conservative/moderate/aggressive)
        
    def _prepare_transaction_data(self) -> pd.DataFrame:
        """Prepara los datos de transacciones."""
        df = pd.DataFrame(self.data["transactions"])
        df['date'] = pd.to_datetime(df['date'])
        df['month'] = df['date'].dt.to_period('M')
        df['year'] = df['date'].dt.year
        df['is_expense'] = df['amount'] < 0
        df['is_income'] = df['amount'] > 0
        return df
    
    def _prepare_budget_data(self) -> pd.DataFrame:
        """Prepara los datos de presupuestos."""
        return pd.DataFrame(self.data["budgets"])
    
    def _prepare_goals_data(self) -> pd.DataFrame:
        """Prepara los datos de metas de ahorro."""
        return pd.DataFrame(self.data["savings_goals"])
    
    def _prepare_income_data(self) -> pd.DataFrame:
        """Prepara los datos de fuentes de ingresos."""
        return pd.DataFrame(self.data["income_sources"])
    
    def analyze_financial_health(self) -> Dict:
        """
        Realiza un análisis completo de la salud financiera.
        
        Returns:
            Dict: Resultados del análisis con métricas clave y recomendaciones.
        """
        results = {
            "cash_flow_analysis": self._analyze_cash_flow(),
            "spending_analysis": self._analyze_spending_patterns(),
            "savings_analysis": self._analyze_savings_progress(),
            "budget_analysis": self._analyze_budget_adherence(),
            "net_worth_trend": self._calculate_net_worth_trend(),
            "anomaly_detection": self._detect_anomalies(),
            "risk_assessment": self._assess_financial_risk(),
            "recommendations": self._generate_recommendations()
        }
        
        return results
    
    def _analyze_cash_flow(self) -> Dict:
        """Analiza el flujo de efectivo mensual."""
        monthly_cash_flow = self.transactions_df.groupby('month')['amount'].sum()
        income = self.transactions_df[self.transactions_df['is_income']].groupby('month')['amount'].sum()
        expenses = self.transactions_df[self.transactions_df['is_expense']].groupby('month')['amount'].sum()
        
        # Cálculo de métricas
        avg_monthly_income = income.mean()
        avg_monthly_expenses = expenses.mean()
        avg_monthly_savings = monthly_cash_flow.mean()
        savings_rate = (avg_monthly_savings / avg_monthly_income) * 100 if avg_monthly_income > 0 else 0
        
        return {
            "avg_monthly_income": avg_monthly_income,
            "avg_monthly_expenses": avg_monthly_expenses,
            "avg_monthly_savings": avg_monthly_savings,
            "savings_rate": savings_rate,
            "monthly_trend": monthly_cash_flow.to_dict(),
            "income_trend": income.to_dict(),
            "expenses_trend": expenses.to_dict()
        }
    
    def _analyze_spending_patterns(self) -> Dict:
        """Analiza patrones de gasto y categorización."""
        expenses = self.transactions_df[self.transactions_df['is_expense']].copy()
        expenses['amount'] = expenses['amount'].abs()
        
        # Gastos por categoría
        spending_by_category = expenses.groupby('category')['amount'].sum().sort_values(ascending=False)
        
        # Segmentación de gastos (necesidades vs deseos)
        necessities = ['Vivienda', 'Alimentos', 'Transporte', 'Salud', 'Educación']
        expenses['is_necessity'] = expenses['category'].isin(necessities)
        necessity_spending = expenses[expenses['is_necessity']]['amount'].sum()
        discretionary_spending = expenses[~expenses['is_necessity']]['amount'].sum()
        
        # Detección de categorías problemáticas
        problem_categories = []
        if len(self.budgets_df) > 0:
            merged = pd.merge(
                expenses.groupby('category')['amount'].sum().reset_index(),
                self.budgets_df,
                on='category',
                how='left'
            )
            merged['pct_of_budget'] = (merged['amount'] / merged['budget_amount']) * 100
            problem_categories = merged[merged['pct_of_budget'] > 90][['category', 'pct_of_budget']].to_dict('records')
        
        return {
            "total_spending": expenses['amount'].sum(),
            "spending_by_category": spending_by_category.to_dict(),
            "necessity_spending": necessity_spending,
            "discretionary_spending": discretionary_spending,
            "necessity_ratio": (necessity_spending / expenses['amount'].sum()) * 100 if expenses['amount'].sum() > 0 else 0,
            "problem_categories": problem_categories,
            "top_spending_categories": spending_by_category.head(3).index.tolist()
        }
    
    def _analyze_savings_progress(self) -> Dict:
        """Evalúa el progreso hacia las metas de ahorro."""
        if self.goals_df.empty:
            return {"status": "No savings goals defined"}
        
        results = {}
        total_saved = 0
        total_goals = 0
        completed_goals = 0
        on_track_goals = 0
        behind_goals = 0
        
        for _, goal in self.goals_df.iterrows():
            target_date = pd.to_datetime(goal['target_date'])
            months_to_goal = (target_date.year - datetime.now().year) * 12 + (target_date.month - datetime.now().month)
            monthly_saving_needed = goal['target_amount'] / months_to_goal if months_to_goal > 0 else goal['target_amount']
            
            current_progress = goal['current_amount'] / goal['target_amount'] * 100
            required_monthly = monthly_saving_needed
            actual_monthly = self._calculate_monthly_saving_for_goal(goal['goal_name'])
            
            status = "on_track" if current_progress >= (100 * (datetime.now().month / months_to_goal)) else "behind"
            
            if current_progress >= 100:
                completed_goals += 1
                status = "completed"
            elif status == "on_track":
                on_track_goals += 1
            else:
                behind_goals += 1
            
            results[goal['goal_name']] = {
                "target_amount": goal['target_amount'],
                "current_amount": goal['current_amount'],
                "progress": current_progress,
                "target_date": goal['target_date'],
                "status": status,
                "monthly_needed": monthly_saving_needed,
                "monthly_actual": actual_monthly,
                "months_to_complete": months_to_goal
            }
            
            total_saved += goal['current_amount']
            total_goals += goal['target_amount']
        
        # Análisis del fondo de emergencia
        avg_monthly_expenses = abs(self.transactions_df[self.transactions_df['is_expense']]['amount'].mean())
        emergency_fund_needed = avg_monthly_expenses * self.emergency_fund_months
        emergency_savings = self.goals_df[self.goals_df['goal_name'] == 'Fondo de Emergencia']['current_amount'].sum()
        emergency_progress = (emergency_savings / emergency_fund_needed) * 100 if emergency_fund_needed > 0 else 0
        
        return {
            "goals_progress": results,
            "total_saved": total_saved,
            "total_goals": total_goals,
            "overall_progress": (total_saved / total_goals) * 100 if total_goals > 0 else 0,
            "completed_goals": completed_goals,
            "on_track_goals": on_track_goals,
            "behind_goals": behind_goals,
            "emergency_fund": {
                "needed": emergency_fund_needed,
                "current": emergency_savings,
                "progress": emergency_progress,
                "status": "adequate" if emergency_progress >= 100 else "inadequate"
            }
        }
    
    def _calculate_monthly_saving_for_goal(self, goal_name: str) -> float:
        """Calcula el ahorro mensual promedio para una meta específica."""
        savings_transactions = self.transactions_df[
            (self.transactions_df['category'] == 'Ahorros') & 
            (self.transactions_df['description'].str.contains(goal_name, case=False))
        ]
        
        if savings_transactions.empty:
            return 0.0
        
        monthly_savings = savings_transactions.groupby('month')['amount'].sum()
        return monthly_savings.mean()
    
    def _analyze_budget_adherence(self) -> Dict:
        """Evalúa el cumplimiento de los presupuestos por categoría."""
        if self.budgets_df.empty:
            return {"status": "No budgets defined"}
        
        expenses = self.transactions_df[self.transactions_df['is_expense']].copy()
        expenses['amount'] = expenses['amount'].abs()
        
        # Agrupar gastos por categoría y mes
        monthly_spending = expenses.groupby(['category', 'month'])['amount'].sum().reset_index()
        
        # Combinar con presupuestos
        merged = pd.merge(monthly_spending, self.budgets_df, on='category', how='right')
        merged['pct_of_budget'] = (merged['amount'] / merged['budget_amount']) * 100
        merged['is_over'] = merged['pct_of_budget'] > 100
        
        # Calcular métricas
        avg_budget_utilization = merged.groupby('category')['pct_of_budget'].mean()
        over_budget_months = merged[merged['is_over']].groupby('category').size()
        budget_compliance = (1 - (len(merged[merged['is_over']]) / len(merged))) * 100
        
        problem_categories = avg_budget_utilization[avg_budget_utilization > 90].index.tolist()
        
        return {
            "avg_budget_utilization": avg_budget_utilization.to_dict(),
            "over_budget_categories": over_budget_months.to_dict(),
            "budget_compliance_rate": budget_compliance,
            "problem_categories": problem_categories,
            "most_respected_category": avg_budget_utilization.idxmin(),
            "most_violated_category": avg_budget_utilization.idxmax()
        }
    
    def _calculate_net_worth_trend(self) -> Dict:
        """Calcula la tendencia del patrimonio neto a lo largo del tiempo."""
        # Agrupar por mes (esto es simplificado - en realidad necesitarías datos de activos/pasivos)
        monthly_net = self.transactions_df.groupby('month')['amount'].sum()
        cumulative_net = monthly_net.cumsum()
        
        # Calcular tasa de crecimiento
        growth_rates = cumulative_net.pct_change() * 100
        
        return {
            "net_worth_trend": cumulative_net.to_dict(),
            "growth_rates": growth_rates.to_dict(),
            "current_net_worth": cumulative_net.iloc[-1] if len(cumulative_net) > 0 else 0,
            "avg_monthly_growth": growth_rates.mean()
        }
    
    def _detect_anomalies(self) -> Dict:
        """Detecta transacciones y patrones anómalos usando Isolation Forest."""
        if len(self.transactions_df) < 10:
            return {"status": "Insufficient data for anomaly detection"}
        
        # Preparar datos para detección de anomalías
        expenses = self.transactions_df[self.transactions_df['is_expense']].copy()
        expenses['amount'] = expenses['amount'].abs()
        
        # Agrupar por categoría y calcular estadísticas
        category_stats = expenses.groupby('category')['amount'].agg(['mean', 'std', 'count'])
        category_stats = category_stats[category_stats['count'] > 5]  # Solo categorías con suficientes datos
        
        # Detectar anomalías por categoría
        anomalies = []
        for category in category_stats.index:
            cat_expenses = expenses[expenses['category'] == category]['amount'].values.reshape(-1, 1)
            
            # Escalar datos
            scaler = StandardScaler()
            X = scaler.fit_transform(cat_expenses)
            
            # Entrenar modelo de detección de anomalías
            clf = IsolationForest(contamination=0.05, random_state=42)
            preds = clf.fit_predict(X)
            
            # Obtener anomalías
            cat_anomalies = expenses[(expenses['category'] == category) & (preds == -1)]
            
            if not cat_anomalies.empty:
                for _, row in cat_anomalies.iterrows():
                    anomalies.append({
                        "date": str(row['date']),
                        "category": category,
                        "amount": row['amount'],
                        "description": row['description'],
                        "deviation": (row['amount'] - category_stats.loc[category, 'mean']) / 
                                      category_stats.loc[category, 'std'] if category_stats.loc[category, 'std'] > 0 else 0
                    })
        
        # Detectar cambios significativos en patrones de gasto (simplificado)
        monthly_spending = expenses.groupby('month')['amount'].sum()
        spending_change = monthly_spending.pct_change()
        significant_changes = spending_change[abs(spending_change) > 0.3]  # >30% cambio
        
        return {
            "transaction_anomalies": anomalies,
            "spending_pattern_changes": significant_changes.to_dict(),
            "total_anomalies_detected": len(anomalies),
            "avg_anomaly_amount": np.mean([a['amount'] for a in anomalies]) if anomalies else 0
        }
    
    def _assess_financial_risk(self) -> Dict:
        """Evalúa los riesgos financieros basados en varios factores."""
        cash_flow = self._analyze_cash_flow()
        savings = self._analyze_savings_progress()
        spending = self._analyze_spending_patterns()
        
        # Calcular puntaje de riesgo (0-100, menor es mejor)
        risk_score = 0
        
        # 1. Riesgo de liquidez (30% peso)
        emergency_status = savings["emergency_fund"]["status"]
        liquidity_risk = 0
        if emergency_status == "inadequate":
            liquidity_risk = 100 - savings["emergency_fund"]["progress"]
        risk_score += liquidity_risk * 0.3
        
        # 2. Riesgo de gastos (25% peso)
        necessity_ratio = spending["necessity_ratio"]
        spending_risk = max(0, necessity_ratio - 50) * 2  # >50% en necesidades es riesgoso
        risk_score += min(spending_risk, 100) * 0.25
        
        # 3. Riesgo de ingresos (20% peso)
        income_sources = len(self.income_df)
        income_concentration = 100 / income_sources if income_sources > 0 else 100
        income_risk = min(income_concentration * 0.8, 100)  # Más fuentes = menor riesgo
        risk_score += income_risk * 0.2
        
        # 4. Riesgo de deuda (25% peso)
        # (Simplificado - asumimos que no hay datos de deuda)
        debt_risk = 0
        risk_score += debt_risk * 0.25
        
        # Determinar nivel de riesgo
        if risk_score < 30:
            risk_level = "low"
        elif risk_score < 60:
            risk_level = "moderate"
        else:
            risk_level = "high"
        
        return {
            "overall_risk_score": risk_score,
            "risk_level": risk_level,
            "liquidity_risk": liquidity_risk,
            "spending_risk": spending_risk,
            "income_risk": income_risk,
            "debt_risk": debt_risk
        }
    
    def _generate_recommendations(self) -> List[Dict]:
        """Genera recomendaciones personalizadas basadas en el análisis."""
        analysis = {
            "cash_flow": self._analyze_cash_flow(),
            "spending": self._analyze_spending_patterns(),
            "savings": self._analyze_savings_progress(),
            "budgets": self._analyze_budget_adherence(),
            "risk": self._assess_financial_risk()
        }
        
        recommendations = []
        
        # 1. Recomendaciones sobre ahorros
        if analysis["savings"]["emergency_fund"]["status"] == "inadequate":
            needed = analysis["savings"]["emergency_fund"]["needed"]
            current = analysis["savings"]["emergency_fund"]["current"]
            monthly_saving = (needed - current) / 6  # Meta de 6 meses para completar
            
            recommendations.append({
                "category": "emergency_fund",
                "priority": "high",
                "action": f"Increase emergency savings by ${monthly_saving:.2f} per month",
                "reason": f"Current emergency fund covers {current/needed*100:.1f}% of recommended {self.emergency_fund_months}-month coverage",
                "impact": "Reduces financial vulnerability to unexpected expenses"
            })
        
        # 2. Recomendaciones sobre gastos problemáticos
        for category in analysis["spending"]["problem_categories"]:
            current_spending = analysis["spending"]["spending_by_category"][category]
            if category in analysis["budgets"]["avg_budget_utilization"]:
                budget_pct = analysis["budgets"]["avg_budget_utilization"][category]
                recommendations.append({
                    "category": "spending",
                    "priority": "medium",
                    "action": f"Reduce spending in {category} by {(budget_pct-100):.1f}% to stay within budget",
                    "reason": f"Currently spending {current_spending:.2f} ({budget_pct:.1f}% of budget)",
                    "impact": "Improves budget adherence and frees up cash flow"
                })
        
        # 3. Recomendaciones sobre metas atrasadas
        for goal, data in analysis["savings"]["goals_progress"].items():
            if data["status"] == "behind":
                needed = data["monthly_needed"]
                actual = data["monthly_actual"]
                shortfall = needed - actual
                
                if shortfall > 0:
                    recommendations.append({
                        "category": "savings_goal",
                        "priority": "medium",
                        "action": f"Increase monthly savings for '{goal}' by ${shortfall:.2f}",
                        "reason": f"Current progress: {data['progress']:.1f}%, needs {needed:.2f}/month to reach target",
                        "impact": "Keeps savings goals on track"
                    })
        
        # 4. Recomendaciones sobre diversificación de ingresos
        if analysis["risk"]["income_risk"] > 50:
            recommendations.append({
                "category": "income",
                "priority": "low",
                "action": "Consider developing additional income sources",
                "reason": f"Reliance on few income sources increases financial risk",
                "impact": "Reduces vulnerability to income shocks"
            })
        
        # 5. Recomendación general basada en tasa de ahorro
        savings_rate = analysis["cash_flow"]["savings_rate"]
        if savings_rate < 20:
            recommendations.append({
                "category": "savings",
                "priority": "high",
                "action": f"Increase monthly savings rate from current {savings_rate:.1f}% to at least 20%",
                "reason": "Recommended savings rate for healthy finances is 20% or more",
                "impact": "Accelerates wealth building and financial security"
            })
        
        return recommendations
    
    def generate_report(self, format: str = "dict") -> Dict:
        """
        Genera un reporte completo del análisis financiero.
        
        Args:
            format (str): Formato de salida ('dict' o 'json')
            
        Returns:
            Dict or str: Reporte financiero en el formato solicitado
        """
        analysis = self.analyze_financial_health()
        
        report = {
            "summary": {
                "current_net_worth": analysis["net_worth_trend"]["current_net_worth"],
                "savings_rate": analysis["cash_flow_analysis"]["savings_rate"],
                "emergency_fund_status": analysis["savings_analysis"]["emergency_fund"]["status"],
                "financial_risk_level": analysis["risk_assessment"]["risk_level"],
                "budget_compliance": analysis["budget_analysis"]["budget_compliance_rate"],
                "goals_progress": analysis["savings_analysis"]["overall_progress"]
            },
            "detailed_analysis": analysis,
            "recommendations": analysis["recommendations"],
            "timestamp": datetime.now().isoformat()
        }
        
        if format == "json":
            return json.dumps(report, indent=2)
        return report


# Ejemplo de uso
if __name__ == "__main__":
    # Datos de ejemplo (en la práctica, estos vendrían de tu base de datos)
    example_data = {
        "transactions": [
            {"date": "2023-01-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-01-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-01-15", "amount": -450.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-01-20", "amount": -150.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-01-25", "amount": -200.00, "category": "Entretenimiento", "description": "Cena"},
            {"date": "2023-02-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-02-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-02-15", "amount": -500.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-02-20", "amount": -180.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-02-25", "amount": -300.00, "category": "Entretenimiento", "description": "Concierto"},
            {"date": "2023-03-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-03-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-03-15", "amount": -400.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-03-20", "amount": -200.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-03-25", "amount": -100.00, "category": "Entretenimiento", "description": "Cine"},
            {"date": "2023-03-28", "amount": 500.00, "category": "Extra", "description": "Bono"},
            {"date": "2023-03-30", "amount": -1500.00, "category": "Vivienda", "description": "Reparación"},
            {"date": "2023-04-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-04-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-04-15", "amount": -350.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-04-20", "amount": -220.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-04-25", "amount": -80.00, "category": "Entretenimiento", "description": "Streaming"},
            {"date": "2023-05-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-05-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-05-15", "amount": -600.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-05-20", "amount": -180.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-05-25", "amount": -250.00, "category": "Entretenimiento", "description": "Regalos"},
            {"date": "2023-06-05", "amount": 2500.00, "category": "Salario", "description": "Pago nómina"},
            {"date": "2023-06-10", "amount": -1200.00, "category": "Vivienda", "description": "Renta"},
            {"date": "2023-06-15", "amount": -550.00, "category": "Alimentos", "description": "Supermercado"},
            {"date": "2023-06-20", "amount": -200.00, "category": "Transporte", "description": "Gasolina"},
            {"date": "2023-06-25", "amount": -120.00, "category": "Entretenimiento", "description": "Cena"},
            {"date": "2023-06-30", "amount": 200.00, "category": "Ahorros", "description": "Depósito fondo emergencia"},
            {"date": "2023-06-30", "amount": 300.00, "category": "Ahorros", "description": "Depósito vacaciones"}
        ],
        "budgets": [
            {"category": "Vivienda", "budget_amount": 1200.00},
            {"category": "Alimentos", "budget_amount": 500.00},
            {"category": "Transporte", "budget_amount": 200.00},
            {"category": "Entretenimiento", "budget_amount": 150.00},
            {"category": "Ahorros", "budget_amount": 500.00}
        ],
        "savings_goals": [
            {"goal_name": "Fondo de Emergencia", "target_amount": 5000.00, "current_amount": 2000.00, "target_date": "2023-12-31"},
            {"goal_name": "Vacaciones", "target_amount": 3000.00, "current_amount": 800.00, "target_date": "2024-06-01"}
        ],
        "income_sources": [
            {"source": "Empleo principal", "amount": 2500.00, "frequency": "monthly"},
            {"source": "Freelance", "amount": 300.00, "frequency": "variable"}
        ]
    }
    
    # Crear analizador y generar reporte
    analyzer = FinancialHealthAnalyzer(example_data)
    report = analyzer.generate_report("json")
    
    print("=== Reporte de Salud Financiera ===")
    print(report)
    
    # También puedes acceder a análisis específicos
    print("\n=== Recomendaciones ===")
    for rec in analyzer.analyze_financial_health()["recommendations"]:
        print(f"- [{rec['priority'].upper()}] {rec['action']} ({rec['reason']})")