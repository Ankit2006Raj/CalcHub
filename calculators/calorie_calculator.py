"""
Professional Calorie Calculator Module
Provides comprehensive daily caloric needs with detailed nutritional planning
"""

from typing import Dict, Union, List, Optional


class CalorieCalculationError(Exception):
    """Custom exception for calorie calculation errors"""
    pass


def calculate_calories(
    gender: str,
    age: int,
    weight: float,
    height: float,
    activity: str,
    goal: str = "maintain",
    body_fat_percentage: Optional[float] = None,
    unit_system: str = "metric",
    detailed: bool = False
) -> Dict[str, Union[float, str, Dict, List]]:
    """
    Calculate comprehensive daily caloric needs with meal planning
    
    Args:
        gender: 'male' or 'female'
        age: Age in years
        weight: Weight in kg (metric) or lbs (imperial)
        height: Height in cm (metric) or inches (imperial)
        activity: Activity level - 'sedentary', 'light', 'moderate', 'active', 'very_active'
        goal: Fitness goal - 'lose', 'maintain', 'gain'
        body_fat_percentage: Optional body fat percentage for more accurate calculations
        unit_system: 'metric' or 'imperial'
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed caloric needs and meal planning
    
    Raises:
        CalorieCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if gender.lower() not in ['male', 'female']:
        raise CalorieCalculationError("Gender must be 'male' or 'female'.")
    if age <= 0 or age > 120:
        raise CalorieCalculationError("Age must be between 1 and 120 years.")
    if weight <= 0:
        raise CalorieCalculationError("Weight must be greater than zero.")
    if height <= 0:
        raise CalorieCalculationError("Height must be greater than zero.")
    if unit_system.lower() not in ['metric', 'imperial']:
        raise CalorieCalculationError("Unit system must be 'metric' or 'imperial'.")
    
    # Convert imperial to metric if needed
    if unit_system.lower() == 'imperial':
        height = height * 2.54  # inches to cm
        weight = weight * 0.453592  # lbs to kg
    
    # Additional validation
    if height < 50 or height > 300:
        raise CalorieCalculationError("Height must be between 50-300 cm.")
    if weight < 20 or weight > 500:
        raise CalorieCalculationError("Weight must be between 20-500 kg.")
    
    # Calculate BMR using multiple formulas
    bmr_harris = calculate_bmr_harris_benedict(gender.lower(), age, height, weight)
    bmr_mifflin = calculate_bmr_mifflin(gender.lower(), age, height, weight)
    
    # Use Mifflin-St Jeor as primary (more accurate for modern populations)
    bmr = bmr_mifflin
    
    # Activity multipliers with detailed descriptions
    activity_levels = {
        'sedentary': {
            'multiplier': 1.2,
            'description': 'Little or no exercise, desk job',
            'examples': 'Office work, studying, minimal movement'
        },
        'light': {
            'multiplier': 1.375,
            'description': 'Light exercise 1-3 days/week',
            'examples': 'Light walking, casual sports 1-3 times/week'
        },
        'moderate': {
            'multiplier': 1.55,
            'description': 'Moderate exercise 3-5 days/week',
            'examples': 'Regular gym sessions, active job, sports 3-5 times/week'
        },
        'active': {
            'multiplier': 1.725,
            'description': 'Hard exercise 6-7 days/week',
            'examples': 'Daily intense workouts, physically demanding job'
        },
        'very_active': {
            'multiplier': 1.9,
            'description': 'Very hard exercise, physical job, training twice/day',
            'examples': 'Athlete training, construction work, multiple daily workouts'
        }
    }
    
    # Get activity multiplier
    activity_lower = activity.lower()
    if activity_lower not in activity_levels:
        raise CalorieCalculationError(f"Invalid activity level. Choose from: {', '.join(activity_levels.keys())}")
    
    multiplier = activity_levels[activity_lower]['multiplier']
    maintenance_calories = bmr * multiplier
    
    # Calculate goal-based calories
    goal_calories = calculate_goal_calories(maintenance_calories, goal.lower())
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'calories': round(goal_calories['calories'], 2),
            'bmr': round(bmr, 2),
            'maintain': round(maintenance_calories, 2),
            'lose': round(maintenance_calories - 500, 2),
            'gain': round(maintenance_calories + 500, 2),
            'activity': activity
        }
    
    # Calculate macronutrient breakdown
    macros = calculate_macronutrients(goal_calories['calories'], goal.lower(), gender.lower())
    
    # Calculate meal distribution
    meal_plan = distribute_calories_to_meals(goal_calories['calories'])
    
    # Calculate hydration needs
    hydration = calculate_hydration_needs(weight, activity_lower)
    
    # Calculate weekly projections
    weekly_projection = calculate_weekly_projection(maintenance_calories, goal_calories['calories'])
    
    # Generate personalized recommendations
    recommendations = generate_calorie_recommendations(
        bmr, maintenance_calories, goal.lower(), age, gender.lower(), activity_lower
    )
    
    # Calculate all activity level options
    all_activity_calories = {}
    for level, data in activity_levels.items():
        all_activity_calories[level] = {
            'calories': round(bmr * data['multiplier'], 2),
            'description': data['description'],
            'examples': data['examples']
        }
    
    return {
        'bmr': {
            'calories': round(bmr, 2),
            'harris_benedict': round(bmr_harris, 2),
            'mifflin_st_jeor': round(bmr_mifflin, 2),
            'description': 'Basal Metabolic Rate - calories burned at rest'
        },
        'tdee': {
            'calories': round(maintenance_calories, 2),
            'activity_level': activity_lower,
            'activity_multiplier': multiplier,
            'description': 'Total Daily Energy Expenditure'
        },
        'goal_calories': goal_calories,
        'all_activity_levels': all_activity_calories,
        'macronutrients': macros,
        'meal_distribution': meal_plan,
        'hydration': hydration,
        'weekly_projection': weekly_projection,
        'input_parameters': {
            'gender': gender.lower(),
            'age': age,
            'weight_kg': round(weight, 2),
            'weight_lbs': round(weight * 2.20462, 2),
            'height_cm': round(height, 2),
            'height_inches': round(height / 2.54, 2),
            'activity_level': activity_lower,
            'goal': goal.lower()
        },
        'recommendations': recommendations,
        'notes': [
            'Caloric needs are estimates and may vary by individual',
            'Adjust based on actual results over 2-4 weeks',
            'Consult healthcare provider before major dietary changes',
            'Quality of calories matters as much as quantity',
            'Stay consistent with tracking for best results'
        ]
    }


def calculate_bmr_harris_benedict(gender: str, age: int, height: float, weight: float) -> float:
    """Calculate BMR using Harris-Benedict equation"""
    if gender == 'male':
        return 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    else:
        return 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)


def calculate_bmr_mifflin(gender: str, age: int, height: float, weight: float) -> float:
    """Calculate BMR using Mifflin-St Jeor equation"""
    bmr = (10 * weight) + (6.25 * height) - (5 * age)
    return bmr + 5 if gender == 'male' else bmr - 161


def calculate_goal_calories(maintenance: float, goal: str) -> Dict:
    """Calculate calories based on fitness goal"""
    goals = {
        'lose': {
            'extreme': {'calories': maintenance - 1000, 'rate': '1 kg/week', 'description': 'Aggressive weight loss'},
            'moderate': {'calories': maintenance - 500, 'rate': '0.5 kg/week', 'description': 'Sustainable weight loss'},
            'mild': {'calories': maintenance - 250, 'rate': '0.25 kg/week', 'description': 'Slow weight loss'}
        },
        'maintain': {
            'calories': maintenance,
            'rate': '0 kg/week',
            'description': 'Maintain current weight'
        },
        'gain': {
            'mild': {'calories': maintenance + 250, 'rate': '0.25 kg/week', 'description': 'Lean muscle gain'},
            'moderate': {'calories': maintenance + 500, 'rate': '0.5 kg/week', 'description': 'Muscle building'},
            'aggressive': {'calories': maintenance + 750, 'rate': '0.75 kg/week', 'description': 'Rapid muscle gain'}
        }
    }
    
    if goal == 'lose':
        return {
            'calories': round(goals['lose']['moderate']['calories'], 2),
            'rate': goals['lose']['moderate']['rate'],
            'description': goals['lose']['moderate']['description'],
            'options': {k: {**v, 'calories': round(v['calories'], 2)} for k, v in goals['lose'].items()}
        }
    elif goal == 'gain':
        return {
            'calories': round(goals['gain']['moderate']['calories'], 2),
            'rate': goals['gain']['moderate']['rate'],
            'description': goals['gain']['moderate']['description'],
            'options': {k: {**v, 'calories': round(v['calories'], 2)} for k, v in goals['gain'].items()}
        }
    else:
        return {
            'calories': round(goals['maintain']['calories'], 2),
            'rate': goals['maintain']['rate'],
            'description': goals['maintain']['description']
        }


def calculate_macronutrients(calories: float, goal: str, gender: str) -> Dict:
    """Calculate macronutrient distribution based on goal"""
    if goal == 'lose':
        # High protein for muscle preservation
        protein_pct, carb_pct, fat_pct = 0.40, 0.30, 0.30
    elif goal == 'gain':
        # Balanced with adequate carbs for energy
        protein_pct, carb_pct, fat_pct = 0.30, 0.45, 0.25
    else:
        # Balanced maintenance
        protein_pct, carb_pct, fat_pct = 0.30, 0.40, 0.30
    
    return {
        'protein': {
            'grams': round(calories * protein_pct / 4, 1),
            'calories': round(calories * protein_pct, 1),
            'percentage': int(protein_pct * 100),
            'calories_per_gram': 4
        },
        'carbohydrates': {
            'grams': round(calories * carb_pct / 4, 1),
            'calories': round(calories * carb_pct, 1),
            'percentage': int(carb_pct * 100),
            'calories_per_gram': 4
        },
        'fats': {
            'grams': round(calories * fat_pct / 9, 1),
            'calories': round(calories * fat_pct, 1),
            'percentage': int(fat_pct * 100),
            'calories_per_gram': 9
        },
        'fiber_grams': round(calories / 1000 * 14, 1),
        'distribution_type': f"Optimized for {goal}"
    }


def distribute_calories_to_meals(total_calories: float) -> Dict:
    """Distribute calories across meals"""
    return {
        '3_meals': {
            'breakfast': round(total_calories * 0.30, 0),
            'lunch': round(total_calories * 0.40, 0),
            'dinner': round(total_calories * 0.30, 0),
            'description': 'Traditional 3 meals per day'
        },
        '4_meals': {
            'breakfast': round(total_calories * 0.25, 0),
            'lunch': round(total_calories * 0.30, 0),
            'snack': round(total_calories * 0.15, 0),
            'dinner': round(total_calories * 0.30, 0),
            'description': '3 meals + 1 snack'
        },
        '5_meals': {
            'breakfast': round(total_calories * 0.20, 0),
            'morning_snack': round(total_calories * 0.15, 0),
            'lunch': round(total_calories * 0.25, 0),
            'afternoon_snack': round(total_calories * 0.15, 0),
            'dinner': round(total_calories * 0.25, 0),
            'description': '3 meals + 2 snacks (recommended for muscle gain)'
        },
        '6_meals': {
            'meal_1': round(total_calories / 6, 0),
            'meal_2': round(total_calories / 6, 0),
            'meal_3': round(total_calories / 6, 0),
            'meal_4': round(total_calories / 6, 0),
            'meal_5': round(total_calories / 6, 0),
            'meal_6': round(total_calories / 6, 0),
            'description': 'Frequent small meals (for athletes/bodybuilders)'
        }
    }


def calculate_hydration_needs(weight_kg: float, activity_level: str) -> Dict:
    """Calculate daily water intake needs"""
    base_water = weight_kg * 0.033  # liters
    
    activity_bonus = {
        'sedentary': 0,
        'light': 0.5,
        'moderate': 1.0,
        'active': 1.5,
        'very_active': 2.0
    }
    
    total_water = base_water + activity_bonus.get(activity_level, 0)
    
    return {
        'liters_per_day': round(total_water, 1),
        'ml_per_day': round(total_water * 1000, 0),
        'cups_per_day': round(total_water * 4.22, 1),
        'ounces_per_day': round(total_water * 33.814, 1),
        'recommendation': f"Drink {round(total_water, 1)}L throughout the day",
        'note': 'Increase during hot weather or intense exercise'
    }


def calculate_weekly_projection(maintenance: float, goal_calories: float) -> Dict:
    """Calculate weekly caloric surplus/deficit and weight change"""
    daily_diff = goal_calories - maintenance
    weekly_diff = daily_diff * 7
    
    # 7700 calories ≈ 1 kg of body weight
    weekly_weight_change = weekly_diff / 7700
    monthly_weight_change = weekly_weight_change * 4.33
    
    return {
        'daily_difference': round(daily_diff, 0),
        'weekly_difference': round(weekly_diff, 0),
        'weekly_weight_change_kg': round(weekly_weight_change, 2),
        'weekly_weight_change_lbs': round(weekly_weight_change * 2.20462, 2),
        'monthly_weight_change_kg': round(monthly_weight_change, 2),
        'monthly_weight_change_lbs': round(monthly_weight_change * 2.20462, 2),
        'projection_type': 'gain' if daily_diff > 0 else ('loss' if daily_diff < 0 else 'maintenance')
    }


def generate_calorie_recommendations(
    bmr: float,
    tdee: float,
    goal: str,
    age: int,
    gender: str,
    activity: str
) -> List[str]:
    """Generate personalized calorie and nutrition recommendations"""
    recommendations = []
    
    if goal == 'lose':
        recommendations.extend([
            'Prioritize protein to preserve muscle mass during weight loss',
            'Eat plenty of vegetables for volume and nutrients',
            'Track your food intake consistently',
            'Aim for 0.5-1 kg weight loss per week for sustainability',
            'Don\'t go below 1200 calories (women) or 1500 calories (men)',
            'Include strength training to maintain muscle'
        ])
    elif goal == 'gain':
        recommendations.extend([
            'Eat in a slight surplus (250-500 calories above maintenance)',
            'Consume protein with every meal (1.6-2.2g per kg body weight)',
            'Focus on nutrient-dense, calorie-rich foods',
            'Combine with progressive resistance training',
            'Be patient - aim for 0.25-0.5 kg gain per week',
            'Track progress with measurements, not just scale weight'
        ])
    else:
        recommendations.extend([
            'Maintain consistent eating patterns',
            'Focus on whole, unprocessed foods',
            'Balance macronutrients for sustained energy',
            'Listen to hunger and fullness cues',
            'Stay active and exercise regularly'
        ])
    
    # Activity-specific recommendations
    if activity in ['sedentary', 'light']:
        recommendations.append('Consider increasing daily activity for better health')
    
    # Age-specific recommendations
    if age > 50:
        recommendations.append('Ensure adequate protein and calcium for bone health')
    
    return recommendations
