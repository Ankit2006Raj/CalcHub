"""
Professional Attendance Calculator Module
Provides comprehensive attendance tracking and analysis with predictions
"""

from typing import Dict, Union, List, Optional
from datetime import datetime, timedelta


class AttendanceCalculationError(Exception):
    """Custom exception for attendance calculation errors"""
    pass


def calculate_attendance(
    attended: int,
    total: int,
    target: float = 75,
    total_classes_in_semester: Optional[int] = None,
    detailed: bool = False
) -> Dict[str, Union[float, int, str, List, Dict]]:
    """
    Calculate comprehensive attendance metrics with predictions and analysis
    
    Args:
        attended: Number of classes attended
        total: Total number of classes held so far
        target: Target attendance percentage (default: 75)
        total_classes_in_semester: Optional total classes expected in semester
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed attendance analysis and predictions
    
    Raises:
        AttendanceCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if attended < 0:
        raise AttendanceCalculationError("Attended classes cannot be negative.")
    if total <= 0:
        raise AttendanceCalculationError("Total classes must be greater than zero.")
    if attended > total:
        raise AttendanceCalculationError("Attended classes cannot exceed total classes.")
    if target < 0 or target > 100:
        raise AttendanceCalculationError("Target percentage must be between 0 and 100.")
    if total_classes_in_semester and total_classes_in_semester < total:
        raise AttendanceCalculationError("Total semester classes cannot be less than current total.")
    
    # Calculate current percentage
    current_percentage = (attended / total) * 100
    
    # Calculate classes needed to reach target
    if current_percentage < target:
        classes_needed = ((target * total) - (100 * attended)) / (100 - target)
        classes_needed = max(0, int(classes_needed) + 1)
    else:
        classes_needed = 0
    
    # Calculate how many classes can be missed
    if current_percentage > target:
        can_miss = int((100 * attended - target * total) / target)
    else:
        can_miss = 0
    
    # Determine status
    status = get_attendance_status(current_percentage, target)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'percentage': round(current_percentage, 2),
            'attended': attended,
            'total': total,
            'target': target,
            'classes_needed': classes_needed,
            'can_miss': max(0, can_miss),
            'status': status['category']
        }
    
    # Calculate detailed metrics
    missed = total - attended
    attendance_rate = attended / total if total > 0 else 0
    
    # Predictions for different scenarios
    predictions = calculate_predictions(attended, total, target, total_classes_in_semester)
    
    # Calculate streak information
    streak_info = {
        'note': 'Streak tracking requires historical data',
        'current_attended': attended,
        'current_missed': missed
    }
    
    # Calculate what-if scenarios
    scenarios = calculate_scenarios(attended, total, target)
    
    # Calculate semester projection
    semester_projection = None
    if total_classes_in_semester:
        semester_projection = project_semester_attendance(
            attended, total, target, total_classes_in_semester
        )
    
    # Generate recommendations
    recommendations = generate_attendance_recommendations(
        current_percentage, target, classes_needed, can_miss
    )
    
    return {
        'current_status': {
            'percentage': round(current_percentage, 2),
            'attended': attended,
            'missed': missed,
            'total': total,
            'attendance_rate': round(attendance_rate, 4),
            'status': status['category'],
            'status_description': status['description'],
            'color': status['color']
        },
        'target_analysis': {
            'target_percentage': target,
            'difference_from_target': round(current_percentage - target, 2),
            'classes_needed_to_reach_target': classes_needed,
            'classes_can_miss_safely': max(0, can_miss),
            'is_on_track': current_percentage >= target
        },
        'predictions': predictions,
        'scenarios': scenarios,
        'semester_projection': semester_projection,
        'statistics': {
            'attendance_ratio': f"{attended}:{total}",
            'absence_ratio': f"{missed}:{total}",
            'attendance_fraction': f"{attended}/{total}",
            'classes_per_percentage': round(total / 100, 2) if total > 0 else 0
        },
        'recommendations': recommendations,
        'notes': [
            'Maintain consistent attendance for better academic performance',
            'Plan ahead for unavoidable absences',
            'Some institutions have strict attendance policies',
            'Medical emergencies may have separate consideration'
        ]
    }


def get_attendance_status(percentage: float, target: float) -> Dict:
    """Determine attendance status with color coding"""
    if percentage >= target + 10:
        return {
            'category': 'Excellent',
            'description': 'Well above target, great attendance!',
            'color': '#2ecc71'
        }
    elif percentage >= target:
        return {
            'category': 'Good',
            'description': 'Meeting attendance requirements',
            'color': '#27ae60'
        }
    elif percentage >= target - 5:
        return {
            'category': 'Warning',
            'description': 'Close to minimum requirement',
            'color': '#f39c12'
        }
    elif percentage >= target - 10:
        return {
            'category': 'Critical',
            'description': 'Below requirement, immediate action needed',
            'color': '#e67e22'
        }
    else:
        return {
            'category': 'Danger',
            'description': 'Significantly below requirement',
            'color': '#e74c3c'
        }


def calculate_predictions(
    attended: int,
    total: int,
    target: float,
    total_semester: Optional[int]
) -> Dict:
    """Calculate attendance predictions for various scenarios"""
    predictions = {}
    
    # Predict if attending all remaining classes
    if total_semester and total_semester > total:
        remaining = total_semester - total
        future_attended = attended + remaining
        future_total = total_semester
        perfect_attendance_pct = (future_attended / future_total) * 100
        
        predictions['perfect_attendance'] = {
            'scenario': 'Attend all remaining classes',
            'final_percentage': round(perfect_attendance_pct, 2),
            'classes_to_attend': remaining,
            'final_attended': future_attended,
            'final_total': future_total
        }
        
        # Predict if missing all remaining classes
        worst_case_pct = (attended / future_total) * 100
        predictions['worst_case'] = {
            'scenario': 'Miss all remaining classes',
            'final_percentage': round(worst_case_pct, 2),
            'classes_missed': remaining,
            'final_attended': attended,
            'final_total': future_total
        }
        
        # Predict maintaining current rate
        current_rate = attended / total
        future_attended_current_rate = int(total_semester * current_rate)
        current_rate_pct = (future_attended_current_rate / total_semester) * 100
        
        predictions['maintain_current_rate'] = {
            'scenario': 'Maintain current attendance rate',
            'final_percentage': round(current_rate_pct, 2),
            'expected_attended': future_attended_current_rate,
            'expected_missed': total_semester - future_attended_current_rate,
            'final_total': total_semester
        }
    
    return predictions


def calculate_scenarios(attended: int, total: int, target: float) -> List[Dict]:
    """Calculate what-if scenarios for next few classes"""
    scenarios = []
    
    for next_classes in [5, 10, 15, 20]:
        # Scenario: Attend all next classes
        new_attended = attended + next_classes
        new_total = total + next_classes
        new_percentage = (new_attended / new_total) * 100
        
        scenarios.append({
            'next_classes': next_classes,
            'attend_all': {
                'percentage': round(new_percentage, 2),
                'attended': new_attended,
                'total': new_total,
                'meets_target': new_percentage >= target
            },
            'attend_none': {
                'percentage': round((attended / new_total) * 100, 2),
                'attended': attended,
                'total': new_total,
                'meets_target': (attended / new_total) * 100 >= target
            }
        })
    
    return scenarios


def project_semester_attendance(
    attended: int,
    total: int,
    target: float,
    total_semester: int
) -> Dict:
    """Project semester-end attendance"""
    remaining = total_semester - total
    current_pct = (attended / total) * 100
    
    # Calculate minimum classes to attend to reach target
    min_to_attend = 0
    for i in range(remaining + 1):
        future_attended = attended + i
        future_pct = (future_attended / total_semester) * 100
        if future_pct >= target:
            min_to_attend = i
            break
    
    # Calculate maximum classes can miss
    max_can_miss = remaining - min_to_attend
    
    return {
        'total_semester_classes': total_semester,
        'classes_completed': total,
        'classes_remaining': remaining,
        'current_percentage': round(current_pct, 2),
        'to_reach_target': {
            'minimum_classes_to_attend': min_to_attend,
            'maximum_classes_can_miss': max_can_miss,
            'attendance_required_percentage': round((min_to_attend / remaining * 100), 2) if remaining > 0 else 0
        },
        'projected_outcomes': {
            'if_attend_all': round(((attended + remaining) / total_semester) * 100, 2),
            'if_attend_none': round((attended / total_semester) * 100, 2),
            'if_attend_half': round(((attended + remaining // 2) / total_semester) * 100, 2)
        }
    }


def generate_attendance_recommendations(
    current_pct: float,
    target: float,
    classes_needed: int,
    can_miss: int
) -> List[str]:
    """Generate personalized attendance recommendations"""
    recommendations = []
    
    if current_pct >= target + 10:
        recommendations.extend([
            'Excellent attendance! Keep up the good work',
            f'You can safely miss up to {can_miss} classes and still meet requirements',
            'Consider helping classmates who struggle with attendance',
            'Use your buffer wisely for emergencies'
        ])
    elif current_pct >= target:
        recommendations.extend([
            'Good attendance, you\'re meeting requirements',
            f'You can miss {can_miss} more classes safely' if can_miss > 0 else 'Avoid missing any more classes',
            'Try to build a buffer for unexpected situations',
            'Maintain consistency in attendance'
        ])
    elif classes_needed > 0:
        recommendations.extend([
            f'⚠️ You need to attend the next {classes_needed} classes consecutively',
            'Avoid any further absences',
            'Plan ahead for important dates',
            'Consider speaking with your instructor about your situation',
            'Set reminders for all upcoming classes'
        ])
    
    # General recommendations
    recommendations.extend([
        'Regular attendance improves learning outcomes',
        'Track your attendance weekly',
        'Inform instructors in advance for planned absences'
    ])
    
    return recommendations
