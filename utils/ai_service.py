"""
AI Service for Calculator Application
Provides AI-powered recommendations, explanations, and chatbot functionality
"""

import os
from typing import Dict, List, Any
import json

class AIService:
    """AI Service for generating recommendations and explanations"""
    
    def __init__(self):
        """Initialize AI Service"""
        self.use_openai = False
        # Check if OpenAI API key is available
        api_key = os.getenv('OPENAI_API_KEY')
        if api_key:
            try:
                import openai
                openai.api_key = api_key
                self.use_openai = True
                self.client = openai.OpenAI(api_key=api_key)
            except:
                self.use_openai = False
    
    def get_bmi_recommendations(self, bmi: float, category: str, height: float, weight: float) -> Dict:
        """Generate AI-powered BMI recommendations"""
        recommendations = {
            'diet_plan': self._generate_diet_plan(bmi, category, weight),
            'workout_plan': self._generate_workout_plan(bmi, category),
            'calorie_plan': self._generate_calorie_reduction_plan(bmi, category, weight),
            'explanation': self._explain_bmi(bmi, category),
            'visual_insight': self._get_visual_insight('bmi', bmi, category)
        }
        return recommendations

    
    def _generate_diet_plan(self, bmi: float, category: str, weight: float) -> List[Dict]:
        """Generate personalized diet plan"""
        plans = {
            'Underweight': [
                {'meal': 'Breakfast', 'items': ['Oatmeal with nuts and banana', 'Whole milk', 'Protein shake'], 'calories': 600},
                {'meal': 'Mid-Morning', 'items': ['Peanut butter sandwich', 'Fruit juice'], 'calories': 400},
                {'meal': 'Lunch', 'items': ['Brown rice', 'Chicken/Fish', 'Vegetables', 'Yogurt'], 'calories': 700},
                {'meal': 'Evening', 'items': ['Protein bar', 'Nuts', 'Smoothie'], 'calories': 400},
                {'meal': 'Dinner', 'items': ['Pasta/Rice', 'Lean meat', 'Salad', 'Avocado'], 'calories': 650},
                {'meal': 'Before Bed', 'items': ['Casein protein shake', 'Almonds'], 'calories': 250}
            ],
            'Normal': [
                {'meal': 'Breakfast', 'items': ['Eggs', 'Whole grain toast', 'Fruit'], 'calories': 400},
                {'meal': 'Mid-Morning', 'items': ['Greek yogurt', 'Berries'], 'calories': 200},
                {'meal': 'Lunch', 'items': ['Grilled chicken', 'Quinoa', 'Vegetables'], 'calories': 500},
                {'meal': 'Evening', 'items': ['Apple', 'Almonds'], 'calories': 200},
                {'meal': 'Dinner', 'items': ['Fish', 'Sweet potato', 'Broccoli'], 'calories': 450}
            ],
            'Overweight': [
                {'meal': 'Breakfast', 'items': ['Oatmeal', 'Berries', 'Green tea'], 'calories': 300},
                {'meal': 'Mid-Morning', 'items': ['Apple', 'Handful of nuts'], 'calories': 150},
                {'meal': 'Lunch', 'items': ['Grilled chicken salad', 'Olive oil dressing'], 'calories': 400},
                {'meal': 'Evening', 'items': ['Carrot sticks', 'Hummus'], 'calories': 150},
                {'meal': 'Dinner', 'items': ['Grilled fish', 'Steamed vegetables'], 'calories': 350}
            ],
            'Obese': [
                {'meal': 'Breakfast', 'items': ['Egg whites', 'Spinach', 'Whole grain toast'], 'calories': 250},
                {'meal': 'Mid-Morning', 'items': ['Low-fat yogurt', 'Cucumber'], 'calories': 100},
                {'meal': 'Lunch', 'items': ['Lean protein', 'Large salad', 'Lemon water'], 'calories': 350},
                {'meal': 'Evening', 'items': ['Celery', 'Almond butter'], 'calories': 100},
                {'meal': 'Dinner', 'items': ['Grilled chicken breast', 'Steamed broccoli'], 'calories': 300}
            ]
        }
        return plans.get(category, plans['Normal'])

    
    def _generate_workout_plan(self, bmi: float, category: str) -> List[Dict]:
        """Generate personalized workout plan"""
        plans = {
            'Underweight': [
                {'day': 'Monday', 'focus': 'Upper Body Strength', 'exercises': ['Bench Press 4x8', 'Rows 4x8', 'Shoulder Press 3x10'], 'duration': '45 min'},
                {'day': 'Tuesday', 'focus': 'Lower Body Strength', 'exercises': ['Squats 4x8', 'Deadlifts 3x8', 'Lunges 3x10'], 'duration': '45 min'},
                {'day': 'Wednesday', 'focus': 'Rest/Light Cardio', 'exercises': ['Walking 20 min'], 'duration': '20 min'},
                {'day': 'Thursday', 'focus': 'Upper Body', 'exercises': ['Pull-ups 3x8', 'Dips 3x10', 'Bicep Curls 3x12'], 'duration': '40 min'},
                {'day': 'Friday', 'focus': 'Lower Body', 'exercises': ['Leg Press 4x10', 'Calf Raises 4x15', 'Hamstring Curls 3x12'], 'duration': '40 min'},
                {'day': 'Weekend', 'focus': 'Rest/Active Recovery', 'exercises': ['Yoga or stretching'], 'duration': '30 min'}
            ],
            'Normal': [
                {'day': 'Monday', 'focus': 'Full Body Strength', 'exercises': ['Squats 3x10', 'Push-ups 3x15', 'Rows 3x12'], 'duration': '40 min'},
                {'day': 'Tuesday', 'focus': 'Cardio', 'exercises': ['Running 30 min', 'Jump rope 10 min'], 'duration': '40 min'},
                {'day': 'Wednesday', 'focus': 'Upper Body', 'exercises': ['Bench Press 3x10', 'Pull-ups 3x8', 'Shoulder Press 3x10'], 'duration': '40 min'},
                {'day': 'Thursday', 'focus': 'HIIT', 'exercises': ['Burpees', 'Mountain Climbers', 'High Knees'], 'duration': '30 min'},
                {'day': 'Friday', 'focus': 'Lower Body', 'exercises': ['Deadlifts 3x8', 'Lunges 3x12', 'Leg Press 3x10'], 'duration': '40 min'},
                {'day': 'Weekend', 'focus': 'Active Recovery', 'exercises': ['Swimming or cycling'], 'duration': '45 min'}
            ],
            'Overweight': [
                {'day': 'Monday', 'focus': 'Low-Impact Cardio', 'exercises': ['Brisk walking 30 min', 'Elliptical 15 min'], 'duration': '45 min'},
                {'day': 'Tuesday', 'focus': 'Strength Training', 'exercises': ['Bodyweight squats 3x12', 'Wall push-ups 3x10', 'Resistance bands'], 'duration': '30 min'},
                {'day': 'Wednesday', 'focus': 'Cardio', 'exercises': ['Swimming 30 min or Cycling'], 'duration': '30 min'},
                {'day': 'Thursday', 'focus': 'Core & Flexibility', 'exercises': ['Planks 3x30sec', 'Yoga', 'Stretching'], 'duration': '30 min'},
                {'day': 'Friday', 'focus': 'Cardio Intervals', 'exercises': ['Walk-jog intervals 25 min'], 'duration': '25 min'},
                {'day': 'Weekend', 'focus': 'Active Lifestyle', 'exercises': ['Hiking', 'Dancing', 'Sports'], 'duration': '60 min'}
            ],
            'Obese': [
                {'day': 'Monday', 'focus': 'Gentle Walking', 'exercises': ['Walk 20 min at comfortable pace'], 'duration': '20 min'},
                {'day': 'Tuesday', 'focus': 'Chair Exercises', 'exercises': ['Seated leg lifts', 'Arm circles', 'Seated marching'], 'duration': '15 min'},
                {'day': 'Wednesday', 'focus': 'Water Aerobics', 'exercises': ['Pool walking', 'Water exercises'], 'duration': '30 min'},
                {'day': 'Thursday', 'focus': 'Stretching', 'exercises': ['Gentle yoga', 'Flexibility exercises'], 'duration': '20 min'},
                {'day': 'Friday', 'focus': 'Walking', 'exercises': ['Walk 25 min'], 'duration': '25 min'},
                {'day': 'Weekend', 'focus': 'Light Activity', 'exercises': ['Gardening', 'Light housework'], 'duration': '30 min'}
            ]
        }
        return plans.get(category, plans['Normal'])

    
    def _generate_calorie_reduction_plan(self, bmi: float, category: str, weight: float) -> Dict:
        """Generate calorie reduction/increase plan"""
        if category == 'Underweight':
            return {
                'goal': 'Gain weight healthily',
                'weekly_target': '+0.5 kg per week',
                'daily_surplus': '+500 calories',
                'timeline': '12-16 weeks to reach healthy weight',
                'tips': [
                    'Eat 5-6 meals per day',
                    'Include protein in every meal',
                    'Add healthy fats (nuts, avocado, olive oil)',
                    'Drink calorie-rich smoothies',
                    'Strength training to build muscle'
                ]
            }
        elif category == 'Overweight':
            return {
                'goal': 'Lose weight gradually',
                'weekly_target': '-0.5 kg per week',
                'daily_deficit': '-500 calories',
                'timeline': '12-20 weeks to reach healthy weight',
                'tips': [
                    'Reduce portion sizes by 20%',
                    'Cut out sugary drinks',
                    'Increase vegetable intake',
                    'Eat protein with each meal',
                    'Track your food intake'
                ]
            }
        elif category == 'Obese':
            return {
                'goal': 'Significant weight loss',
                'weekly_target': '-0.5 to -1 kg per week',
                'daily_deficit': '-500 to -750 calories',
                'timeline': '24-52 weeks for substantial improvement',
                'tips': [
                    'Consult with a healthcare provider',
                    'Start with small, sustainable changes',
                    'Focus on whole foods',
                    'Eliminate processed foods',
                    'Consider working with a nutritionist',
                    'Join a support group'
                ]
            }
        else:
            return {
                'goal': 'Maintain healthy weight',
                'weekly_target': 'Maintain current weight',
                'daily_deficit': '0 calories (maintenance)',
                'timeline': 'Ongoing',
                'tips': [
                    'Continue balanced eating',
                    'Stay active regularly',
                    'Monitor weight monthly',
                    'Adjust calories if needed',
                    'Focus on overall health'
                ]
            }

    
    def _explain_bmi(self, bmi: float, category: str) -> Dict:
        """Explain BMI calculation and meaning"""
        return {
            'formula': 'BMI = weight (kg) / (height (m))²',
            'your_calculation': f'Your BMI of {bmi} indicates you are in the {category} category',
            'what_it_means': self._get_bmi_meaning(category),
            'why_this_value': self._explain_why_bmi(bmi, category),
            'health_implications': self._get_health_implications(category)
        }
    
    def _get_bmi_meaning(self, category: str) -> str:
        meanings = {
            'Underweight': 'Your body weight is below the healthy range. This may indicate insufficient nutrition or underlying health issues.',
            'Normal': 'Your body weight is within the healthy range. This is associated with lower risk of weight-related health problems.',
            'Overweight': 'Your body weight is above the healthy range. This increases risk of certain health conditions.',
            'Obese': 'Your body weight is significantly above the healthy range. This substantially increases health risks.'
        }
        return meanings.get(category, '')
    
    def _explain_why_bmi(self, bmi: float, category: str) -> str:
        if category == 'Underweight':
            return f'Your BMI of {bmi} is below 18.5, suggesting your body weight is low relative to your height. This could be due to high metabolism, insufficient calorie intake, or medical conditions.'
        elif category == 'Normal':
            return f'Your BMI of {bmi} falls between 18.5-24.9, indicating a healthy balance between your height and weight. This range is associated with optimal health outcomes.'
        elif category == 'Overweight':
            return f'Your BMI of {bmi} is between 25-29.9, indicating excess body weight. This typically results from consuming more calories than your body burns over time.'
        else:
            return f'Your BMI of {bmi} is 30 or above, indicating significant excess body weight. This usually develops from long-term positive energy balance (calories in > calories out).'
    
    def _get_health_implications(self, category: str) -> List[str]:
        implications = {
            'Underweight': [
                'Weakened immune system',
                'Nutritional deficiencies',
                'Decreased bone density',
                'Fertility issues',
                'Slower wound healing'
            ],
            'Normal': [
                'Lower risk of chronic diseases',
                'Better cardiovascular health',
                'Improved energy levels',
                'Optimal metabolic function',
                'Better quality of life'
            ],
            'Overweight': [
                'Increased risk of type 2 diabetes',
                'Higher blood pressure',
                'Elevated cholesterol',
                'Joint stress and pain',
                'Sleep apnea risk'
            ],
            'Obese': [
                'High risk of heart disease',
                'Type 2 diabetes',
                'Certain cancers',
                'Stroke risk',
                'Severe joint problems',
                'Respiratory issues'
            ]
        }
        return implications.get(category, [])

    
    def get_loan_recommendations(self, amount: float, rate: float, duration: int, emi: float) -> Dict:
        """Generate AI-powered loan recommendations"""
        return {
            'best_tenure': self._suggest_best_tenure(amount, rate, emi),
            'future_rates': self._predict_future_rates(rate),
            'prepayment_strategy': self._generate_prepayment_strategy(amount, rate, duration, emi),
            'explanation': self._explain_loan(amount, rate, duration, emi),
            'visual_insight': self._get_visual_insight('loan', emi, 'EMI Analysis')
        }
    
    def _suggest_best_tenure(self, amount: float, rate: float, emi: float) -> Dict:
        """Suggest optimal loan tenure"""
        # Calculate EMI for different tenures
        tenures = []
        for years in [5, 10, 15, 20, 25, 30]:
            months = years * 12
            monthly_rate = rate / (12 * 100)
            if monthly_rate > 0:
                calculated_emi = (amount * monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)
            else:
                calculated_emi = amount / months
            total_payment = calculated_emi * months
            total_interest = total_payment - amount
            
            tenures.append({
                'years': years,
                'monthly_emi': round(calculated_emi, 2),
                'total_interest': round(total_interest, 2),
                'total_payment': round(total_payment, 2),
                'affordability': 'High' if calculated_emi < emi * 0.8 else 'Medium' if calculated_emi < emi * 1.2 else 'Low'
            })
        
        return {
            'options': tenures,
            'recommendation': 'Choose shorter tenure if you can afford higher EMI to save on interest',
            'best_option': min(tenures, key=lambda x: x['total_interest'])
        }
    
    def _predict_future_rates(self, current_rate: float) -> Dict:
        """Predict future interest rate trends"""
        return {
            'current_rate': current_rate,
            'trend': 'stable' if 5 <= current_rate <= 8 else 'high' if current_rate > 8 else 'low',
            'predictions': {
                '6_months': round(current_rate + 0.25, 2),
                '1_year': round(current_rate + 0.5, 2),
                '2_years': round(current_rate + 0.75, 2)
            },
            'advice': 'Consider fixed rate if rates are expected to rise' if current_rate < 7 else 'Current rates are moderate, good time to lock in'
        }
    
    def _generate_prepayment_strategy(self, amount: float, rate: float, duration: int, emi: float) -> Dict:
        """Generate prepayment strategy"""
        return {
            'strategy': 'Aggressive Prepayment',
            'recommendations': [
                f'Pay extra ${round(emi * 0.1, 2)} per month to save significantly on interest',
                'Make lump sum payments from bonuses or tax refunds',
                'Prepay during initial years for maximum impact',
                f'Could reduce loan tenure by {round(duration * 0.2)} years with 10% extra payment'
            ],
            'savings_potential': {
                '10_percent_extra': f'Save approximately ${round(amount * rate * 0.15 / 100, 2)} in interest',
                '20_percent_extra': f'Save approximately ${round(amount * rate * 0.25 / 100, 2)} in interest'
            }
        }
    
    def _explain_loan(self, amount: float, rate: float, duration: int, emi: float) -> Dict:
        """Explain loan calculation"""
        return {
            'formula': 'EMI = [P × R × (1+R)^N] / [(1+R)^N-1]',
            'components': {
                'P': f'Principal Amount = ${amount}',
                'R': f'Monthly Interest Rate = {rate}% / 12 = {round(rate/12, 4)}%',
                'N': f'Number of Months = {duration} years × 12 = {duration * 12} months'
            },
            'breakdown': f'Your EMI of ${emi} includes both principal and interest. Initially, more goes to interest, but over time, more goes to principal.',
            'why_this_value': f'The EMI is calculated to ensure the loan is fully repaid in {duration} years with equal monthly payments.'
        }

    
    def get_gpa_recommendations(self, gpa: float, courses: List[Dict]) -> Dict:
        """Generate AI-powered GPA recommendations"""
        return {
            'focus_subjects': self._suggest_focus_subjects(courses),
            'predicted_gpa': self._predict_final_gpa(gpa, courses),
            'improvement_plan': self._generate_improvement_plan(gpa),
            'explanation': self._explain_gpa(gpa, courses),
            'visual_insight': self._get_visual_insight('gpa', gpa, 'Academic Performance')
        }
    
    def _suggest_focus_subjects(self, courses: List[Dict]) -> List[Dict]:
        """Suggest which subjects to focus on"""
        grade_points = {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'F': 0.0
        }
        
        focus_list = []
        for course in courses:
            grade = course.get('grade', 'C')
            credits = float(course.get('credits', 3))
            points = grade_points.get(grade, 2.0)
            
            if points < 3.0:
                focus_list.append({
                    'course': course.get('name', 'Course'),
                    'current_grade': grade,
                    'credits': credits,
                    'priority': 'High' if points < 2.0 else 'Medium',
                    'potential_impact': round(credits * (3.0 - points), 2),
                    'recommendation': 'Needs immediate attention' if points < 2.0 else 'Room for improvement'
                })
        
        return sorted(focus_list, key=lambda x: x['potential_impact'], reverse=True)
    
    def _predict_final_gpa(self, current_gpa: float, courses: List[Dict]) -> Dict:
        """Predict final GPA with improvements"""
        return {
            'current_gpa': current_gpa,
            'if_maintain': round(current_gpa, 2),
            'if_improve_10_percent': round(min(current_gpa * 1.1, 4.0), 2),
            'if_improve_20_percent': round(min(current_gpa * 1.2, 4.0), 2),
            'realistic_target': round(min(current_gpa + 0.3, 4.0), 2),
            'timeline': 'Next 2 semesters with focused effort'
        }
    
    def _generate_improvement_plan(self, gpa: float) -> Dict:
        """Generate GPA improvement plan"""
        if gpa >= 3.5:
            return {
                'status': 'Excellent',
                'goal': 'Maintain and excel',
                'strategies': [
                    'Continue current study habits',
                    'Take on leadership roles',
                    'Consider advanced courses',
                    'Mentor other students',
                    'Focus on research opportunities'
                ]
            }
        elif gpa >= 3.0:
            return {
                'status': 'Good',
                'goal': 'Push towards excellence',
                'strategies': [
                    'Identify and strengthen weak subjects',
                    'Form study groups',
                    'Attend office hours regularly',
                    'Improve time management',
                    'Set specific grade goals per course'
                ]
            }
        elif gpa >= 2.5:
            return {
                'status': 'Average',
                'goal': 'Significant improvement needed',
                'strategies': [
                    'Meet with academic advisor',
                    'Create structured study schedule',
                    'Use tutoring services',
                    'Reduce extracurricular commitments',
                    'Focus on understanding, not memorizing',
                    'Start assignments early'
                ]
            }
        else:
            return {
                'status': 'Needs Attention',
                'goal': 'Immediate intervention required',
                'strategies': [
                    'Seek academic counseling immediately',
                    'Consider reducing course load',
                    'Get professional tutoring',
                    'Address any personal issues affecting studies',
                    'Create daily study routine',
                    'Meet with professors for extra help'
                ]
            }
    
    def _explain_gpa(self, gpa: float, courses: List[Dict]) -> Dict:
        """Explain GPA calculation"""
        return {
            'formula': 'GPA = (Sum of Grade Points × Credits) / Total Credits',
            'your_calculation': f'Your GPA of {gpa} is calculated by averaging all course grades weighted by credits',
            'what_it_means': self._get_gpa_meaning(gpa),
            'why_this_value': f'Your GPA reflects your overall academic performance across all courses',
            'scale': 'GPA is on a 4.0 scale where A=4.0, B=3.0, C=2.0, D=1.0, F=0.0'
        }
    
    def _get_gpa_meaning(self, gpa: float) -> str:
        if gpa >= 3.7:
            return 'Outstanding academic performance. You are in the top tier of students.'
        elif gpa >= 3.3:
            return 'Excellent performance. You are well above average.'
        elif gpa >= 3.0:
            return 'Good performance. You are meeting academic standards well.'
        elif gpa >= 2.5:
            return 'Satisfactory performance. There is room for improvement.'
        elif gpa >= 2.0:
            return 'Below average performance. Significant improvement needed.'
        else:
            return 'Poor performance. Immediate action required to improve.'

    
    def _get_visual_insight(self, calculator_type: str, value: float, context: str) -> Dict:
        """Generate visual insights"""
        insights = {
            'bmi': {
                'chart_type': 'gauge',
                'ranges': [
                    {'min': 0, 'max': 18.5, 'label': 'Underweight', 'color': '#3498db'},
                    {'min': 18.5, 'max': 25, 'label': 'Normal', 'color': '#2ecc71'},
                    {'min': 25, 'max': 30, 'label': 'Overweight', 'color': '#f39c12'},
                    {'min': 30, 'max': 50, 'label': 'Obese', 'color': '#e74c3c'}
                ],
                'your_position': value,
                'interpretation': f'Your BMI of {value} places you in a specific health category'
            },
            'loan': {
                'chart_type': 'breakdown',
                'message': f'Your EMI of ${value} will be split between principal and interest over time',
                'tip': 'Early payments go mostly to interest, later payments to principal'
            },
            'gpa': {
                'chart_type': 'progress',
                'scale': 4.0,
                'your_score': value,
                'percentage': round((value / 4.0) * 100, 1),
                'message': f'You are at {round((value / 4.0) * 100, 1)}% of the maximum GPA'
            }
        }
        return insights.get(calculator_type, {'message': 'Visual representation of your results'})
    
    def chat_with_ai(self, message: str, calculator_type: str, context: Dict = None) -> str:
        """AI Chatbot for answering questions"""
        # Predefined responses for common questions
        responses = {
            'bmi': {
                'how to calculate': 'BMI is calculated by dividing your weight in kilograms by the square of your height in meters: BMI = weight(kg) / height(m)²',
                'what is bmi': 'BMI (Body Mass Index) is a measure of body fat based on height and weight that applies to adult men and women.',
                'is bmi accurate': 'BMI is a useful screening tool but has limitations. It doesn\'t account for muscle mass, bone density, or fat distribution.',
                'how to improve': 'To improve your BMI, focus on balanced nutrition, regular exercise, adequate sleep, and stress management.',
            },
            'loan': {
                'what is emi': 'EMI (Equated Monthly Installment) is the fixed amount you pay every month to repay your loan, including both principal and interest.',
                'how to reduce emi': 'You can reduce EMI by: 1) Increasing loan tenure, 2) Making a larger down payment, 3) Negotiating lower interest rate, or 4) Making prepayments.',
                'prepayment': 'Prepayment means paying extra towards your loan principal. This reduces total interest and can shorten loan duration.',
                'interest rate': 'Interest rate is the cost of borrowing money, expressed as a percentage of the loan amount per year.',
            },
            'gpa': {
                'how to calculate': 'GPA is calculated by multiplying each grade\'s point value by credits, summing these, and dividing by total credits.',
                'what is good gpa': 'Generally, 3.5+ is excellent, 3.0-3.5 is good, 2.5-3.0 is average, and below 2.5 needs improvement.',
                'how to improve': 'Improve GPA by: attending all classes, studying regularly, seeking help when needed, managing time well, and staying organized.',
                'grade scale': 'Typically: A=4.0, A-=3.7, B+=3.3, B=3.0, B-=2.7, C+=2.3, C=2.0, C-=1.7, D=1.0, F=0.0',
            }
        }
        
        # Simple keyword matching
        message_lower = message.lower()
        calc_responses = responses.get(calculator_type, {})
        
        for key, response in calc_responses.items():
            if key in message_lower:
                return response
        
        # Default responses
        default_responses = {
            'bmi': 'I can help you understand BMI calculations, health implications, and improvement strategies. What would you like to know?',
            'loan': 'I can explain EMI calculations, interest rates, prepayment strategies, and loan optimization. How can I assist you?',
            'gpa': 'I can help with GPA calculations, grade improvements, and academic planning. What\'s your question?',
            'calorie': 'I can explain calorie needs, weight management, and nutrition planning. What would you like to know?',
        }
        
        return default_responses.get(calculator_type, 'I\'m here to help! Please ask me about calculations, formulas, or recommendations.')
    
    def get_smart_explanation(self, calculator_type: str, result: Dict, inputs: Dict) -> Dict:
        """Generate smart explanation for any calculator"""
        explanations = {
            'bmi': self._explain_bmi(result.get('bmi', 0), result.get('category', 'Normal')),
            'loan': self._explain_loan(
                inputs.get('amount', 0),
                inputs.get('rate', 0),
                inputs.get('duration', 0),
                result.get('emi', 0)
            ),
            'gpa': self._explain_gpa(result.get('gpa', 0), inputs.get('courses', []))
        }
        
        return explanations.get(calculator_type, {
            'formula': 'Calculation formula',
            'explanation': 'Detailed explanation of your results',
            'interpretation': 'What your results mean'
        })
