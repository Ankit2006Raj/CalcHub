"""
Sleep Calculator Module
Calculate optimal sleep and wake times based on sleep cycles
"""

from typing import Dict, List
from datetime import datetime, timedelta


SLEEP_CYCLE_MINUTES = 90  # Average sleep cycle duration


def calculate_sleep_times(wake_time: str = None, sleep_time: str = None, cycles: int = None) -> Dict:
    """
    Calculate optimal sleep/wake times based on 90-minute sleep cycles
    
    Args:
        wake_time: Desired wake time (HH:MM format)
        sleep_time: Desired sleep time (HH:MM format)
        cycles: Number of sleep cycles (optional)
    
    Returns:
        Dictionary with sleep recommendations
    """
    if wake_time:
        return calculate_bedtimes(wake_time)
    elif sleep_time:
        return calculate_wake_times(sleep_time)
    else:
        return {'error': 'Please provide either wake_time or sleep_time'}


def calculate_bedtimes(wake_time: str) -> Dict:
    """Calculate when to go to bed based on desired wake time"""
    try:
        wake_dt = datetime.strptime(wake_time, '%H:%M')
    except ValueError:
        return {'error': 'Invalid time format. Use HH:MM (e.g., 07:00)'}
    
    bedtimes = []
    # Calculate for 4, 5, and 6 sleep cycles (6-9 hours)
    for cycles in [6, 5, 4]:
        sleep_duration = cycles * SLEEP_CYCLE_MINUTES
        # Add 15 minutes to fall asleep
        total_time = sleep_duration + 15
        
        bedtime = wake_dt - timedelta(minutes=total_time)
        
        bedtimes.append({
            'cycles': cycles,
            'bedtime': bedtime.strftime('%H:%M'),
            'sleep_duration_hours': round(sleep_duration / 60, 1),
            'total_hours': round(total_time / 60, 1),
            'quality': get_sleep_quality(cycles)
        })
    
    return {
        'wake_time': wake_time,
        'bedtime_options': bedtimes,
        'recommended': bedtimes[0],  # 6 cycles (9 hours)
        'note': 'Times include 15 minutes to fall asleep'
    }


def calculate_wake_times(sleep_time: str) -> Dict:
    """Calculate when to wake up based on bedtime"""
    try:
        sleep_dt = datetime.strptime(sleep_time, '%H:%M')
    except ValueError:
        return {'error': 'Invalid time format. Use HH:MM (e.g., 23:00)'}
    
    # Add 15 minutes to fall asleep
    actual_sleep = sleep_dt + timedelta(minutes=15)
    
    wake_times = []
    # Calculate for 4, 5, and 6 sleep cycles
    for cycles in [4, 5, 6]:
        sleep_duration = cycles * SLEEP_CYCLE_MINUTES
        wake_time = actual_sleep + timedelta(minutes=sleep_duration)
        
        wake_times.append({
            'cycles': cycles,
            'wake_time': wake_time.strftime('%H:%M'),
            'sleep_duration_hours': round(sleep_duration / 60, 1),
            'total_hours': round((sleep_duration + 15) / 60, 1),
            'quality': get_sleep_quality(cycles)
        })
    
    return {
        'sleep_time': sleep_time,
        'wake_time_options': wake_times,
        'recommended': wake_times[1],  # 5 cycles (7.5 hours)
        'note': 'Times include 15 minutes to fall asleep'
    }


def calculate_sleep_debt(hours_slept_per_night: List[float]) -> Dict:
    """Calculate sleep debt over a week"""
    optimal_sleep = 8.0
    total_debt = sum(optimal_sleep - hours for hours in hours_slept_per_night)
    avg_sleep = sum(hours_slept_per_night) / len(hours_slept_per_night)
    
    return {
        'average_sleep_hours': round(avg_sleep, 1),
        'total_sleep_debt_hours': round(total_debt, 1),
        'status': get_sleep_debt_status(total_debt),
        'recovery_nights_needed': max(0, round(total_debt / 2, 0)),
        'recommendations': get_sleep_debt_recommendations(total_debt)
    }


def get_sleep_quality(cycles: int) -> str:
    """Determine sleep quality based on cycles"""
    if cycles >= 6:
        return 'Excellent'
    elif cycles == 5:
        return 'Good'
    elif cycles == 4:
        return 'Adequate'
    else:
        return 'Insufficient'


def get_sleep_debt_status(debt: float) -> str:
    """Determine sleep debt status"""
    if debt <= 0:
        return 'No sleep debt - well rested!'
    elif debt <= 5:
        return 'Minor sleep debt'
    elif debt <= 10:
        return 'Moderate sleep debt'
    else:
        return 'Severe sleep debt'


def get_sleep_debt_recommendations(debt: float) -> List[str]:
    """Get recommendations based on sleep debt"""
    recommendations = []
    
    if debt <= 0:
        recommendations.extend([
            'Maintain your current sleep schedule',
            'Continue prioritizing sleep hygiene',
            'Keep consistent sleep/wake times'
        ])
    elif debt <= 5:
        recommendations.extend([
            'Try to get an extra hour of sleep tonight',
            'Avoid caffeine after 2 PM',
            'Take a 20-minute power nap if needed'
        ])
    elif debt <= 10:
        recommendations.extend([
            'Prioritize 8-9 hours of sleep for the next few nights',
            'Avoid screens 1 hour before bed',
            'Create a relaxing bedtime routine',
            'Consider going to bed 30 minutes earlier'
        ])
    else:
        recommendations.extend([
            'Consult a healthcare provider about sleep issues',
            'Aim for 9 hours of sleep per night this week',
            'Eliminate all caffeine and alcohol',
            'Create a dark, cool sleep environment',
            'Consider cognitive behavioral therapy for insomnia'
        ])
    
    return recommendations


def get_sleep_tips() -> List[str]:
    """General sleep hygiene tips"""
    return [
        'Keep bedroom cool (60-67°F / 15-19°C)',
        'Use blackout curtains or eye mask',
        'Avoid screens 1 hour before bed',
        'No caffeine after 2 PM',
        'Exercise regularly, but not before bed',
        'Keep consistent sleep schedule',
        'Avoid large meals before bedtime',
        'Use white noise if needed',
        'Reserve bed for sleep only',
        'Try relaxation techniques (meditation, deep breathing)'
    ]
