"""
Calorie Burn Calculator Module
Calculate calories burned during various activities
"""

from typing import Dict, List


# MET (Metabolic Equivalent of Task) values for different activities
ACTIVITY_METS = {
    'walking_slow': {'name': 'Walking (2 mph)', 'met': 2.5},
    'walking_moderate': {'name': 'Walking (3.5 mph)', 'met': 4.0},
    'walking_fast': {'name': 'Walking (4.5 mph)', 'met': 5.0},
    'running_5mph': {'name': 'Running (5 mph)', 'met': 8.0},
    'running_6mph': {'name': 'Running (6 mph)', 'met': 10.0},
    'running_8mph': {'name': 'Running (8 mph)', 'met': 13.5},
    'cycling_leisure': {'name': 'Cycling (leisure)', 'met': 4.0},
    'cycling_moderate': {'name': 'Cycling (12-14 mph)', 'met': 8.0},
    'cycling_vigorous': {'name': 'Cycling (16-19 mph)', 'met': 12.0},
    'swimming_leisure': {'name': 'Swimming (leisure)', 'met': 6.0},
    'swimming_moderate': {'name': 'Swimming (moderate)', 'met': 8.0},
    'swimming_vigorous': {'name': 'Swimming (vigorous)', 'met': 11.0},
    'yoga': {'name': 'Yoga', 'met': 2.5},
    'pilates': {'name': 'Pilates', 'met': 3.0},
    'weight_training': {'name': 'Weight Training', 'met': 6.0},
    'aerobics_low': {'name': 'Aerobics (low impact)', 'met': 5.0},
    'aerobics_high': {'name': 'Aerobics (high impact)', 'met': 7.0},
    'dancing': {'name': 'Dancing', 'met': 4.5},
    'basketball': {'name': 'Basketball', 'met': 6.5},
    'soccer': {'name': 'Soccer', 'met': 7.0},
    'tennis': {'name': 'Tennis', 'met': 7.3},
    'hiking': {'name': 'Hiking', 'met': 6.0},
    'jump_rope': {'name': 'Jump Rope', 'met': 12.0},
    'rowing': {'name': 'Rowing Machine', 'met': 7.0},
    'elliptical': {'name': 'Elliptical', 'met': 5.0},
    'stair_climbing': {'name': 'Stair Climbing', 'met': 8.0},
    'gardening': {'name': 'Gardening', 'met': 4.0},
    'cleaning': {'name': 'House Cleaning', 'met': 3.5},
    'golf': {'name': 'Golf (walking)', 'met': 4.8},
    'bowling': {'name': 'Bowling', 'met': 3.0}
}


def calculate_calorie_burn(
    weight: float,
    activity: str,
    duration: int,
    weight_unit: str = 'kg'
) -> Dict:
    """
    Calculate calories burned during an activity
    
    Args:
        weight: Body weight
        activity: Activity type (key from ACTIVITY_METS)
        duration: Duration in minutes
        weight_unit: 'kg' or 'lbs'
    
    Returns:
        Dictionary with calorie burn information
    """
    # Convert weight to kg if needed
    if weight_unit.lower() == 'lbs':
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight
    
    # Get MET value
    if activity not in ACTIVITY_METS:
        activity = 'walking_moderate'  # Default
    
    met_data = ACTIVITY_METS[activity]
    met_value = met_data['met']
    
    # Calculate calories burned
    # Formula: Calories = MET × weight (kg) × duration (hours)
    duration_hours = duration / 60
    calories_burned = met_value * weight_kg * duration_hours
    
    # Calculate additional metrics
    calories_per_minute = calories_burned / duration
    calories_per_hour = calories_per_minute * 60
    
    # Estimate fat burned (1 pound of fat = 3500 calories)
    fat_burned_lbs = calories_burned / 3500
    fat_burned_kg = fat_burned_lbs * 0.453592
    
    # Calculate equivalent activities
    equivalents = calculate_equivalents(calories_burned, weight_kg)
    
    return {
        'activity': met_data['name'],
        'duration_minutes': duration,
        'weight': weight,
        'weight_unit': weight_unit,
        'met_value': met_value,
        'calories_burned': round(calories_burned, 2),
        'calories_per_minute': round(calories_per_minute, 2),
        'calories_per_hour': round(calories_per_hour, 2),
        'fat_burned_lbs': round(fat_burned_lbs, 4),
        'fat_burned_kg': round(fat_burned_kg, 4),
        'intensity': get_intensity_level(met_value),
        'equivalents': equivalents,
        'recommendations': get_recommendations(met_value, duration)
    }


def calculate_multiple_activities(
    weight: float,
    activities: List[Dict],
    weight_unit: str = 'kg'
) -> Dict:
    """
    Calculate total calories burned from multiple activities
    
    Args:
        weight: Body weight
        activities: List of dicts with 'activity' and 'duration' keys
        weight_unit: 'kg' or 'lbs'
    
    Returns:
        Dictionary with total calorie burn information
    """
    total_calories = 0
    total_duration = 0
    activity_breakdown = []
    
    for activity_data in activities:
        result = calculate_calorie_burn(
            weight,
            activity_data['activity'],
            activity_data['duration'],
            weight_unit
        )
        
        total_calories += result['calories_burned']
        total_duration += result['duration_minutes']
        
        activity_breakdown.append({
            'activity': result['activity'],
            'duration': result['duration_minutes'],
            'calories': result['calories_burned']
        })
    
    return {
        'total_calories_burned': round(total_calories, 2),
        'total_duration_minutes': total_duration,
        'total_duration_hours': round(total_duration / 60, 2),
        'average_calories_per_minute': round(total_calories / total_duration, 2) if total_duration > 0 else 0,
        'activity_breakdown': activity_breakdown,
        'weight': weight,
        'weight_unit': weight_unit
    }


def get_intensity_level(met_value: float) -> str:
    """Determine intensity level based on MET value"""
    if met_value < 3:
        return 'Light'
    elif met_value < 6:
        return 'Moderate'
    elif met_value < 9:
        return 'Vigorous'
    else:
        return 'Very Vigorous'


def calculate_equivalents(calories: float, weight_kg: float) -> Dict:
    """Calculate equivalent activities for burned calories"""
    return {
        'walking_minutes': round(calories / (4.0 * weight_kg / 60), 0),
        'running_minutes': round(calories / (10.0 * weight_kg / 60), 0),
        'cycling_minutes': round(calories / (8.0 * weight_kg / 60), 0),
        'swimming_minutes': round(calories / (8.0 * weight_kg / 60), 0)
    }


def get_recommendations(met_value: float, duration: int) -> List[str]:
    """Get activity recommendations"""
    recommendations = []
    
    if met_value < 3:
        recommendations.append("Consider increasing intensity for better calorie burn")
    
    if duration < 30:
        recommendations.append("Aim for at least 30 minutes of activity for optimal benefits")
    
    if met_value >= 6:
        recommendations.append("Great job! This is a vigorous activity")
    
    recommendations.append("Stay hydrated during and after exercise")
    recommendations.append("Combine with a balanced diet for best results")
    
    return recommendations


def get_all_activities() -> Dict:
    """Return all available activities"""
    return ACTIVITY_METS
