"""
Professional Grade Calculator Module
Provides comprehensive grade analysis with performance insights
"""

from typing import Dict, Union, List, Optional


class GradeCalculationError(Exception):
    """Custom exception for grade calculation errors"""
    pass


def calculate_grade(
    scored: float,
    total: float,
    grading_system: str = "standard",
    passing_percentage: float = 40,
    detailed: bool = False
) -> Dict[str, Union[float, str, Dict, List]]:
    """
    Calculate comprehensive grade with detailed performance analysis
    
    Args:
        scored: Marks scored
        total: Total marks
        grading_system: 'standard', 'strict', or 'lenient'
        passing_percentage: Minimum percentage to pass (default: 40)
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed grade analysis
    
    Raises:
        GradeCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if scored < 0:
        raise GradeCalculationError("Scored marks cannot be negative.")
    if total <= 0:
        raise GradeCalculationError("Total marks must be greater than zero.")
    if scored > total:
        raise GradeCalculationError("Scored marks cannot exceed total marks.")
    if passing_percentage < 0 or passing_percentage > 100:
        raise GradeCalculationError("Passing percentage must be between 0 and 100.")
    
    # Calculate percentage
    percentage = (scored / total) * 100
    
    # Get grade based on grading system
    grade_info = get_grade_info(percentage, grading_system)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'percentage': round(percentage, 2),
            'grade': grade_info['grade'],
            'color': grade_info['color'],
            'scored': scored,
            'total': total
        }
    
    # Calculate detailed metrics
    marks_lost = total - scored
    pass_status = percentage >= passing_percentage
    
    # Calculate performance metrics
    performance = analyze_performance(percentage, passing_percentage)
    
    # Calculate improvement scenarios
    improvement = calculate_improvement_scenarios(scored, total, percentage)
    
    # Calculate grade boundaries
    boundaries = calculate_grade_boundaries(total, grading_system)
    
    # Generate recommendations
    recommendations = generate_grade_recommendations(
        percentage, grade_info['grade'], passing_percentage, marks_lost, total
    )
    
    return {
        'score_summary': {
            'scored': scored,
            'total': total,
            'marks_lost': marks_lost,
            'percentage': round(percentage, 2),
            'fraction': f"{scored}/{total}"
        },
        'grade_info': {
            'grade': grade_info['grade'],
            'grade_description': grade_info['description'],
            'grade_points': grade_info['grade_points'],
            'color': grade_info['color'],
            'grading_system': grading_system
        },
        'pass_status': {
            'passed': pass_status,
            'passing_percentage': passing_percentage,
            'margin': round(percentage - passing_percentage, 2),
            'status': 'Passed' if pass_status else 'Failed'
        },
        'performance_analysis': performance,
        'improvement_scenarios': improvement,
        'grade_boundaries': boundaries,
        'recommendations': recommendations,
        'notes': [
            'Grade is calculated based on percentage scored',
            'Different institutions may use different grading systems',
            'Focus on understanding concepts, not just grades',
            'Consistent effort leads to better results'
        ]
    }


def get_grade_info(percentage: float, grading_system: str) -> Dict:
    """Get grade information based on percentage and grading system"""
    if grading_system == "strict":
        # Strict grading system
        if percentage >= 95:
            return {'grade': 'A+', 'description': 'Outstanding', 'grade_points': 4.0, 'color': '#2ecc71'}
        elif percentage >= 90:
            return {'grade': 'A', 'description': 'Excellent', 'grade_points': 4.0, 'color': '#27ae60'}
        elif percentage >= 85:
            return {'grade': 'A-', 'description': 'Very Good', 'grade_points': 3.7, 'color': '#229954'}
        elif percentage >= 80:
            return {'grade': 'B+', 'description': 'Good', 'grade_points': 3.3, 'color': '#3498db'}
        elif percentage >= 75:
            return {'grade': 'B', 'description': 'Above Average', 'grade_points': 3.0, 'color': '#2980b9'}
        elif percentage >= 70:
            return {'grade': 'B-', 'description': 'Average', 'grade_points': 2.7, 'color': '#5dade2'}
        elif percentage >= 65:
            return {'grade': 'C+', 'description': 'Below Average', 'grade_points': 2.3, 'color': '#f39c12'}
        elif percentage >= 60:
            return {'grade': 'C', 'description': 'Satisfactory', 'grade_points': 2.0, 'color': '#e67e22'}
        elif percentage >= 50:
            return {'grade': 'D', 'description': 'Pass', 'grade_points': 1.0, 'color': '#e74c3c'}
        else:
            return {'grade': 'F', 'description': 'Fail', 'grade_points': 0.0, 'color': '#c0392b'}
    
    elif grading_system == "lenient":
        # Lenient grading system
        if percentage >= 85:
            return {'grade': 'A+', 'description': 'Outstanding', 'grade_points': 4.0, 'color': '#2ecc71'}
        elif percentage >= 75:
            return {'grade': 'A', 'description': 'Excellent', 'grade_points': 4.0, 'color': '#27ae60'}
        elif percentage >= 65:
            return {'grade': 'B+', 'description': 'Very Good', 'grade_points': 3.3, 'color': '#3498db'}
        elif percentage >= 55:
            return {'grade': 'B', 'description': 'Good', 'grade_points': 3.0, 'color': '#2980b9'}
        elif percentage >= 45:
            return {'grade': 'C', 'description': 'Average', 'grade_points': 2.0, 'color': '#f39c12'}
        elif percentage >= 35:
            return {'grade': 'D', 'description': 'Pass', 'grade_points': 1.0, 'color': '#e67e22'}
        else:
            return {'grade': 'F', 'description': 'Fail', 'grade_points': 0.0, 'color': '#e74c3c'}
    
    else:  # Standard grading system
        if percentage >= 90:
            return {'grade': 'A+', 'description': 'Outstanding', 'grade_points': 4.0, 'color': '#2ecc71'}
        elif percentage >= 80:
            return {'grade': 'A', 'description': 'Excellent', 'grade_points': 4.0, 'color': '#27ae60'}
        elif percentage >= 70:
            return {'grade': 'B+', 'description': 'Very Good', 'grade_points': 3.3, 'color': '#3498db'}
        elif percentage >= 60:
            return {'grade': 'B', 'description': 'Good', 'grade_points': 3.0, 'color': '#2980b9'}
        elif percentage >= 50:
            return {'grade': 'C', 'description': 'Average', 'grade_points': 2.0, 'color': '#f39c12'}
        elif percentage >= 40:
            return {'grade': 'D', 'description': 'Pass', 'grade_points': 1.0, 'color': '#e67e22'}
        else:
            return {'grade': 'F', 'description': 'Fail', 'grade_points': 0.0, 'color': '#e74c3c'}


def analyze_performance(percentage: float, passing_percentage: float) -> Dict:
    """Analyze performance level"""
    if percentage >= 90:
        level = 'Exceptional'
        description = 'Outstanding performance, top of the class'
    elif percentage >= 80:
        level = 'Excellent'
        description = 'Excellent work, well above average'
    elif percentage >= 70:
        level = 'Good'
        description = 'Good performance, above average'
    elif percentage >= 60:
        level = 'Satisfactory'
        description = 'Satisfactory work, meeting expectations'
    elif percentage >= passing_percentage:
        level = 'Passing'
        description = 'Passing grade, but room for improvement'
    else:
        level = 'Failing'
        description = 'Below passing standard, needs significant improvement'
    
    # Calculate percentile (simplified estimation)
    if percentage >= 90:
        percentile = 95
    elif percentage >= 80:
        percentile = 85
    elif percentage >= 70:
        percentile = 70
    elif percentage >= 60:
        percentile = 55
    elif percentage >= 50:
        percentile = 40
    else:
        percentile = 25
    
    return {
        'performance_level': level,
        'description': description,
        'estimated_percentile': percentile,
        'above_passing': percentage >= passing_percentage,
        'margin_from_passing': round(percentage - passing_percentage, 2)
    }


def calculate_improvement_scenarios(scored: float, total: float, current_percentage: float) -> Dict:
    """Calculate what-if scenarios for improvement"""
    scenarios = {}
    
    # Calculate marks needed for different target percentages
    targets = [40, 50, 60, 70, 80, 90, 95, 100]
    
    for target in targets:
        if target > current_percentage:
            marks_needed = (target * total / 100) - scored
            additional_percentage = target - current_percentage
            
            scenarios[f'to_reach_{target}%'] = {
                'target_percentage': target,
                'additional_marks_needed': round(marks_needed, 2),
                'additional_percentage_needed': round(additional_percentage, 2),
                'achievable': marks_needed <= (total - scored)
            }
    
    return scenarios


def calculate_grade_boundaries(total: float, grading_system: str) -> List[Dict]:
    """Calculate marks required for each grade"""
    if grading_system == "strict":
        boundaries = [
            {'grade': 'A+', 'min_percentage': 95, 'max_percentage': 100},
            {'grade': 'A', 'min_percentage': 90, 'max_percentage': 94.99},
            {'grade': 'A-', 'min_percentage': 85, 'max_percentage': 89.99},
            {'grade': 'B+', 'min_percentage': 80, 'max_percentage': 84.99},
            {'grade': 'B', 'min_percentage': 75, 'max_percentage': 79.99},
            {'grade': 'B-', 'min_percentage': 70, 'max_percentage': 74.99},
            {'grade': 'C+', 'min_percentage': 65, 'max_percentage': 69.99},
            {'grade': 'C', 'min_percentage': 60, 'max_percentage': 64.99},
            {'grade': 'D', 'min_percentage': 50, 'max_percentage': 59.99},
            {'grade': 'F', 'min_percentage': 0, 'max_percentage': 49.99}
        ]
    elif grading_system == "lenient":
        boundaries = [
            {'grade': 'A+', 'min_percentage': 85, 'max_percentage': 100},
            {'grade': 'A', 'min_percentage': 75, 'max_percentage': 84.99},
            {'grade': 'B+', 'min_percentage': 65, 'max_percentage': 74.99},
            {'grade': 'B', 'min_percentage': 55, 'max_percentage': 64.99},
            {'grade': 'C', 'min_percentage': 45, 'max_percentage': 54.99},
            {'grade': 'D', 'min_percentage': 35, 'max_percentage': 44.99},
            {'grade': 'F', 'min_percentage': 0, 'max_percentage': 34.99}
        ]
    else:  # Standard
        boundaries = [
            {'grade': 'A+', 'min_percentage': 90, 'max_percentage': 100},
            {'grade': 'A', 'min_percentage': 80, 'max_percentage': 89.99},
            {'grade': 'B+', 'min_percentage': 70, 'max_percentage': 79.99},
            {'grade': 'B', 'min_percentage': 60, 'max_percentage': 69.99},
            {'grade': 'C', 'min_percentage': 50, 'max_percentage': 59.99},
            {'grade': 'D', 'min_percentage': 40, 'max_percentage': 49.99},
            {'grade': 'F', 'min_percentage': 0, 'max_percentage': 39.99}
        ]
    
    # Add marks required for each boundary
    for boundary in boundaries:
        boundary['min_marks'] = round((boundary['min_percentage'] * total) / 100, 2)
        boundary['max_marks'] = round((boundary['max_percentage'] * total) / 100, 2)
    
    return boundaries


def generate_grade_recommendations(
    percentage: float,
    grade: str,
    passing_percentage: float,
    marks_lost: float,
    total: float
) -> List[str]:
    """Generate personalized recommendations based on performance"""
    recommendations = []
    
    if percentage >= 90:
        recommendations.extend([
            'Excellent work! You\'re performing at the highest level',
            'Maintain your study habits and consistency',
            'Consider helping peers who are struggling',
            'Challenge yourself with advanced topics'
        ])
    elif percentage >= 80:
        recommendations.extend([
            'Great performance! You\'re doing very well',
            'Review areas where you lost marks to reach 90%+',
            'Keep up the consistent effort',
            'Focus on perfecting your understanding'
        ])
    elif percentage >= 70:
        recommendations.extend([
            'Good work! Solid performance overall',
            'Identify weak areas and strengthen them',
            'Practice more problems in challenging topics',
            'Aim for 80%+ in your next assessment'
        ])
    elif percentage >= 60:
        recommendations.extend([
            'Satisfactory performance with room for improvement',
            'Review fundamental concepts thoroughly',
            'Increase study time and practice',
            'Seek help from teachers for difficult topics',
            'Create a structured study plan'
        ])
    elif percentage >= passing_percentage:
        recommendations.extend([
            'You\'ve passed, but there\'s significant room for improvement',
            'Focus on building strong fundamentals',
            'Dedicate more time to regular study',
            'Practice previous papers and exercises',
            'Don\'t hesitate to ask for help'
        ])
    else:
        recommendations.extend([
            '⚠️ Immediate action needed - below passing grade',
            'Meet with your teacher to discuss improvement strategies',
            'Identify specific topics causing difficulty',
            'Create a detailed study schedule',
            'Consider tutoring or study groups',
            'Focus on understanding, not memorization'
        ])
    
    # Specific recommendations based on marks lost
    if marks_lost > 0:
        loss_percentage = (marks_lost / total) * 100
        if loss_percentage > 20:
            recommendations.append(f'You lost {round(loss_percentage, 1)}% - review these areas carefully')
    
    return recommendations
