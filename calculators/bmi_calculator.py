"""
Professional BMI (Body Mass Index) Calculator Module
Provides comprehensive body composition analysis and health metrics
"""

from typing import Dict, Union, Optional, List
from decimal import Decimal, ROUND_HALF_UP
import math


class BMICalculationError(Exception):
    """Custom exception for BMI calculation errors"""
    pass


def calculate_bmi(
    height: float,
    weight: float,
    age: Optional[int] = None,
    gender: Optional[str] = None,
    unit_system: str = "metric",
    waist_circumference: Optional[float] = None,
    hip_circumference: Optional[float] = None,
    detailed: bool = False
) -> Dict[str, Union[float, str, Dict, List]]:
    """
    Calculate comprehensive BMI with detailed health analysis
    
    Args:
        height: Height in cm (metric) or inches (imperial)
        weight: Weight in kg (metric) or lbs (imperial)
        age: Optional age for age-specific analysis
        gender: Optional gender ('male' or 'female') for detailed metrics
        unit_system: 'metric' or 'imperial'
        waist_circumference: Optional waist measurement in cm or inches
        hip_circumference: Optional hip measurement in cm or inches
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing comprehensive BMI analysis and health metrics
    
    Raises:
        BMICalculationError: If input parameters are invalid
    """
    # Validate inputs
    if height <= 0:
        raise BMICalculationError("Height must be greater than zero.")
    if weight <= 0:
        raise BMICalculationError("Weight must be greater than zero.")
    if unit_system.lower() not in ['metric', 'imperial']:
        raise BMICalculationError("Unit system must be 'metric' or 'imperial'.")
    if age is not None and (age <= 0 or age > 120):
        raise BMICalculationError("Age must be between 1 and 120 years.")
    if gender is not None and gender.lower() not in ['male', 'female']:
        raise BMICalculationError("Gender must be 'male' or 'female'.")
    
    # Convert imperial to metric if needed
    original_unit = unit_system.lower()
    if original_unit == 'imperial':
        height_cm = height * 2.54  # inches to cm
        weight_kg = weight * 0.453592  # lbs to kg
        if waist_circumference:
            waist_circumference = waist_circumference * 2.54
        if hip_circumference:
            hip_circumference = hip_circumference * 2.54
    else:
        height_cm = height
        weight_kg = weight
    
    # Additional validation for metric values
    if height_cm < 50 or height_cm > 300:
        raise BMICalculationError("Height must be between 50-300 cm (20-118 inches).")
    if weight_kg < 20 or weight_kg > 500:
        raise BMICalculationError("Weight must be between 20-500 kg (44-1100 lbs).")
    
    # Calculate BMI
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)
    bmi = round(bmi, 2)
    
    # Determine BMI category and health risk
    category_info = get_bmi_category(bmi, age)
    
    # Calculate ideal weight range
    ideal_weight = calculate_ideal_weight(height_cm, gender)
    
    # Calculate weight goals
    weight_goals = calculate_weight_goals(weight_kg, height_cm, bmi)
    
    # Calculate body surface area (BSA)
    bsa = calculate_body_surface_area(height_cm, weight_kg)
    
    # Calculate ponderal index (for more accurate assessment)
    ponderal_index = calculate_ponderal_index(height_cm, weight_kg)
    
    # Additional body composition metrics
    body_composition = {}
    if waist_circumference and hip_circumference:
        body_composition = calculate_body_ratios(waist_circumference, hip_circumference, gender)
    
    # Health risk assessment
    health_risks = assess_health_risks(bmi, age, gender, waist_circumference)
    
    # Caloric recommendations
    caloric_needs = estimate_caloric_needs(weight_kg, height_cm, age, gender, bmi)
    
    # BMI prime (BMI divided by upper limit of normal BMI)
    bmi_prime = round(bmi / 25, 2)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'bmi': bmi,
            'category': category_info['category'],
            'color': category_info['color']
        }
    
    return {
        'bmi': bmi,
        'bmi_prime': bmi_prime,
        'category': category_info['category'],
        'category_description': category_info['description'],
        'health_risk': category_info['health_risk'],
        'color': category_info['color'],
        'ideal_weight_range': ideal_weight,
        'weight_goals': weight_goals,
        'body_metrics': {
            'body_surface_area_m2': bsa,
            'ponderal_index': ponderal_index,
            'bmi_percentile': get_bmi_percentile(bmi, age, gender) if age and gender else None
        },
        'body_composition': body_composition if body_composition else None,
        'health_risk_assessment': health_risks,
        'caloric_recommendations': caloric_needs,
        'input_parameters': {
            'height_cm': round(height_cm, 2),
            'height_inches': round(height_cm / 2.54, 2),
            'weight_kg': round(weight_kg, 2),
            'weight_lbs': round(weight_kg * 2.20462, 2),
            'age': age,
            'gender': gender.lower() if gender else None
        },
        'recommendations': generate_recommendations(bmi, category_info['category'], age),
        'notes': [
            'BMI is a screening tool, not a diagnostic measure',
            'Athletes and muscular individuals may have high BMI despite low body fat',
            'Consult healthcare provider for personalized health assessment',
            'BMI may not be accurate for children, elderly, or pregnant women'
        ]
    }


def get_bmi_category(bmi: float, age: Optional[int]) -> Dict:
    """Determine BMI category with health risk assessment"""
    if age and age < 20:
        # For children/teens, use percentile-based categories (simplified)
        return {
            'category': 'See pediatric BMI chart',
            'description': 'BMI interpretation differs for individuals under 20',
            'health_risk': 'Consult pediatrician',
            'color': '#95a5a6'
        }
    
    if bmi < 16:
        return {
            'category': 'Severe Underweight',
            'description': 'Significantly below healthy weight',
            'health_risk': 'High risk - malnutrition, weakened immunity',
            'color': '#3498db'
        }
    elif 16 <= bmi < 17:
        return {
            'category': 'Moderate Underweight',
            'description': 'Below healthy weight',
            'health_risk': 'Moderate risk - nutritional deficiency',
            'color': '#5dade2'
        }
    elif 17 <= bmi < 18.5:
        return {
            'category': 'Mild Underweight',
            'description': 'Slightly below healthy weight',
            'health_risk': 'Low to moderate risk',
            'color': '#85c1e9'
        }
    elif 18.5 <= bmi < 25:
        return {
            'category': 'Normal Weight',
            'description': 'Healthy weight range',
            'health_risk': 'Low risk - optimal health range',
            'color': '#2ecc71'
        }
    elif 25 <= bmi < 30:
        return {
            'category': 'Overweight',
            'description': 'Above healthy weight',
            'health_risk': 'Moderate risk - increased disease risk',
            'color': '#f39c12'
        }
    elif 30 <= bmi < 35:
        return {
            'category': 'Obese Class I',
            'description': 'Moderately obese',
            'health_risk': 'High risk - cardiovascular, diabetes',
            'color': '#e67e22'
        }
    elif 35 <= bmi < 40:
        return {
            'category': 'Obese Class II',
            'description': 'Severely obese',
            'health_risk': 'Very high risk - serious health complications',
            'color': '#d35400'
        }
    else:
        return {
            'category': 'Obese Class III',
            'description': 'Morbidly obese',
            'health_risk': 'Extremely high risk - life-threatening conditions',
            'color': '#e74c3c'
        }


def calculate_ideal_weight(height_cm: float, gender: Optional[str]) -> Dict:
    """Calculate ideal weight range using multiple methods"""
    height_m = height_cm / 100
    
    # WHO healthy BMI range (18.5-24.9)
    min_healthy = 18.5 * (height_m ** 2)
    max_healthy = 24.9 * (height_m ** 2)
    
    # Hamwi formula
    if gender:
        if gender.lower() == 'male':
            hamwi = 48 + 2.7 * ((height_cm / 2.54) - 60)
        else:
            hamwi = 45.5 + 2.2 * ((height_cm / 2.54) - 60)
    else:
        hamwi = None
    
    # Devine formula
    if gender:
        if gender.lower() == 'male':
            devine = 50 + 2.3 * ((height_cm / 2.54) - 60)
        else:
            devine = 45.5 + 2.3 * ((height_cm / 2.54) - 60)
    else:
        devine = None
    
    # Robinson formula
    if gender:
        if gender.lower() == 'male':
            robinson = 52 + 1.9 * ((height_cm / 2.54) - 60)
        else:
            robinson = 49 + 1.7 * ((height_cm / 2.54) - 60)
    else:
        robinson = None
    
    result = {
        'healthy_bmi_range': {
            'min_kg': round(min_healthy, 1),
            'max_kg': round(max_healthy, 1),
            'min_lbs': round(min_healthy * 2.20462, 1),
            'max_lbs': round(max_healthy * 2.20462, 1)
        }
    }
    
    if hamwi:
        result['hamwi_formula_kg'] = round(hamwi, 1)
    if devine:
        result['devine_formula_kg'] = round(devine, 1)
    if robinson:
        result['robinson_formula_kg'] = round(robinson, 1)
    
    return result


def calculate_weight_goals(current_weight: float, height_cm: float, current_bmi: float) -> Dict:
    """Calculate weight needed to reach different BMI categories"""
    height_m = height_cm / 100
    
    goals = {
        'to_normal_max': {
            'target_bmi': 24.9,
            'weight_kg': round(24.9 * (height_m ** 2), 1),
            'change_kg': None,
            'description': 'Upper limit of normal weight'
        },
        'to_normal_mid': {
            'target_bmi': 21.7,
            'weight_kg': round(21.7 * (height_m ** 2), 1),
            'change_kg': None,
            'description': 'Middle of normal weight range'
        },
        'to_normal_min': {
            'target_bmi': 18.5,
            'weight_kg': round(18.5 * (height_m ** 2), 1),
            'change_kg': None,
            'description': 'Lower limit of normal weight'
        }
    }
    
    for goal in goals.values():
        change = goal['weight_kg'] - current_weight
        goal['change_kg'] = round(change, 1)
        goal['change_lbs'] = round(change * 2.20462, 1)
        goal['weeks_to_goal'] = abs(round(change / 0.5, 0)) if change != 0 else 0
    
    return goals


def calculate_body_surface_area(height_cm: float, weight_kg: float) -> float:
    """Calculate BSA using Mosteller formula"""
    bsa = math.sqrt((height_cm * weight_kg) / 3600)
    return round(bsa, 2)


def calculate_ponderal_index(height_cm: float, weight_kg: float) -> float:
    """Calculate Ponderal Index (alternative to BMI)"""
    height_m = height_cm / 100
    pi = weight_kg / (height_m ** 3)
    return round(pi, 2)


def calculate_body_ratios(waist: float, hip: float, gender: Optional[str]) -> Dict:
    """Calculate waist-to-hip ratio and assess health risk"""
    whr = waist / hip
    whr = round(whr, 2)
    
    # Determine risk based on gender
    if gender:
        if gender.lower() == 'male':
            if whr < 0.90:
                risk = 'Low risk'
            elif whr < 1.0:
                risk = 'Moderate risk'
            else:
                risk = 'High risk'
        else:  # female
            if whr < 0.80:
                risk = 'Low risk'
            elif whr < 0.85:
                risk = 'Moderate risk'
            else:
                risk = 'High risk'
    else:
        risk = 'Unknown (gender not specified)'
    
    return {
        'waist_to_hip_ratio': whr,
        'health_risk': risk,
        'waist_cm': round(waist, 1),
        'hip_cm': round(hip, 1),
        'note': 'WHR indicates body fat distribution and cardiovascular risk'
    }


def assess_health_risks(bmi: float, age: Optional[int], gender: Optional[str], waist: Optional[float]) -> Dict:
    """Comprehensive health risk assessment"""
    risks = []
    
    if bmi < 18.5:
        risks.extend(['Malnutrition', 'Weakened immune system', 'Osteoporosis', 'Anemia'])
    elif 25 <= bmi < 30:
        risks.extend(['Type 2 diabetes', 'High blood pressure', 'Heart disease', 'Sleep apnea'])
    elif bmi >= 30:
        risks.extend(['Type 2 diabetes', 'Heart disease', 'Stroke', 'Certain cancers', 
                     'Osteoarthritis', 'Sleep apnea', 'Fatty liver disease'])
    
    # Waist circumference risk
    waist_risk = None
    if waist and gender:
        if gender.lower() == 'male' and waist > 102:
            waist_risk = 'High risk - waist circumference exceeds 102 cm'
        elif gender.lower() == 'female' and waist > 88:
            waist_risk = 'High risk - waist circumference exceeds 88 cm'
        else:
            waist_risk = 'Normal - waist circumference within healthy range'
    
    return {
        'potential_health_risks': risks if risks else ['Low risk - maintain healthy lifestyle'],
        'waist_circumference_risk': waist_risk,
        'recommendation': 'Consult healthcare provider for personalized assessment'
    }


def estimate_caloric_needs(weight: float, height: float, age: Optional[int], 
                           gender: Optional[str], bmi: float) -> Dict:
    """Estimate daily caloric needs based on BMI goals"""
    if not age or not gender:
        return {'note': 'Age and gender required for caloric estimation'}
    
    # Calculate BMR (using Mifflin-St Jeor)
    if gender.lower() == 'male':
        bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
    
    maintenance = bmr * 1.55  # Moderate activity
    
    return {
        'maintenance_calories': round(maintenance, 0),
        'weight_loss_calories': round(maintenance - 500, 0),
        'weight_gain_calories': round(maintenance + 500, 0),
        'note': 'Based on moderate activity level (3-5 days/week exercise)'
    }


def get_bmi_percentile(bmi: float, age: Optional[int], gender: Optional[str]) -> str:
    """Estimate BMI percentile (simplified)"""
    if not age or not gender or age >= 20:
        return 'N/A (for ages 2-19 only)'
    
    # This is a simplified estimation - real percentiles require CDC growth charts
    return 'Consult pediatric BMI percentile charts for accurate assessment'


def generate_recommendations(bmi: float, category: str, age: Optional[int]) -> List[str]:
    """Generate personalized health recommendations"""
    recommendations = []
    
    if bmi < 18.5:
        recommendations.extend([
            'Increase caloric intake with nutrient-dense foods',
            'Include protein-rich foods in every meal',
            'Consider strength training to build muscle mass',
            'Consult a nutritionist for personalized meal plan',
            'Rule out underlying medical conditions'
        ])
    elif 18.5 <= bmi < 25:
        recommendations.extend([
            'Maintain current healthy weight through balanced diet',
            'Engage in regular physical activity (150 min/week)',
            'Stay hydrated with 8-10 glasses of water daily',
            'Get adequate sleep (7-9 hours per night)',
            'Regular health check-ups'
        ])
    elif 25 <= bmi < 30:
        recommendations.extend([
            'Create a moderate caloric deficit (500 cal/day)',
            'Increase physical activity to 200-300 min/week',
            'Focus on whole foods, reduce processed foods',
            'Practice portion control',
            'Track food intake and exercise',
            'Consider consulting a dietitian'
        ])
    else:  # BMI >= 30
        recommendations.extend([
            'Consult healthcare provider for comprehensive weight management plan',
            'Consider medically supervised weight loss program',
            'Start with low-impact exercises (walking, swimming)',
            'Focus on sustainable lifestyle changes',
            'Address emotional eating patterns',
            'Regular monitoring of blood pressure, blood sugar',
            'Consider support groups or counseling'
        ])
    
    # Age-specific recommendations
    if age:
        if age > 65:
            recommendations.append('Focus on maintaining muscle mass and bone density')
        elif age < 20:
            recommendations.append('Consult pediatrician for age-appropriate guidance')
    
    return recommendations
