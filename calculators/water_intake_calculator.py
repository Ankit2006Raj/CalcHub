"""
Water Intake Calculator Module
Calculate daily water intake needs based on various factors
"""

from typing import Dict, List


def calculate_water_intake(
    weight: float,
    activity_level: str,
    climate: str = 'moderate',
    gender: str = 'male',
    age: int = 30,
    weight_unit: str = 'kg',
    pregnant: bool = False,
    breastfeeding: bool = False
) -> Dict:
    """
    Calculate daily water intake recommendation
    
    Args:
        weight: Body weight
        activity_level: 'sedentary', 'light', 'moderate', 'active', 'very_active'
        climate: 'cold', 'moderate', 'hot'
        gender: 'male' or 'female'
        age: Age in years
        weight_unit: 'kg' or 'lbs'
        pregnant: Whether pregnant
        breastfeeding: Whether breastfeeding
    
    Returns:
        Dictionary with water intake recommendations
    """
    # Convert weight to kg if needed
    if weight_unit.lower() == 'lbs':
        weight_kg = weight * 0.453592
    else:
        weight_kg = weight
    
    # Base calculation: 30-35 ml per kg of body weight
    base_intake_ml = weight_kg * 33
    
    # Activity level multipliers
    activity_multipliers = {
        'sedentary': 1.0,
        'light': 1.1,
        'moderate': 1.2,
        'active': 1.3,
        'very_active': 1.5
    }
    
    activity_multiplier = activity_multipliers.get(activity_level, 1.0)
    
    # Climate adjustments
    climate_adjustments = {
        'cold': 0,
        'moderate': 200,
        'hot': 500
    }
    
    climate_adjustment = climate_adjustments.get(climate, 200)
    
    # Calculate total intake
    total_intake_ml = (base_intake_ml * activity_multiplier) + climate_adjustment
    
    # Gender adjustments (males typically need slightly more)
    if gender.lower() == 'male':
        total_intake_ml *= 1.05
    
    # Age adjustments
    if age > 65:
        total_intake_ml *= 1.1  # Elderly need more hydration
    elif age < 18:
        total_intake_ml *= 0.9  # Youth need slightly less
    
    # Pregnancy and breastfeeding adjustments
    if pregnant:
        total_intake_ml += 300
    if breastfeeding:
        total_intake_ml += 700
    
    # Convert to different units
    total_intake_liters = total_intake_ml / 1000
    total_intake_oz = total_intake_ml * 0.033814
    total_intake_cups = total_intake_oz / 8
    total_intake_glasses = total_intake_ml / 250  # 250ml per glass
    
    # Calculate hourly intake (assuming 16 waking hours)
    hourly_intake_ml = total_intake_ml / 16
    
    # Generate drinking schedule
    schedule = generate_drinking_schedule(total_intake_ml)
    
    # Get recommendations
    recommendations = get_hydration_recommendations(
        activity_level, climate, age, pregnant, breastfeeding
    )
    
    # Calculate hydration from food
    food_hydration_ml = total_intake_ml * 0.2  # ~20% from food
    water_to_drink_ml = total_intake_ml - food_hydration_ml
    
    return {
        'weight': weight,
        'weight_unit': weight_unit,
        'activity_level': activity_level.replace('_', ' ').title(),
        'climate': climate.title(),
        'total_intake_ml': round(total_intake_ml, 0),
        'total_intake_liters': round(total_intake_liters, 2),
        'total_intake_oz': round(total_intake_oz, 1),
        'total_intake_cups': round(total_intake_cups, 1),
        'total_intake_glasses': round(total_intake_glasses, 1),
        'water_to_drink_ml': round(water_to_drink_ml, 0),
        'water_to_drink_liters': round(water_to_drink_ml / 1000, 2),
        'food_hydration_ml': round(food_hydration_ml, 0),
        'hourly_intake_ml': round(hourly_intake_ml, 0),
        'hourly_intake_oz': round(hourly_intake_ml * 0.033814, 1),
        'drinking_schedule': schedule,
        'recommendations': recommendations,
        'hydration_tips': get_hydration_tips(),
        'signs_of_dehydration': get_dehydration_signs(),
        'benefits': get_hydration_benefits()
    }


def generate_drinking_schedule(total_ml: float) -> List[Dict]:
    """Generate a drinking schedule throughout the day"""
    schedule = [
        {'time': '7:00 AM', 'amount_ml': 250, 'note': 'Start your day hydrated'},
        {'time': '9:00 AM', 'amount_ml': 250, 'note': 'Mid-morning hydration'},
        {'time': '11:00 AM', 'amount_ml': 250, 'note': 'Before lunch'},
        {'time': '1:00 PM', 'amount_ml': 250, 'note': 'After lunch'},
        {'time': '3:00 PM', 'amount_ml': 250, 'note': 'Afternoon boost'},
        {'time': '5:00 PM', 'amount_ml': 250, 'note': 'Before dinner'},
        {'time': '7:00 PM', 'amount_ml': 250, 'note': 'Evening hydration'},
        {'time': '9:00 PM', 'amount_ml': 200, 'note': 'Before bed (light)'}
    ]
    
    # Adjust amounts based on total intake
    total_scheduled = sum(item['amount_ml'] for item in schedule)
    ratio = total_ml / total_scheduled
    
    for item in schedule:
        item['amount_ml'] = round(item['amount_ml'] * ratio, 0)
        item['amount_oz'] = round(item['amount_ml'] * 0.033814, 1)
    
    return schedule


def get_hydration_recommendations(
    activity_level: str,
    climate: str,
    age: int,
    pregnant: bool,
    breastfeeding: bool
) -> List[str]:
    """Get personalized hydration recommendations"""
    recommendations = []
    
    if activity_level in ['active', 'very_active']:
        recommendations.append("Drink extra water before, during, and after exercise")
        recommendations.append("Consider electrolyte drinks for intense workouts")
    
    if climate == 'hot':
        recommendations.append("Increase water intake in hot weather to prevent dehydration")
        recommendations.append("Avoid prolonged sun exposure during peak hours")
    
    if age > 65:
        recommendations.append("Elderly individuals may not feel thirsty - drink regularly")
    
    if pregnant:
        recommendations.append("Adequate hydration is crucial during pregnancy")
    
    if breastfeeding:
        recommendations.append("Breastfeeding mothers need extra fluids")
    
    recommendations.extend([
        "Drink water consistently throughout the day",
        "Monitor urine color - pale yellow indicates good hydration",
        "Eat water-rich foods like fruits and vegetables"
    ])
    
    return recommendations


def get_hydration_tips() -> List[str]:
    """Get general hydration tips"""
    return [
        "Carry a reusable water bottle with you",
        "Set reminders on your phone to drink water",
        "Drink a glass of water before each meal",
        "Flavor water with lemon, cucumber, or mint if plain water is boring",
        "Track your water intake with an app or journal",
        "Drink water when you wake up to rehydrate after sleep"
    ]


def get_dehydration_signs() -> List[str]:
    """Get signs of dehydration"""
    return [
        "Dark yellow urine",
        "Dry mouth and lips",
        "Headache",
        "Fatigue and dizziness",
        "Decreased urination",
        "Dry skin",
        "Rapid heartbeat"
    ]


def get_hydration_benefits() -> List[str]:
    """Get benefits of proper hydration"""
    return [
        "Improved physical performance",
        "Better cognitive function and concentration",
        "Healthy skin and complexion",
        "Proper digestion and metabolism",
        "Temperature regulation",
        "Joint lubrication",
        "Toxin removal and kidney function",
        "Weight management support"
    ]
