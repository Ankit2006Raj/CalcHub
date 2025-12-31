"""
Macros (Macronutrient) Calculator Module
Calculate daily protein, carbs, and fats based on goals
"""

from typing import Dict, Optional


def calculate_macros(
    weight: float,
    height: float,
    age: int,
    gender: str,
    activity_level: str,
    goal: str,
    weight_unit: str = 'kg'
) -> Dict:
    """
    Calculate daily macronutrient needs
    
    Args:
        weight: Body weight
        height: Height in cm
        age: Age in years
        gender: 'male' or 'female'
        activity_level: sedentary, light, moderate, active, very_active
        goal: lose_weight, maintain, gain_muscle
        weight_unit: 'kg' or 'lbs'
    
    Returns:
        Dictionary with macro calculations
    """
    # Convert to kg if needed
    if weight_unit == 'lbs':
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight
    
    # Calculate BMR (Mifflin-St Jeor)
    if gender.lower() == 'male':
        bmr = (10 * weight_kg) + (6.25 * height) - (5 * age) + 5
    else:
        bmr = (10 * weight_kg) + (6.25 * height) - (5 * age) - 161
    
    # Activity multipliers
    activity_multipliers = {
        'sedentary': 1.2,
        'light': 1.375,
        'moderate': 1.55,
        'active': 1.725,
        'very_active': 1.9
    }
    
    tdee = bmr * activity_multipliers.get(activity_level, 1.55)
    
    # Adjust calories based on goal
    if goal == 'lose_weight':
        target_calories = tdee - 500  # 500 cal deficit
        protein_ratio = 0.35
        carb_ratio = 0.30
        fat_ratio = 0.35
    elif goal == 'gain_muscle':
        target_calories = tdee + 300  # 300 cal surplus
        protein_ratio = 0.30
        carb_ratio = 0.45
        fat_ratio = 0.25
    else:  # maintain
        target_calories = tdee
        protein_ratio = 0.30
        carb_ratio = 0.40
        fat_ratio = 0.30
    
    # Calculate macros (1g protein = 4 cal, 1g carb = 4 cal, 1g fat = 9 cal)
    protein_calories = target_calories * protein_ratio
    carb_calories = target_calories * carb_ratio
    fat_calories = target_calories * fat_ratio
    
    protein_grams = protein_calories / 4
    carb_grams = carb_calories / 4
    fat_grams = fat_calories / 9
    
    # Protein per kg body weight
    protein_per_kg = protein_grams / weight_kg
    
    return {
        'bmr': round(bmr, 0),
        'tdee': round(tdee, 0),
        'target_calories': round(target_calories, 0),
        'macros': {
            'protein': {
                'grams': round(protein_grams, 1),
                'calories': round(protein_calories, 0),
                'percentage': round(protein_ratio * 100, 1),
                'per_kg_bodyweight': round(protein_per_kg, 2)
            },
            'carbs': {
                'grams': round(carb_grams, 1),
                'calories': round(carb_calories, 0),
                'percentage': round(carb_ratio * 100, 1)
            },
            'fats': {
                'grams': round(fat_grams, 1),
                'calories': round(fat_calories, 0),
                'percentage': round(fat_ratio * 100, 1)
            }
        },
        'goal': goal,
        'activity_level': activity_level,
        'meal_breakdown': calculate_meal_breakdown(protein_grams, carb_grams, fat_grams),
        'recommendations': get_macro_recommendations(goal, protein_per_kg)
    }


def calculate_meal_breakdown(protein: float, carbs: float, fats: float, meals: int = 3) -> Dict:
    """Break down macros per meal"""
    return {
        'meals_per_day': meals,
        'per_meal': {
            'protein_grams': round(protein / meals, 1),
            'carbs_grams': round(carbs / meals, 1),
            'fats_grams': round(fats / meals, 1),
            'calories': round((protein * 4 + carbs * 4 + fats * 9) / meals, 0)
        }
    }


def get_macro_recommendations(goal: str, protein_per_kg: float) -> list:
    """Get personalized recommendations"""
    recommendations = []
    
    if goal == 'lose_weight':
        recommendations.extend([
            'Maintain high protein to preserve muscle mass',
            'Focus on complex carbs and fiber',
            'Include healthy fats for satiety',
            'Stay in caloric deficit consistently'
        ])
    elif goal == 'gain_muscle':
        recommendations.extend([
            'Consume protein within 2 hours post-workout',
            'Eat carbs around training for energy',
            'Don\'t fear healthy fats for hormone production',
            'Stay in slight caloric surplus'
        ])
    else:
        recommendations.extend([
            'Balance all three macronutrients',
            'Adjust based on activity level',
            'Focus on whole food sources',
            'Stay consistent with meal timing'
        ])
    
    if protein_per_kg < 1.6:
        recommendations.append('Consider increasing protein intake for optimal results')
    
    return recommendations
