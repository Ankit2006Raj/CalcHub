"""
Professional BMR (Basal Metabolic Rate) Calculator Module
Provides comprehensive metabolic rate calculations using multiple formulas
"""

from typing import Dict, Union, Optional
from decimal import Decimal, ROUND_HALF_UP


class BMRCalculationError(Exception):
    """Custom exception for BMR calculation errors"""
    pass


def calculate_bmr(
    gender: str,
    age: int,
    height: float,
    weight: float,
    formula: str = "harris-benedict",
    body_fat_percentage: Optional[float] = None,
    unit_system: str = "metric",
    detailed: bool = False
) -> Dict[str, Union[float, str, Dict]]:
    """
    Calculate comprehensive BMR using multiple formulas and activity levels
    
    Args:
        gender: 'male' or 'female'
        age: Age in years
        height: Height in cm (metric) or inches (imperial)
        weight: Weight in kg (metric) or lbs (imperial)
        formula: Calculation formula - 'harris-benedict', 'mifflin-st-jeor', 'katch-mcardle'
        body_fat_percentage: Optional body fat % (required for Katch-McArdle)
        unit_system: 'metric' or 'imperial'
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed BMR and caloric needs
    
    Raises:
        BMRCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if gender.lower() not in ['male', 'female']:
        raise BMRCalculationError("Gender must be 'male' or 'female'.")
    if age <= 0 or age > 120:
        raise BMRCalculationError("Age must be between 1 and 120 years.")
    if height <= 0:
        raise BMRCalculationError("Height must be greater than zero.")
    if weight <= 0:
        raise BMRCalculationError("Weight must be greater than zero.")
    if unit_system.lower() not in ['metric', 'imperial']:
        raise BMRCalculationError("Unit system must be 'metric' or 'imperial'.")
    
    # Convert imperial to metric if needed
    if unit_system.lower() == 'imperial':
        height = height * 2.54  # inches to cm
        weight = weight * 0.453592  # lbs to kg
    
    # Additional validation for metric values
    if height < 50 or height > 300:
        raise BMRCalculationError("Height must be between 50-300 cm.")
    if weight < 20 or weight > 500:
        raise BMRCalculationError("Weight must be between 20-500 kg.")
    
    # Calculate BMR using selected formula
    formula_lower = formula.lower()
    
    if formula_lower == "harris-benedict":
        bmr = calculate_harris_benedict(gender.lower(), age, height, weight)
        formula_name = "Harris-Benedict Equation (Revised)"
    elif formula_lower == "mifflin-st-jeor":
        bmr = calculate_mifflin_st_jeor(gender.lower(), age, height, weight)
        formula_name = "Mifflin-St Jeor Equation"
    elif formula_lower == "katch-mcardle":
        if body_fat_percentage is None:
            raise BMRCalculationError("Body fat percentage required for Katch-McArdle formula.")
        if body_fat_percentage < 3 or body_fat_percentage > 60:
            raise BMRCalculationError("Body fat percentage must be between 3-60%.")
        bmr = calculate_katch_mcardle(weight, body_fat_percentage)
        formula_name = "Katch-McArdle Formula"
    else:
        raise BMRCalculationError("Invalid formula. Choose 'harris-benedict', 'mifflin-st-jeor', or 'katch-mcardle'.")
    
    # Calculate TDEE (Total Daily Energy Expenditure) for different activity levels
    activity_multipliers = {
        'sedentary': {
            'multiplier': 1.2,
            'description': 'Little or no exercise, desk job'
        },
        'lightly_active': {
            'multiplier': 1.375,
            'description': 'Light exercise 1-3 days/week'
        },
        'moderately_active': {
            'multiplier': 1.55,
            'description': 'Moderate exercise 3-5 days/week'
        },
        'very_active': {
            'multiplier': 1.725,
            'description': 'Hard exercise 6-7 days/week'
        },
        'extremely_active': {
            'multiplier': 1.9,
            'description': 'Very hard exercise, physical job, training twice/day'
        }
    }
    
    tdee_levels = {}
    for level, data in activity_multipliers.items():
        tdee_levels[level] = {
            'calories': round(bmr * data['multiplier'], 2),
            'description': data['description'],
            'multiplier': data['multiplier']
        }
    
    # Calculate caloric needs for different goals
    caloric_goals = calculate_caloric_goals(bmr, tdee_levels['moderately_active']['calories'])
    
    # Calculate macronutrient recommendations
    macros = calculate_macronutrients(tdee_levels['moderately_active']['calories'])
    
    # Calculate comparison with other formulas
    formula_comparison = compare_formulas(gender.lower(), age, height, weight, body_fat_percentage)
    
    # Health metrics and recommendations
    health_metrics = calculate_health_metrics(bmr, age, gender.lower(), weight, height)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'bmr': round(bmr, 2),
            'sedentary': tdee_levels['sedentary']['calories'],
            'light': tdee_levels['lightly_active']['calories'],
            'moderate': tdee_levels['moderately_active']['calories'],
            'active': tdee_levels['very_active']['calories'],
            'very_active': tdee_levels['extremely_active']['calories']
        }
    
    return {
        'bmr': round(bmr, 2),
        'formula_used': formula_name,
        'tdee_by_activity': tdee_levels,
        'caloric_goals': caloric_goals,
        'macronutrient_recommendations': macros,
        'formula_comparison': formula_comparison,
        'health_metrics': health_metrics,
        'input_parameters': {
            'gender': gender.lower(),
            'age': age,
            'height_cm': round(height, 2),
            'weight_kg': round(weight, 2),
            'body_fat_percentage': body_fat_percentage
        },
        'notes': [
            'BMR represents calories burned at complete rest',
            'TDEE includes daily activity and exercise',
            'Individual metabolism may vary by ±10-15%',
            'Consult healthcare provider for personalized advice'
        ]
    }


def calculate_harris_benedict(gender: str, age: int, height: float, weight: float) -> float:
    """Harris-Benedict Equation (Revised 1984)"""
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    return bmr


def calculate_mifflin_st_jeor(gender: str, age: int, height: float, weight: float) -> float:
    """Mifflin-St Jeor Equation (More accurate for modern populations)"""
    bmr = (10 * weight) + (6.25 * height) - (5 * age)
    if gender == 'male':
        bmr += 5
    else:
        bmr -= 161
    return bmr


def calculate_katch_mcardle(weight: float, body_fat_percentage: float) -> float:
    """Katch-McArdle Formula (Based on lean body mass)"""
    lean_body_mass = weight * (1 - body_fat_percentage / 100)
    bmr = 370 + (21.6 * lean_body_mass)
    return bmr


def calculate_caloric_goals(bmr: float, maintenance_calories: float) -> Dict:
    """Calculate caloric needs for different fitness goals"""
    return {
        'extreme_weight_loss': {
            'calories': round(maintenance_calories - 1000, 2),
            'weekly_change': '-1 kg (-2 lbs)',
            'description': 'Aggressive deficit (not recommended without supervision)'
        },
        'weight_loss': {
            'calories': round(maintenance_calories - 500, 2),
            'weekly_change': '-0.5 kg (-1 lb)',
            'description': 'Moderate deficit for sustainable fat loss'
        },
        'mild_weight_loss': {
            'calories': round(maintenance_calories - 250, 2),
            'weekly_change': '-0.25 kg (-0.5 lbs)',
            'description': 'Small deficit for slow, steady weight loss'
        },
        'maintenance': {
            'calories': round(maintenance_calories, 2),
            'weekly_change': '0 kg (0 lbs)',
            'description': 'Maintain current weight'
        },
        'mild_weight_gain': {
            'calories': round(maintenance_calories + 250, 2),
            'weekly_change': '+0.25 kg (+0.5 lbs)',
            'description': 'Small surplus for lean muscle gain'
        },
        'weight_gain': {
            'calories': round(maintenance_calories + 500, 2),
            'weekly_change': '+0.5 kg (+1 lb)',
            'description': 'Moderate surplus for muscle building'
        }
    }


def calculate_macronutrients(calories: float) -> Dict:
    """Calculate macronutrient recommendations"""
    return {
        'balanced': {
            'protein': {'grams': round(calories * 0.30 / 4, 1), 'percentage': 30, 'calories': round(calories * 0.30, 1)},
            'carbs': {'grams': round(calories * 0.40 / 4, 1), 'percentage': 40, 'calories': round(calories * 0.40, 1)},
            'fats': {'grams': round(calories * 0.30 / 9, 1), 'percentage': 30, 'calories': round(calories * 0.30, 1)},
            'description': 'Balanced diet for general health'
        },
        'high_protein': {
            'protein': {'grams': round(calories * 0.40 / 4, 1), 'percentage': 40, 'calories': round(calories * 0.40, 1)},
            'carbs': {'grams': round(calories * 0.30 / 4, 1), 'percentage': 30, 'calories': round(calories * 0.30, 1)},
            'fats': {'grams': round(calories * 0.30 / 9, 1), 'percentage': 30, 'calories': round(calories * 0.30, 1)},
            'description': 'For muscle building and recovery'
        },
        'low_carb': {
            'protein': {'grams': round(calories * 0.35 / 4, 1), 'percentage': 35, 'calories': round(calories * 0.35, 1)},
            'carbs': {'grams': round(calories * 0.20 / 4, 1), 'percentage': 20, 'calories': round(calories * 0.20, 1)},
            'fats': {'grams': round(calories * 0.45 / 9, 1), 'percentage': 45, 'calories': round(calories * 0.45, 1)},
            'description': 'For fat loss and blood sugar control'
        }
    }


def compare_formulas(gender: str, age: int, height: float, weight: float, body_fat: Optional[float]) -> Dict:
    """Compare BMR across different formulas"""
    comparison = {
        'harris_benedict': round(calculate_harris_benedict(gender, age, height, weight), 2),
        'mifflin_st_jeor': round(calculate_mifflin_st_jeor(gender, age, height, weight), 2)
    }
    
    if body_fat is not None:
        comparison['katch_mcardle'] = round(calculate_katch_mcardle(weight, body_fat), 2)
    
    values = list(comparison.values())
    comparison['average'] = round(sum(values) / len(values), 2)
    comparison['range'] = round(max(values) - min(values), 2)
    comparison['note'] = 'Mifflin-St Jeor is generally considered most accurate for modern populations'
    
    return comparison


def calculate_health_metrics(bmr: float, age: int, gender: str, weight: float, height: float) -> Dict:
    """Calculate additional health and metabolic metrics"""
    # Calculate BMI
    bmi = weight / ((height / 100) ** 2)
    
    # Ideal weight range (using BMI 18.5-24.9)
    height_m = height / 100
    ideal_weight_min = 18.5 * (height_m ** 2)
    ideal_weight_max = 24.9 * (height_m ** 2)
    
    # Metabolic age estimation (simplified)
    if gender == 'male':
        expected_bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        expected_bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    
    metabolic_age_diff = round((expected_bmr - bmr) / 10, 1)
    
    return {
        'bmi': round(bmi, 2),
        'ideal_weight_range_kg': {
            'min': round(ideal_weight_min, 1),
            'max': round(ideal_weight_max, 1)
        },
        'metabolic_health': 'Good' if abs(metabolic_age_diff) < 5 else 'Needs attention',
        'daily_water_intake_liters': round(weight * 0.033, 1),
        'resting_heart_rate_estimate': '60-100 bpm (measure for accuracy)',
        'recommended_meal_frequency': '3-6 meals per day based on preference'
    }
