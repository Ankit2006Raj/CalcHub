"""
Analytics Service for Calculator Application
Generates charts, trends, and visual insights
"""

from typing import Dict, List, Any
import json

class AnalyticsService:
    """Service for generating analytics and visualizations"""
    
    def __init__(self):
        """Initialize analytics service"""
        pass
    
    def generate_bmi_chart_data(self, history: List[Dict]) -> Dict:
        """Generate BMI trend chart data"""
        if not history:
            return {'labels': [], 'data': [], 'categories': []}
        
        labels = []
        data = []
        categories = []
        
        for entry in reversed(history[-10:]):  # Last 10 entries
            labels.append(entry['date'])
            data.append(entry['results'].get('bmi', 0))
            categories.append(entry['results'].get('category', 'Unknown'))
        
        return {
            'type': 'line',
            'labels': labels,
            'datasets': [{
                'label': 'BMI Trend',
                'data': data,
                'borderColor': '#3498db',
                'backgroundColor': 'rgba(52, 152, 219, 0.1)',
                'tension': 0.4
            }],
            'categories': categories,
            'ranges': [
                {'value': 18.5, 'label': 'Underweight', 'color': '#3498db'},
                {'value': 25, 'label': 'Normal', 'color': '#2ecc71'},
                {'value': 30, 'label': 'Overweight', 'color': '#f39c12'},
                {'value': 40, 'label': 'Obese', 'color': '#e74c3c'}
            ]
        }
    
    def generate_calorie_chart_data(self, history: List[Dict]) -> Dict:
        """Generate calorie burn trend chart"""
        if not history:
            return {'labels': [], 'datasets': []}
        
        labels = []
        bmr_data = []
        maintain_data = []
        
        for entry in reversed(history[-10:]):
            labels.append(entry['date'])
            bmr_data.append(entry['results'].get('bmr', 0))
            maintain_data.append(entry['results'].get('maintain', 0))
        
        return {
            'type': 'bar',
            'labels': labels,
            'datasets': [
                {
                    'label': 'BMR (Basal Metabolic Rate)',
                    'data': bmr_data,
                    'backgroundColor': '#3498db'
                },
                {
                    'label': 'Maintenance Calories',
                    'data': maintain_data,
                    'backgroundColor': '#2ecc71'
                }
            ]
        }
    
    def generate_loan_visualization(self, loan_data: Dict) -> Dict:
        """Generate loan repayment visualization"""
        principal = loan_data.get('principal', 0)
        total_interest = loan_data.get('total_interest', 0)
        
        return {
            'type': 'doughnut',
            'labels': ['Principal Amount', 'Total Interest'],
            'datasets': [{
                'data': [principal, total_interest],
                'backgroundColor': ['#3498db', '#e74c3c'],
                'borderWidth': 2
            }],
            'centerText': f"${loan_data.get('total_payment', 0):,.2f}",
            'subtitle': 'Total Payment'
        }
    
    def generate_loan_amortization_schedule(self, amount: float, rate: float, 
                                           duration: int, emi: float) -> List[Dict]:
        """Generate loan amortization schedule"""
        schedule = []
        balance = amount
        monthly_rate = rate / (12 * 100)
        months = duration * 12
        
        for month in range(1, min(months + 1, 13)):  # First 12 months
            interest_payment = balance * monthly_rate
            principal_payment = emi - interest_payment
            balance -= principal_payment
            
            schedule.append({
                'month': month,
                'emi': round(emi, 2),
                'principal': round(principal_payment, 2),
                'interest': round(interest_payment, 2),
                'balance': round(max(balance, 0), 2)
            })
        
        return schedule
    
    def generate_gpa_progress_chart(self, history: List[Dict]) -> Dict:
        """Generate GPA progress chart"""
        if not history:
            return {'labels': [], 'data': []}
        
        labels = []
        data = []
        
        for entry in reversed(history[-10:]):
            labels.append(entry['date'])
            data.append(entry['results'].get('gpa', 0))
        
        return {
            'type': 'line',
            'labels': labels,
            'datasets': [{
                'label': 'GPA Progress',
                'data': data,
                'borderColor': '#9b59b6',
                'backgroundColor': 'rgba(155, 89, 182, 0.1)',
                'tension': 0.4,
                'fill': True
            }],
            'yAxis': {
                'min': 0,
                'max': 4.0,
                'ticks': [0, 1.0, 2.0, 3.0, 4.0]
            },
            'annotations': [
                {'y': 3.5, 'label': 'Excellent', 'color': '#2ecc71'},
                {'y': 3.0, 'label': 'Good', 'color': '#3498db'},
                {'y': 2.5, 'label': 'Average', 'color': '#f39c12'}
            ]
        }
    
    def generate_attendance_chart(self, history: List[Dict]) -> Dict:
        """Generate attendance improvement chart"""
        if not history:
            return {'labels': [], 'data': []}
        
        labels = []
        data = []
        
        for entry in reversed(history[-10:]):
            labels.append(entry['date'])
            data.append(entry['results'].get('current_percentage', 0))
        
        return {
            'type': 'line',
            'labels': labels,
            'datasets': [{
                'label': 'Attendance %',
                'data': data,
                'borderColor': '#e74c3c',
                'backgroundColor': 'rgba(231, 76, 60, 0.1)',
                'tension': 0.4,
                'fill': True
            }],
            'yAxis': {
                'min': 0,
                'max': 100
            },
            'threshold': {
                'value': 75,
                'label': 'Minimum Required',
                'color': '#f39c12'
            }
        }
    
    def generate_comparison_chart(self, calculator_type: str, 
                                  current: Dict, previous: Dict) -> Dict:
        """Generate before/after comparison chart"""
        if calculator_type == 'bmi':
            return {
                'type': 'bar',
                'labels': ['Previous', 'Current'],
                'datasets': [{
                    'label': 'BMI',
                    'data': [
                        previous.get('bmi', 0),
                        current.get('bmi', 0)
                    ],
                    'backgroundColor': ['#95a5a6', '#3498db']
                }]
            }
        
        elif calculator_type == 'gpa':
            return {
                'type': 'bar',
                'labels': ['Previous', 'Current'],
                'datasets': [{
                    'label': 'GPA',
                    'data': [
                        previous.get('gpa', 0),
                        current.get('gpa', 0)
                    ],
                    'backgroundColor': ['#95a5a6', '#9b59b6']
                }]
            }
        
        return {}
    
    def generate_monthly_activity_heatmap(self, history: List[Dict]) -> Dict:
        """Generate monthly activity heatmap data"""
        activity_map = {}
        
        for entry in history:
            date = entry['date']
            activity_map[date] = activity_map.get(date, 0) + 1
        
        return {
            'type': 'heatmap',
            'data': activity_map,
            'colorScale': {
                'low': '#ebedf0',
                'medium': '#9be9a8',
                'high': '#40c463',
                'highest': '#30a14e'
            }
        }
    
    def generate_calculator_usage_stats(self, history: List[Dict]) -> Dict:
        """Generate calculator usage statistics"""
        usage = {}
        
        for entry in history:
            calc_type = entry['calculator_type']
            usage[calc_type] = usage.get(calc_type, 0) + 1
        
        # Sort by usage
        sorted_usage = sorted(usage.items(), key=lambda x: x[1], reverse=True)
        
        return {
            'type': 'pie',
            'labels': [item[0].replace('_', ' ').title() for item in sorted_usage],
            'datasets': [{
                'data': [item[1] for item in sorted_usage],
                'backgroundColor': [
                    '#3498db', '#2ecc71', '#f39c12', '#e74c3c',
                    '#9b59b6', '#1abc9c', '#34495e', '#e67e22'
                ]
            }],
            'total': sum(usage.values())
        }
    
    def generate_insights(self, calculator_type: str, history: List[Dict], 
                         current_result: Dict) -> List[str]:
        """Generate AI-powered insights"""
        insights = []
        
        if not history or len(history) < 2:
            return ["Start tracking your progress to see insights and trends!"]
        
        if calculator_type == 'bmi':
            bmis = [h['results'].get('bmi', 0) for h in history]
            change = bmis[0] - bmis[-1]
            
            if change > 0:
                insights.append(f"📈 Your BMI has increased by {abs(change):.1f} points")
            elif change < 0:
                insights.append(f"📉 Great! Your BMI has decreased by {abs(change):.1f} points")
            else:
                insights.append("➡️ Your BMI has remained stable")
            
            avg_bmi = sum(bmis) / len(bmis)
            insights.append(f"📊 Your average BMI over time: {avg_bmi:.1f}")
            
        elif calculator_type == 'gpa':
            gpas = [h['results'].get('gpa', 0) for h in history]
            change = gpas[0] - gpas[-1]
            
            if change > 0:
                insights.append(f"🎓 Excellent! Your GPA improved by {abs(change):.2f} points")
            elif change < 0:
                insights.append(f"⚠️ Your GPA decreased by {abs(change):.2f} points - time to focus!")
            else:
                insights.append("➡️ Your GPA has remained consistent")
            
            if gpas[0] >= 3.5:
                insights.append("⭐ You're maintaining excellent academic performance!")
            
        elif calculator_type == 'attendance':
            percentages = [h['results'].get('current_percentage', 0) for h in history]
            change = percentages[0] - percentages[-1]
            
            if change > 0:
                insights.append(f"✅ Your attendance improved by {abs(change):.1f}%")
            elif change < 0:
                insights.append(f"⚠️ Your attendance dropped by {abs(change):.1f}%")
            
            if percentages[0] >= 75:
                insights.append("🎯 You're meeting the attendance requirement!")
            else:
                insights.append("📌 Focus on improving attendance to meet requirements")
        
        elif calculator_type == 'loan':
            insights.append(f"💰 Total interest over loan period: ${current_result.get('total_interest', 0):,.2f}")
            insights.append(f"📅 You've calculated {len(history)} loan scenarios")
        
        return insights
    
    def generate_recommendations_based_on_trends(self, calculator_type: str, 
                                                 history: List[Dict]) -> List[str]:
        """Generate recommendations based on historical trends"""
        if not history or len(history) < 3:
            return []
        
        recommendations = []
        
        if calculator_type == 'bmi':
            bmis = [h['results'].get('bmi', 0) for h in history[-5:]]
            trend = sum([bmis[i] - bmis[i-1] for i in range(1, len(bmis))]) / (len(bmis) - 1)
            
            if trend > 0.5:
                recommendations.append("Your BMI is trending upward. Consider reviewing your diet and exercise routine.")
            elif trend < -0.5:
                recommendations.append("Great progress! Your BMI is trending downward. Keep up the good work!")
            
        elif calculator_type == 'gpa':
            gpas = [h['results'].get('gpa', 0) for h in history[-5:]]
            trend = sum([gpas[i] - gpas[i-1] for i in range(1, len(gpas))]) / (len(gpas) - 1)
            
            if trend < -0.1:
                recommendations.append("Your GPA is declining. Consider meeting with an academic advisor.")
            elif trend > 0.1:
                recommendations.append("Excellent! Your GPA is improving. Maintain your study habits!")
        
        return recommendations
