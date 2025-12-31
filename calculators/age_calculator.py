"""
Professional Age Calculator Module
Provides comprehensive age calculations with multiple formats and milestones
"""

from datetime import datetime, timedelta
from typing import Dict, Optional, Union
import calendar


class AgeCalculationError(Exception):
    """Custom exception for age calculation errors"""
    pass


def calculate_age(dob: str, reference_date: Optional[str] = None, detailed: bool = False) -> Dict[str, Union[int, float, str, Dict]]:
    """
    Calculate comprehensive age metrics from date of birth
    
    Args:
        dob: Date of birth in 'YYYY-MM-DD' format
        reference_date: Optional reference date (defaults to today)
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed age information
    
    Raises:
        AgeCalculationError: If date format is invalid or date is in future
    """
    try:
        birth_date = datetime.strptime(dob, '%Y-%m-%d')
    except ValueError:
        raise AgeCalculationError("Invalid date format. Please use YYYY-MM-DD format.")
    
    # Use reference date or today
    if reference_date:
        try:
            today = datetime.strptime(reference_date, '%Y-%m-%d')
        except ValueError:
            raise AgeCalculationError("Invalid reference date format. Please use YYYY-MM-DD format.")
    else:
        today = datetime.today()
    
    # Validate date is not in future
    if birth_date > today:
        raise AgeCalculationError("Date of birth cannot be in the future.")
    
    # Calculate precise age components
    years = today.year - birth_date.year
    months = today.month - birth_date.month
    days = today.day - birth_date.day
    
    # Adjust for negative days
    if days < 0:
        months -= 1
        # Get actual days in previous month
        prev_month = today.month - 1 if today.month > 1 else 12
        prev_year = today.year if today.month > 1 else today.year - 1
        days_in_prev_month = calendar.monthrange(prev_year, prev_month)[1]
        days += days_in_prev_month
    
    # Adjust for negative months
    if months < 0:
        years -= 1
        months += 12
    
    # Calculate total time units
    time_diff = today - birth_date
    total_days = time_diff.days
    total_hours = total_days * 24
    total_minutes = total_hours * 60
    total_seconds = total_minutes * 60
    
    # Calculate weeks
    total_weeks = total_days // 7
    remaining_days = total_days % 7
    
    # Calculate total months (approximate)
    total_months = years * 12 + months
    
    # Calculate next birthday
    next_birthday = datetime(today.year, birth_date.month, birth_date.day)
    if next_birthday < today:
        next_birthday = datetime(today.year + 1, birth_date.month, birth_date.day)
    days_to_birthday = (next_birthday - today).days
    
    # Determine zodiac sign
    zodiac_sign = get_zodiac_sign(birth_date.month, birth_date.day)
    
    # Determine generation
    generation = get_generation(birth_date.year)
    
    # Calculate life milestones
    milestones = calculate_milestones(birth_date, today)
    
    # Day of week born
    day_of_week = birth_date.strftime('%A')
    
    # Age category
    age_category = categorize_age(years)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'years': years,
            'months': months,
            'days': days,
            'total_days': total_days,
            'total_weeks': total_weeks,
            'total_months': total_months
        }
    
    # Detailed professional format
    return {
        'age': {
            'years': years,
            'months': months,
            'days': days
        },
        'precise_age': f"{years} years, {months} months, {days} days",
        'total_units': {
            'months': total_months,
            'weeks': total_weeks,
            'days': total_days,
            'hours': total_hours,
            'minutes': total_minutes,
            'seconds': total_seconds
        },
        'next_birthday': {
            'date': next_birthday.strftime('%Y-%m-%d'),
            'day_of_week': next_birthday.strftime('%A'),
            'days_remaining': days_to_birthday,
            'weeks_remaining': days_to_birthday // 7,
            'months_remaining': days_to_birthday // 30
        },
        'birth_details': {
            'date': birth_date.strftime('%Y-%m-%d'),
            'day_of_week': day_of_week,
            'zodiac_sign': zodiac_sign,
            'generation': generation
        },
        'milestones': milestones,
        'age_category': age_category,
        'is_leap_year_born': calendar.isleap(birth_date.year),
        'current_age_in_words': convert_age_to_words(years)
    }


def get_zodiac_sign(month: int, day: int) -> str:
    """Determine zodiac sign based on birth date"""
    zodiac_dates = [
        (1, 20, "Capricorn"), (2, 19, "Aquarius"), (3, 21, "Pisces"),
        (4, 20, "Aries"), (5, 21, "Taurus"), (6, 21, "Gemini"),
        (7, 23, "Cancer"), (8, 23, "Leo"), (9, 23, "Virgo"),
        (10, 23, "Libra"), (11, 22, "Scorpio"), (12, 22, "Sagittarius"),
        (12, 31, "Capricorn")
    ]
    
    for m, d, sign in zodiac_dates:
        if month < m or (month == m and day <= d):
            return sign
    return "Capricorn"


def get_generation(year: int) -> str:
    """Determine generation based on birth year"""
    if year >= 2013:
        return "Generation Alpha"
    elif year >= 1997:
        return "Generation Z"
    elif year >= 1981:
        return "Millennial"
    elif year >= 1965:
        return "Generation X"
    elif year >= 1946:
        return "Baby Boomer"
    elif year >= 1928:
        return "Silent Generation"
    else:
        return "Greatest Generation"


def categorize_age(years: int) -> str:
    """Categorize age into life stages"""
    if years < 1:
        return "Infant"
    elif years < 3:
        return "Toddler"
    elif years < 13:
        return "Child"
    elif years < 20:
        return "Teenager"
    elif years < 40:
        return "Young Adult"
    elif years < 60:
        return "Middle-Aged Adult"
    elif years < 80:
        return "Senior"
    else:
        return "Elderly"


def calculate_milestones(birth_date: datetime, current_date: datetime) -> Dict[str, Dict]:
    """Calculate important life milestones"""
    milestones = {}
    
    milestone_ages = {
        'Sweet 16': 16,
        'Legal Adult (18)': 18,
        'Legal Drinking (21)': 21,
        'Quarter Century': 25,
        'Dirty Thirty': 30,
        'Midlife (40)': 40,
        'Half Century': 50,
        'Retirement (65)': 65,
        'Platinum (70)': 70,
        'Diamond (75)': 75,
        'Octogenarian (80)': 80,
        'Nonagenarian (90)': 90,
        'Centenarian (100)': 100
    }
    
    for milestone_name, milestone_age in milestone_ages.items():
        milestone_date = datetime(birth_date.year + milestone_age, birth_date.month, birth_date.day)
        
        if milestone_date < current_date:
            status = "Completed"
            days_diff = (current_date - milestone_date).days
            time_info = f"{days_diff} days ago"
        else:
            status = "Upcoming"
            days_diff = (milestone_date - current_date).days
            time_info = f"in {days_diff} days"
        
        milestones[milestone_name] = {
            'date': milestone_date.strftime('%Y-%m-%d'),
            'status': status,
            'time_info': time_info,
            'days_difference': days_diff
        }
    
    return milestones


def convert_age_to_words(years: int) -> str:
    """Convert age number to words"""
    ones = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine"]
    teens = ["Ten", "Eleven", "Twelve", "Thirteen", "Fourteen", "Fifteen", 
             "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
    tens = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]
    
    if years == 0:
        return "Less than one year"
    elif years < 10:
        return ones[years]
    elif years < 20:
        return teens[years - 10]
    elif years < 100:
        return tens[years // 10] + (" " + ones[years % 10] if years % 10 != 0 else "")
    elif years < 120:
        return "One Hundred" + (" and " + convert_age_to_words(years - 100) if years > 100 else "")
    else:
        return str(years)
