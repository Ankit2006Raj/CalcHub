"""
Professional Percentage Calculator Module
Provides comprehensive percentage calculations with subject-wise analysis
"""

from typing import Dict, Union, List, Optional


class PercentageCalculationError(Exception):
    """Custom exception for percentage calculation errors"""
    pass


def calculate_percentage(
    marks: List[Dict],
    passing_percentage: float = 40,
    subject_passing_percentage: float = 35,
    detailed: bool = False
) -> Dict[str, Union[float, str, List, Dict]]:
    """
    Calculate comprehensive percentage with subject-wise analysis
    
    Args:
        marks: List of subject dictionaries with 'subject', 'scored', and 'max'
        passing_percentage: Overall passing percentage (default: 40)
        subject_passing_percentage: Individual subject passing percentage (default: 35)
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed percentage analysis
    
    Raises:
        PercentageCalculationError: If input parameters are invalid
    """
    if not marks:
        raise PercentageCalculationError("Marks list cannot be empty.")
    
    # Validate and calculate
    total_scored = 0
    total_max = 0
    subject_percentages = []
    failed_subjects = []
    
    for mark in marks:
        if 'subject' not in mark or 'scored' not in mark or 'max' not in mark:
            raise PercentageCalculationError("Each mark entry must have 'subject', 'scored', and 'max' fields.")
        
        try:
            scored = float(mark['scored'])
            max_marks = float(mark['max'])
        except ValueError:
            raise PercentageCalculationError(f"Invalid numeric value in marks for {mark.get('subject', 'unknown')}.")
        
        if scored < 0:
            raise PercentageCalculationError(f"Scored marks cannot be negative for {mark['subject']}.")
        if max_marks <= 0:
            raise PercentageCalculationError(f"Maximum marks must be greater than zero for {mark['subject']}.")
        if scored > max_marks:
            raise PercentageCalculationError(f"Scored marks cannot exceed maximum for {mark['subject']}.")
        
        subject_pct = (scored / max_marks) * 100
        grade_info = get_grade_from_percentage(subject_pct)
        
        subject_data = {
            'subject': mark['subject'],
            'scored': scored,
            'max': max_marks,
            'percentage': round(subject_pct, 2),
            'grade': grade_info['grade'],
            'grade_color': grade_info['color'],
            'passed': subject_pct >= subject_passing_percentage,
            'marks_lost': max_marks - scored
        }
        
        subject_percentages.append(subject_data)
        
        if subject_pct < subject_passing_percentage:
            failed_subjects.append(mark['subject'])
        
        total_scored += scored
        total_max += max_marks
    
    # Calculate overall percentage
    overall_percentage = (total_scored / total_max) * 100 if total_max > 0 else 0
    overall_grade = get_grade_from_percentage(overall_percentage)
    overall_passed = overall_percentage >= passing_percentage and len(failed_subjects) == 0
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'percentage': round(overall_percentage, 2),
            'total_scored': total_scored,
            'total_max': total_max,
            'subjects': subject_percentages
        }
    
    # Calculate detailed analytics
    subject_analysis = analyze_subjects(subject_percentages)
    performance_analysis = analyze_overall_performance(overall_percentage, passing_percentage)
    improvement_plan = calculate_improvement_plan(subject_percentages, overall_percentage, total_max)
    
    # Generate recommendations
    recommendations = generate_percentage_recommendations(
        overall_percentage,
        subject_percentages,
        failed_subjects,
        passing_percentage
    )
    
    return {
        'overall_summary': {
            'percentage': round(overall_percentage, 2),
            'total_scored': round(total_scored, 2),
            'total_max': round(total_max, 2),
            'total_marks_lost': round(total_max - total_scored, 2),
            'grade': overall_grade['grade'],
            'grade_description': overall_grade['description'],
            'grade_color': overall_grade['color'],
            'passed': overall_passed,
            'passing_percentage': passing_percentage
        },
        'subject_details': subject_percentages,
        'subject_analysis': subject_analysis,
        'pass_status': {
            'overall_passed': overall_passed,
            'subjects_passed': len(subject_percentages) - len(failed_subjects),
            'subjects_failed': len(failed_subjects),
            'failed_subjects': failed_subjects,
            'pass_rate': round(((len(subject_percentages) - len(failed_subjects)) / len(subject_percentages)) * 100, 1)
        },
        'performance_analysis': performance_analysis,
        'improvement_plan': improvement_plan,
        'recommendations': recommendations,
        'notes': [
            'Overall percentage is calculated from total marks across all subjects',
            'Some institutions require passing in each subject individually',
            'Focus on weak subjects to improve overall performance',
            'Consistent effort across all subjects is important'
        ]
    }


def get_grade_from_percentage(percentage: float) -> Dict:
    """Convert percentage to grade"""
    if percentage >= 90:
        return {'grade': 'A+', 'description': 'Outstanding', 'color': '#2ecc71'}
    elif percentage >= 80:
        return {'grade': 'A', 'description': 'Excellent', 'color': '#27ae60'}
    elif percentage >= 70:
        return {'grade': 'B+', 'description': 'Very Good', 'color': '#3498db'}
    elif percentage >= 60:
        return {'grade': 'B', 'description': 'Good', 'color': '#2980b9'}
    elif percentage >= 50:
        return {'grade': 'C', 'description': 'Average', 'color': '#f39c12'}
    elif percentage >= 40:
        return {'grade': 'D', 'description': 'Pass', 'color': '#e67e22'}
    else:
        return {'grade': 'F', 'description': 'Fail', 'color': '#e74c3c'}


def analyze_subjects(subject_percentages: List[Dict]) -> Dict:
    """Analyze subject-wise performance"""
    if not subject_percentages:
        return {}
    
    percentages = [s['percentage'] for s in subject_percentages]
    
    # Find best and worst subjects
    best_subject = max(subject_percentages, key=lambda x: x['percentage'])
    worst_subject = min(subject_percentages, key=lambda x: x['percentage'])
    
    # Calculate statistics
    avg_percentage = sum(percentages) / len(percentages)
    
    # Categorize subjects
    excellent = [s for s in subject_percentages if s['percentage'] >= 80]
    good = [s for s in subject_percentages if 60 <= s['percentage'] < 80]
    average = [s for s in subject_percentages if 40 <= s['percentage'] < 60]
    weak = [s for s in subject_percentages if s['percentage'] < 40]
    
    return {
        'best_subject': {
            'name': best_subject['subject'],
            'percentage': best_subject['percentage'],
            'grade': best_subject['grade']
        },
        'worst_subject': {
            'name': worst_subject['subject'],
            'percentage': worst_subject['percentage'],
            'grade': worst_subject['grade']
        },
        'average_percentage': round(avg_percentage, 2),
        'highest_percentage': max(percentages),
        'lowest_percentage': min(percentages),
        'percentage_range': round(max(percentages) - min(percentages), 2),
        'subject_categories': {
            'excellent': [s['subject'] for s in excellent],
            'good': [s['subject'] for s in good],
            'average': [s['subject'] for s in average],
            'weak': [s['subject'] for s in weak]
        },
        'consistency': 'High' if (max(percentages) - min(percentages)) < 20 else 'Moderate' if (max(percentages) - min(percentages)) < 40 else 'Low'
    }


def analyze_overall_performance(percentage: float, passing_percentage: float) -> Dict:
    """Analyze overall performance level"""
    if percentage >= 90:
        level = 'Exceptional'
        description = 'Outstanding performance across all subjects'
        color = '#2ecc71'
    elif percentage >= 80:
        level = 'Excellent'
        description = 'Excellent overall performance'
        color = '#27ae60'
    elif percentage >= 70:
        level = 'Good'
        description = 'Good performance with room for improvement'
        color = '#3498db'
    elif percentage >= 60:
        level = 'Satisfactory'
        description = 'Satisfactory performance, meeting expectations'
        color = '#f39c12'
    elif percentage >= passing_percentage:
        level = 'Passing'
        description = 'Passing grade but needs improvement'
        color = '#e67e22'
    else:
        level = 'Failing'
        description = 'Below passing standard, immediate action needed'
        color = '#e74c3c'
    
    return {
        'performance_level': level,
        'description': description,
        'color': color,
        'margin_from_passing': round(percentage - passing_percentage, 2),
        'distance_to_excellence': round(90 - percentage, 2) if percentage < 90 else 0
    }


def calculate_improvement_plan(
    subject_percentages: List[Dict],
    current_percentage: float,
    total_max: float
) -> Dict:
    """Calculate improvement scenarios and targets"""
    improvement_plan = {}
    
    # Identify subjects needing most improvement
    weak_subjects = sorted(
        [s for s in subject_percentages if s['percentage'] < 60],
        key=lambda x: x['percentage']
    )
    
    # Calculate marks needed for different target percentages
    targets = [60, 70, 80, 90]
    target_scenarios = {}
    
    for target in targets:
        if target > current_percentage:
            marks_needed = (target * total_max / 100) - sum(s['scored'] for s in subject_percentages)
            target_scenarios[f'{target}%'] = {
                'target_percentage': target,
                'additional_marks_needed': round(marks_needed, 2),
                'achievable': marks_needed <= sum(s['marks_lost'] for s in subject_percentages)
            }
    
    improvement_plan['target_scenarios'] = target_scenarios
    improvement_plan['priority_subjects'] = [
        {
            'subject': s['subject'],
            'current_percentage': s['percentage'],
            'marks_lost': s['marks_lost'],
            'potential_gain': s['marks_lost']
        }
        for s in weak_subjects[:3]  # Top 3 subjects needing improvement
    ]
    
    return improvement_plan


def generate_percentage_recommendations(
    overall_percentage: float,
    subject_percentages: List[Dict],
    failed_subjects: List[str],
    passing_percentage: float
) -> List[str]:
    """Generate personalized recommendations"""
    recommendations = []
    
    # Overall performance recommendations
    if overall_percentage >= 90:
        recommendations.extend([
            'Exceptional performance! Maintain your excellence',
            'You\'re performing at the highest level across all subjects',
            'Consider mentoring peers who need help'
        ])
    elif overall_percentage >= 80:
        recommendations.extend([
            'Excellent work! You\'re doing very well',
            'Focus on maintaining consistency across all subjects',
            'Aim for 90%+ by strengthening weaker areas'
        ])
    elif overall_percentage >= 70:
        recommendations.extend([
            'Good performance overall',
            'Identify and strengthen subjects below 70%',
            'Increase practice in challenging topics'
        ])
    elif overall_percentage >= passing_percentage:
        recommendations.extend([
            'You\'ve passed, but there\'s room for improvement',
            'Focus on building stronger fundamentals',
            'Dedicate more time to regular study and practice'
        ])
    else:
        recommendations.extend([
            '⚠️ Below passing percentage - immediate action needed',
            'Meet with teachers to create an improvement plan',
            'Focus on understanding core concepts',
            'Consider additional tutoring or study support'
        ])
    
    # Subject-specific recommendations
    if failed_subjects:
        recommendations.append(f'⚠️ Priority: Focus on failed subjects - {", ".join(failed_subjects)}')
    
    # Check for inconsistency
    percentages = [s['percentage'] for s in subject_percentages]
    if max(percentages) - min(percentages) > 30:
        recommendations.append('Large variation between subjects - work on consistency')
    
    # Identify weak subjects
    weak = [s['subject'] for s in subject_percentages if s['percentage'] < 50]
    if weak:
        recommendations.append(f'Strengthen weak subjects: {", ".join(weak)}')
    
    return recommendations
