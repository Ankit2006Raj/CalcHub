"""
Professional GPA/CGPA Calculator Module
Provides comprehensive academic performance analysis and predictions
"""

from typing import Dict, Union, List, Optional


class GPACalculationError(Exception):
    """Custom exception for GPA calculation errors"""
    pass


def calculate_gpa(
    courses: List[Dict],
    scale: str = "4.0",
    previous_gpa: Optional[float] = None,
    previous_credits: Optional[float] = None,
    detailed: bool = False
) -> Dict[str, Union[float, str, List, Dict]]:
    """
    Calculate comprehensive GPA with academic performance analysis
    
    Args:
        courses: List of course dictionaries with 'grade' and 'credits'
        scale: GPA scale - "4.0" or "5.0"
        previous_gpa: Optional previous semester/cumulative GPA
        previous_credits: Optional previous total credits
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed GPA analysis and predictions
    
    Raises:
        GPACalculationError: If input parameters are invalid
    """
    if not courses:
        raise GPACalculationError("Course list cannot be empty.")
    
    # Get grade point mapping based on scale
    grade_points = get_grade_points(scale)
    
    # Calculate current semester GPA
    total_points = 0
    total_credits = 0
    course_details = []
    
    for course in courses:
        if 'grade' not in course or 'credits' not in course:
            raise GPACalculationError("Each course must have 'grade' and 'credits' fields.")
        
        grade = course['grade'].upper().strip()
        try:
            credits = float(course['credits'])
        except ValueError:
            raise GPACalculationError(f"Invalid credits value: {course['credits']}")
        
        if credits <= 0:
            raise GPACalculationError("Credits must be greater than zero.")
        
        if grade not in grade_points:
            raise GPACalculationError(f"Invalid grade: {grade}. Use grades like A+, A, A-, B+, B, etc.")
        
        points = grade_points[grade] * credits
        total_points += points
        total_credits += credits
        
        course_details.append({
            'course_name': course.get('name', 'Unnamed Course'),
            'grade': grade,
            'credits': credits,
            'grade_points': grade_points[grade],
            'quality_points': round(points, 2)
        })
    
    # Calculate semester GPA
    semester_gpa = total_points / total_credits if total_credits > 0 else 0
    
    # Calculate cumulative GPA if previous data provided
    cumulative_gpa = None
    cumulative_credits = total_credits
    
    if previous_gpa is not None and previous_credits is not None:
        if previous_credits < 0:
            raise GPACalculationError("Previous credits cannot be negative.")
        if previous_gpa < 0 or previous_gpa > float(scale):
            raise GPACalculationError(f"Previous GPA must be between 0 and {scale}.")
        
        previous_points = previous_gpa * previous_credits
        cumulative_points = previous_points + total_points
        cumulative_credits = previous_credits + total_credits
        cumulative_gpa = cumulative_points / cumulative_credits if cumulative_credits > 0 else 0
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'gpa': round(semester_gpa, 2),
            'total_credits': total_credits,
            'grade': get_letter_grade(semester_gpa, scale)
        }
    
    # Calculate detailed analytics
    grade_distribution = calculate_grade_distribution(course_details, grade_points)
    performance_analysis = analyze_performance(semester_gpa, cumulative_gpa, scale)
    
    # Calculate predictions
    predictions = calculate_gpa_predictions(
        cumulative_gpa if cumulative_gpa else semester_gpa,
        cumulative_credits,
        scale
    )
    
    # Calculate what-if scenarios
    scenarios = calculate_what_if_scenarios(
        cumulative_gpa if cumulative_gpa else semester_gpa,
        cumulative_credits,
        scale
    )
    
    # Generate recommendations
    recommendations = generate_gpa_recommendations(
        semester_gpa,
        cumulative_gpa,
        grade_distribution,
        scale
    )
    
    result = {
        'semester_gpa': {
            'gpa': round(semester_gpa, 2),
            'letter_grade': get_letter_grade(semester_gpa, scale),
            'credits_earned': total_credits,
            'quality_points': round(total_points, 2),
            'scale': scale
        },
        'course_details': course_details,
        'grade_distribution': grade_distribution,
        'performance_analysis': performance_analysis,
        'predictions': predictions,
        'what_if_scenarios': scenarios,
        'recommendations': recommendations
    }
    
    # Add cumulative GPA if available
    if cumulative_gpa is not None:
        result['cumulative_gpa'] = {
            'gpa': round(cumulative_gpa, 2),
            'letter_grade': get_letter_grade(cumulative_gpa, scale),
            'total_credits': cumulative_credits,
            'previous_gpa': previous_gpa,
            'previous_credits': previous_credits,
            'gpa_change': round(cumulative_gpa - previous_gpa, 2) if previous_gpa else 0
        }
    
    result['notes'] = [
        'GPA is calculated as total quality points divided by total credits',
        'Quality points = grade points × credit hours',
        'Maintain consistent performance across all courses',
        'Seek help early if struggling in any course'
    ]
    
    return result


def get_grade_points(scale: str) -> Dict[str, float]:
    """Get grade point mapping based on scale"""
    if scale == "5.0":
        return {
            'A+': 5.0, 'A': 5.0, 'A-': 4.7,
            'B+': 4.3, 'B': 4.0, 'B-': 3.7,
            'C+': 3.3, 'C': 3.0, 'C-': 2.7,
            'D+': 2.3, 'D': 2.0, 'D-': 1.7,
            'F': 0.0
        }
    else:  # Default 4.0 scale
        return {
            'A+': 4.0, 'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0, 'D-': 0.7,
            'F': 0.0
        }


def get_letter_grade(gpa: float, scale: str = "4.0") -> str:
    """Convert GPA to letter grade"""
    max_gpa = 5.0 if scale == "5.0" else 4.0
    
    if scale == "5.0":
        if gpa >= 4.7: return 'A'
        elif gpa >= 4.3: return 'A-'
        elif gpa >= 4.0: return 'B+'
        elif gpa >= 3.7: return 'B'
        elif gpa >= 3.3: return 'B-'
        elif gpa >= 3.0: return 'C+'
        elif gpa >= 2.7: return 'C'
        elif gpa >= 2.0: return 'D'
        else: return 'F'
    else:
        if gpa >= 3.7: return 'A'
        elif gpa >= 3.3: return 'A-'
        elif gpa >= 3.0: return 'B+'
        elif gpa >= 2.7: return 'B'
        elif gpa >= 2.3: return 'B-'
        elif gpa >= 2.0: return 'C+'
        elif gpa >= 1.7: return 'C'
        elif gpa >= 1.0: return 'D'
        else: return 'F'


def calculate_grade_distribution(course_details: List[Dict], grade_points: Dict) -> Dict:
    """Calculate grade distribution statistics"""
    grade_counts = {}
    total_courses = len(course_details)
    
    for course in course_details:
        grade = course['grade']
        grade_counts[grade] = grade_counts.get(grade, 0) + 1
    
    distribution = {}
    for grade, count in grade_counts.items():
        distribution[grade] = {
            'count': count,
            'percentage': round((count / total_courses) * 100, 1),
            'grade_points': grade_points[grade]
        }
    
    # Calculate statistics
    grades_list = [course['grade_points'] for course in course_details]
    
    return {
        'by_grade': distribution,
        'total_courses': total_courses,
        'highest_grade': max(grades_list),
        'lowest_grade': min(grades_list),
        'average_grade_points': round(sum(grades_list) / len(grades_list), 2)
    }


def analyze_performance(semester_gpa: float, cumulative_gpa: Optional[float], scale: str) -> Dict:
    """Analyze academic performance"""
    max_gpa = 5.0 if scale == "5.0" else 4.0
    
    # Determine performance level
    gpa_to_analyze = cumulative_gpa if cumulative_gpa else semester_gpa
    
    if gpa_to_analyze >= max_gpa * 0.9:
        level = 'Excellent'
        description = 'Outstanding academic performance'
        color = '#2ecc71'
    elif gpa_to_analyze >= max_gpa * 0.75:
        level = 'Good'
        description = 'Strong academic performance'
        color = '#27ae60'
    elif gpa_to_analyze >= max_gpa * 0.60:
        level = 'Satisfactory'
        description = 'Acceptable academic performance'
        color = '#f39c12'
    elif gpa_to_analyze >= max_gpa * 0.50:
        level = 'Needs Improvement'
        description = 'Below average performance'
        color = '#e67e22'
    else:
        level = 'Critical'
        description = 'Significant improvement needed'
        color = '#e74c3c'
    
    analysis = {
        'performance_level': level,
        'description': description,
        'color': color,
        'percentage_of_max': round((gpa_to_analyze / max_gpa) * 100, 1)
    }
    
    # Compare semester to cumulative if available
    if cumulative_gpa is not None:
        trend = 'improving' if semester_gpa > cumulative_gpa else ('declining' if semester_gpa < cumulative_gpa else 'stable')
        analysis['trend'] = trend
        analysis['semester_vs_cumulative'] = round(semester_gpa - cumulative_gpa, 2)
    
    return analysis


def calculate_gpa_predictions(current_gpa: float, current_credits: float, scale: str) -> Dict:
    """Calculate GPA predictions for future semesters"""
    max_gpa = 5.0 if scale == "5.0" else 4.0
    predictions = {}
    
    # Predict for different credit scenarios
    for future_credits in [12, 15, 18, 30, 60]:
        predictions[f'after_{future_credits}_credits'] = {}
        
        # Best case: All A's
        best_case_points = current_gpa * current_credits + max_gpa * future_credits
        best_case_gpa = best_case_points / (current_credits + future_credits)
        
        # Worst case: All F's
        worst_case_points = current_gpa * current_credits
        worst_case_gpa = worst_case_points / (current_credits + future_credits)
        
        # Maintain current GPA
        maintain_gpa = current_gpa
        
        predictions[f'after_{future_credits}_credits'] = {
            'best_case': round(best_case_gpa, 2),
            'worst_case': round(worst_case_gpa, 2),
            'if_maintain_current': round(maintain_gpa, 2),
            'total_credits': current_credits + future_credits
        }
    
    return predictions


def calculate_what_if_scenarios(current_gpa: float, current_credits: float, scale: str) -> List[Dict]:
    """Calculate what-if scenarios for GPA goals"""
    max_gpa = 5.0 if scale == "5.0" else 4.0
    scenarios = []
    
    # Target GPAs to achieve
    targets = [3.0, 3.5, 4.0] if scale == "4.0" else [3.5, 4.0, 4.5, 5.0]
    
    for target in targets:
        if target <= max_gpa:
            scenario = {'target_gpa': target, 'scenarios': []}
            
            for credits in [12, 15, 18, 30]:
                # Calculate required GPA in next semester
                required_points = target * (current_credits + credits) - current_gpa * current_credits
                required_gpa = required_points / credits if credits > 0 else 0
                
                achievable = 0 <= required_gpa <= max_gpa
                
                scenario['scenarios'].append({
                    'credits': credits,
                    'required_semester_gpa': round(required_gpa, 2),
                    'achievable': achievable,
                    'difficulty': get_difficulty_level(required_gpa, max_gpa)
                })
            
            scenarios.append(scenario)
    
    return scenarios


def get_difficulty_level(required_gpa: float, max_gpa: float) -> str:
    """Determine difficulty level of achieving required GPA"""
    if required_gpa > max_gpa:
        return 'Impossible'
    elif required_gpa >= max_gpa * 0.95:
        return 'Very Difficult'
    elif required_gpa >= max_gpa * 0.85:
        return 'Difficult'
    elif required_gpa >= max_gpa * 0.75:
        return 'Moderate'
    elif required_gpa >= max_gpa * 0.60:
        return 'Achievable'
    else:
        return 'Easy'


def generate_gpa_recommendations(
    semester_gpa: float,
    cumulative_gpa: Optional[float],
    grade_distribution: Dict,
    scale: str
) -> List[str]:
    """Generate personalized academic recommendations"""
    recommendations = []
    max_gpa = 5.0 if scale == "5.0" else 4.0
    
    gpa_to_check = cumulative_gpa if cumulative_gpa else semester_gpa
    
    if gpa_to_check >= max_gpa * 0.9:
        recommendations.extend([
            'Excellent work! Maintain your study habits',
            'Consider taking more challenging courses',
            'You\'re on track for academic honors',
            'Share your study strategies with peers'
        ])
    elif gpa_to_check >= max_gpa * 0.75:
        recommendations.extend([
            'Good performance! Keep up the consistent effort',
            'Identify areas where you can improve further',
            'Consider joining study groups for challenging subjects',
            'Aim for higher grades in your major courses'
        ])
    elif gpa_to_check >= max_gpa * 0.60:
        recommendations.extend([
            'Focus on improving study habits and time management',
            'Seek help from professors during office hours',
            'Consider tutoring for difficult subjects',
            'Review and strengthen foundational concepts',
            'Create a structured study schedule'
        ])
    else:
        recommendations.extend([
            '⚠️ Immediate action needed to improve GPA',
            'Meet with academic advisor to create improvement plan',
            'Utilize all available academic support resources',
            'Consider reducing course load to focus on quality',
            'Identify and address underlying challenges',
            'Set specific, achievable goals for each course'
        ])
    
    # Check grade distribution
    if 'by_grade' in grade_distribution:
        low_grades = sum(1 for grade, data in grade_distribution['by_grade'].items() 
                        if data['grade_points'] < max_gpa * 0.6)
        if low_grades > 0:
            recommendations.append(f'Focus on improving performance in {low_grades} course(s) with lower grades')
    
    return recommendations
