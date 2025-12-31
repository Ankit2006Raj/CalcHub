"""
Professional Pregnancy Calculator Module
Provides comprehensive pregnancy tracking with trimester details and milestones
"""

from datetime import datetime, timedelta
from typing import Dict, Union, List, Optional


class PregnancyCalculationError(Exception):
    """Custom exception for pregnancy calculation errors"""
    pass


def calculate_due_date(
    last_period: str,
    cycle_length: int = 28,
    reference_date: Optional[str] = None,
    detailed: bool = False
) -> Dict[str, Union[str, int, float, List, Dict]]:
    """
    Calculate comprehensive pregnancy information with trimester details
    
    Args:
        last_period: Last menstrual period date in 'YYYY-MM-DD' format
        cycle_length: Average menstrual cycle length in days (default: 28)
        reference_date: Optional reference date (defaults to today)
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed pregnancy information and milestones
    
    Raises:
        PregnancyCalculationError: If input parameters are invalid
    """
    # Validate and parse dates
    try:
        lmp = datetime.strptime(last_period, '%Y-%m-%d')
    except ValueError:
        raise PregnancyCalculationError("Invalid date format. Please use YYYY-MM-DD format.")
    
    # Use reference date or today
    if reference_date:
        try:
            today = datetime.strptime(reference_date, '%Y-%m-%d')
        except ValueError:
            raise PregnancyCalculationError("Invalid reference date format. Please use YYYY-MM-DD format.")
    else:
        today = datetime.today()
    
    # Validate cycle length
    if cycle_length < 21 or cycle_length > 35:
        raise PregnancyCalculationError("Cycle length must be between 21 and 35 days.")
    
    # Validate LMP is not in future
    if lmp > today:
        raise PregnancyCalculationError("Last menstrual period cannot be in the future.")
    
    # Calculate key dates
    # Adjust conception date based on cycle length
    ovulation_day = cycle_length - 14
    conception_date = lmp + timedelta(days=ovulation_day)
    
    # Calculate due date (Naegele's rule adjusted for cycle length)
    cycle_adjustment = cycle_length - 28
    due_date = lmp + timedelta(days=280 + cycle_adjustment)
    
    # Calculate current pregnancy status
    days_pregnant = (today - lmp).days
    weeks_pregnant = days_pregnant // 7
    days_in_week = days_pregnant % 7
    
    # Calculate remaining time
    days_remaining = (due_date - today).days
    weeks_remaining = days_remaining // 7
    
    # Determine trimester
    if weeks_pregnant < 13:
        trimester = 1
        trimester_name = "First Trimester"
    elif weeks_pregnant < 27:
        trimester = 2
        trimester_name = "Second Trimester"
    else:
        trimester = 3
        trimester_name = "Third Trimester"
    
    # Check if pregnancy is valid (not too far along)
    if days_pregnant < 0:
        raise PregnancyCalculationError("Pregnancy calculation resulted in negative days.")
    if weeks_pregnant > 45:
        raise PregnancyCalculationError("Pregnancy duration exceeds normal range. Please verify LMP date.")
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'due_date': due_date.strftime('%Y-%m-%d'),
            'weeks_pregnant': weeks_pregnant,
            'days_pregnant': days_pregnant,
            'days_remaining': max(0, days_remaining),
            'trimester': trimester,
            'conception_date': conception_date.strftime('%Y-%m-%d')
        }
    
    # Calculate detailed information
    trimester_info = get_trimester_information(weeks_pregnant, days_in_week)
    milestones = calculate_pregnancy_milestones(lmp, conception_date, due_date, today)
    fetal_development = get_fetal_development_info(weeks_pregnant)
    important_dates = calculate_important_dates(lmp, due_date)
    health_tips = get_health_tips_by_trimester(trimester)
    
    # Calculate percentage of pregnancy completed
    total_days = 280 + cycle_adjustment
    percentage_complete = (days_pregnant / total_days) * 100 if days_pregnant <= total_days else 100
    
    return {
        'pregnancy_summary': {
            'weeks_pregnant': weeks_pregnant,
            'days_in_current_week': days_in_week,
            'gestational_age': f"{weeks_pregnant} weeks, {days_in_week} days",
            'days_pregnant': days_pregnant,
            'percentage_complete': round(percentage_complete, 1),
            'trimester': trimester,
            'trimester_name': trimester_name
        },
        'key_dates': {
            'last_menstrual_period': lmp.strftime('%Y-%m-%d'),
            'estimated_conception': conception_date.strftime('%Y-%m-%d'),
            'estimated_due_date': due_date.strftime('%Y-%m-%d'),
            'current_date': today.strftime('%Y-%m-%d')
        },
        'time_remaining': {
            'days_remaining': max(0, days_remaining),
            'weeks_remaining': max(0, weeks_remaining),
            'months_remaining': round(max(0, days_remaining) / 30.44, 1),
            'due_date_range': {
                'early': (due_date - timedelta(days=14)).strftime('%Y-%m-%d'),
                'expected': due_date.strftime('%Y-%m-%d'),
                'late': (due_date + timedelta(days=14)).strftime('%Y-%m-%d')
            }
        },
        'trimester_information': trimester_info,
        'fetal_development': fetal_development,
        'pregnancy_milestones': milestones,
        'important_dates': important_dates,
        'health_tips': health_tips,
        'notes': [
            'Due date is an estimate - only 5% of babies are born on their due date',
            'Full term is considered 37-42 weeks',
            'Regular prenatal care is essential for healthy pregnancy',
            'Consult healthcare provider for personalized medical advice',
            'This calculator uses Naegele\'s rule adjusted for cycle length'
        ]
    }


def get_trimester_information(weeks: int, days: int) -> Dict:
    """Get detailed information about current trimester"""
    if weeks < 13:
        return {
            'trimester': 1,
            'name': 'First Trimester',
            'weeks_range': '1-12 weeks',
            'weeks_completed': weeks,
            'weeks_remaining_in_trimester': 12 - weeks,
            'description': 'Early pregnancy - crucial development period',
            'key_developments': [
                'Major organs begin to form',
                'Heart starts beating',
                'Neural tube develops',
                'Limbs begin to form',
                'Baby is size of a grape to lime'
            ],
            'common_symptoms': [
                'Morning sickness',
                'Fatigue',
                'Breast tenderness',
                'Frequent urination',
                'Food aversions or cravings'
            ]
        }
    elif weeks < 27:
        return {
            'trimester': 2,
            'name': 'Second Trimester',
            'weeks_range': '13-26 weeks',
            'weeks_completed': weeks - 13,
            'weeks_remaining_in_trimester': 26 - weeks,
            'description': 'Middle pregnancy - often called the "golden period"',
            'key_developments': [
                'Baby can hear sounds',
                'Movement becomes noticeable',
                'Sex can be determined',
                'Fingerprints form',
                'Baby is size of an avocado to cauliflower'
            ],
            'common_symptoms': [
                'Reduced nausea',
                'Increased energy',
                'Baby movements (quickening)',
                'Growing belly',
                'Back pain'
            ]
        }
    else:
        return {
            'trimester': 3,
            'name': 'Third Trimester',
            'weeks_range': '27-40+ weeks',
            'weeks_completed': weeks - 27,
            'weeks_remaining_in_trimester': max(0, 40 - weeks),
            'description': 'Final pregnancy stage - preparing for birth',
            'key_developments': [
                'Rapid weight gain',
                'Lungs mature',
                'Brain develops rapidly',
                'Baby moves into birth position',
                'Baby is size of a pineapple to watermelon'
            ],
            'common_symptoms': [
                'Braxton Hicks contractions',
                'Shortness of breath',
                'Frequent urination',
                'Swelling in feet and ankles',
                'Difficulty sleeping'
            ]
        }


def get_fetal_development_info(weeks: int) -> Dict:
    """Get fetal development information for current week"""
    development_stages = {
        4: {'size': 'Poppy seed', 'length_mm': 2, 'weight_g': 0.5, 'milestone': 'Embryo implants in uterus'},
        8: {'size': 'Raspberry', 'length_mm': 16, 'weight_g': 1, 'milestone': 'All major organs forming'},
        12: {'size': 'Lime', 'length_mm': 54, 'weight_g': 14, 'milestone': 'Reflexes developing'},
        16: {'size': 'Avocado', 'length_mm': 116, 'weight_g': 100, 'milestone': 'Can hear sounds'},
        20: {'size': 'Banana', 'length_mm': 166, 'weight_g': 300, 'milestone': 'Halfway point, movements felt'},
        24: {'size': 'Corn', 'length_mm': 300, 'weight_g': 600, 'milestone': 'Lungs developing'},
        28: {'size': 'Eggplant', 'length_mm': 375, 'weight_g': 1000, 'milestone': 'Eyes can open'},
        32: {'size': 'Squash', 'length_mm': 425, 'weight_g': 1700, 'milestone': 'Rapid brain development'},
        36: {'size': 'Papaya', 'length_mm': 475, 'weight_g': 2600, 'milestone': 'Preparing for birth'},
        40: {'size': 'Watermelon', 'length_mm': 510, 'weight_g': 3400, 'milestone': 'Full term, ready for birth'}
    }
    
    # Find closest week
    closest_week = min(development_stages.keys(), key=lambda x: abs(x - weeks))
    info = development_stages[closest_week]
    
    return {
        'week': weeks,
        'approximate_size': info['size'],
        'length_mm': info['length_mm'],
        'length_cm': round(info['length_mm'] / 10, 1),
        'length_inches': round(info['length_mm'] / 25.4, 1),
        'weight_grams': info['weight_g'],
        'weight_ounces': round(info['weight_g'] / 28.35, 1),
        'weight_pounds': round(info['weight_g'] / 453.59, 2),
        'key_milestone': info['milestone']
    }


def calculate_pregnancy_milestones(lmp: datetime, conception: datetime, due_date: datetime, today: datetime) -> List[Dict]:
    """Calculate important pregnancy milestones"""
    milestones = []
    
    milestone_weeks = [
        (4, 'Positive pregnancy test possible'),
        (8, 'First prenatal visit recommended'),
        (10, 'End of embryonic period, now a fetus'),
        (12, 'End of first trimester, miscarriage risk decreases'),
        (16, 'Amniocentesis window (if needed)'),
        (18, 'Anatomy scan ultrasound'),
        (20, 'Halfway point'),
        (24, 'Viability milestone'),
        (28, 'Third trimester begins'),
        (32, 'Baby may move into head-down position'),
        (36, 'Weekly checkups begin'),
        (37, 'Early term - baby considered full term'),
        (40, 'Due date'),
        (42, 'Post-term, induction may be considered')
    ]
    
    for week, description in milestone_weeks:
        milestone_date = lmp + timedelta(weeks=week)
        days_until = (milestone_date - today).days
        
        if days_until >= 0:
            status = 'Upcoming'
        else:
            status = 'Completed'
        
        milestones.append({
            'week': week,
            'date': milestone_date.strftime('%Y-%m-%d'),
            'description': description,
            'status': status,
            'days_until': days_until if days_until >= 0 else None,
            'days_ago': abs(days_until) if days_until < 0 else None
        })
    
    return milestones


def calculate_important_dates(lmp: datetime, due_date: datetime) -> Dict:
    """Calculate other important pregnancy dates"""
    return {
        'first_trimester_end': (lmp + timedelta(weeks=12)).strftime('%Y-%m-%d'),
        'second_trimester_start': (lmp + timedelta(weeks=13)).strftime('%Y-%m-%d'),
        'second_trimester_end': (lmp + timedelta(weeks=26)).strftime('%Y-%m-%d'),
        'third_trimester_start': (lmp + timedelta(weeks=27)).strftime('%Y-%m-%d'),
        'viability_date': (lmp + timedelta(weeks=24)).strftime('%Y-%m-%d'),
        'full_term_start': (lmp + timedelta(weeks=37)).strftime('%Y-%m-%d'),
        'due_date': due_date.strftime('%Y-%m-%d'),
        'post_term_date': (lmp + timedelta(weeks=42)).strftime('%Y-%m-%d')
    }


def get_health_tips_by_trimester(trimester: int) -> List[str]:
    """Get health tips based on current trimester"""
    if trimester == 1:
        return [
            'Take prenatal vitamins with folic acid daily',
            'Avoid alcohol, smoking, and certain medications',
            'Stay hydrated and eat small, frequent meals',
            'Get plenty of rest - fatigue is normal',
            'Schedule your first prenatal appointment',
            'Avoid raw or undercooked foods',
            'Manage morning sickness with ginger or crackers'
        ]
    elif trimester == 2:
        return [
            'Continue prenatal vitamins',
            'Stay active with pregnancy-safe exercises',
            'Monitor baby movements',
            'Maintain healthy weight gain (0.5-1 lb/week)',
            'Stay hydrated - drink 8-10 glasses of water daily',
            'Sleep on your left side for better circulation',
            'Attend all prenatal appointments and screenings'
        ]
    else:
        return [
            'Prepare hospital bag by week 36',
            'Attend childbirth education classes',
            'Practice relaxation and breathing techniques',
            'Monitor for signs of labor',
            'Count baby kicks daily',
            'Avoid lying flat on your back',
            'Discuss birth plan with healthcare provider',
            'Watch for signs of preterm labor',
            'Stay close to home after week 36'
        ]
