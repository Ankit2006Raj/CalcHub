"""
Professional Mathematical Expression Calculator Module
Provides comprehensive mathematical calculations with multiple functions and modes
"""

import math
import re
from typing import Dict, Union, List, Optional
from decimal import Decimal, ROUND_HALF_UP


class MathCalculationError(Exception):
    """Custom exception for math calculation errors"""
    pass


def evaluate_expression(
    expression: str,
    angle_mode: str = "degrees",
    precision: int = 10,
    detailed: bool = False
) -> Dict[str, Union[float, str, bool, List, Dict]]:
    """
    Evaluate mathematical expression with comprehensive analysis
    
    Args:
        expression: Mathematical expression to evaluate
        angle_mode: 'degrees' or 'radians' for trigonometric functions
        precision: Number of decimal places for result (default: 10)
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing result and detailed analysis
    
    Raises:
        MathCalculationError: If expression is invalid or cannot be evaluated
    """
    if not expression or not expression.strip():
        raise MathCalculationError("Expression cannot be empty.")
    
    original_expression = expression.strip()
    
    try:
        # Prepare expression for evaluation
        processed_expression = preprocess_expression(expression, angle_mode)
        
        # Create safe evaluation environment
        safe_dict = create_safe_environment()
        
        # Evaluate expression
        result = eval(processed_expression, {"__builtins__": {}}, safe_dict)
        
        # Round result if it's a float
        if isinstance(result, float):
            if math.isnan(result):
                raise MathCalculationError("Result is not a number (NaN).")
            if math.isinf(result):
                raise MathCalculationError("Result is infinity.")
            result = round(result, precision)
        
        # Backward compatibility: return simple format if detailed=False
        if not detailed:
            return {
                'result': result,
                'expression': processed_expression,
                'success': True
            }
        
        # Detailed analysis
        analysis = analyze_expression(original_expression, result)
        
        return {
            'result': result,
            'original_expression': original_expression,
            'processed_expression': processed_expression,
            'success': True,
            'result_type': type(result).__name__,
            'scientific_notation': f"{result:.{precision}e}" if isinstance(result, (int, float)) else None,
            'analysis': analysis,
            'angle_mode': angle_mode,
            'precision': precision,
            'alternative_forms': get_alternative_forms(result) if isinstance(result, (int, float)) else None
        }
        
    except ZeroDivisionError:
        return create_error_response(original_expression, "Division by zero is undefined.", detailed)
    except OverflowError:
        return create_error_response(original_expression, "Result is too large to compute.", detailed)
    except ValueError as e:
        return create_error_response(original_expression, f"Invalid value: {str(e)}", detailed)
    except SyntaxError:
        return create_error_response(original_expression, "Invalid mathematical syntax.", detailed)
    except Exception as e:
        return create_error_response(original_expression, f"Calculation error: {str(e)}", detailed)


def preprocess_expression(expression: str, angle_mode: str) -> str:
    """Preprocess expression to handle various mathematical notations"""
    # Replace power operator
    expression = expression.replace('^', '**')
    
    # Replace implicit multiplication (e.g., 2(3+4) -> 2*(3+4))
    expression = re.sub(r'(\d)\(', r'\1*(', expression)
    expression = re.sub(r'\)(\d)', r')*\1', expression)
    expression = re.sub(r'\)\(', r')*(', expression)
    
    # Handle trigonometric functions
    if angle_mode.lower() == "degrees":
        expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(math.radians(\1))', expression)
        expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(math.radians(\1))', expression)
        expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(math.radians(\1))', expression)
        expression = re.sub(r'asin\(([^)]+)\)', r'math.degrees(math.asin(\1))', expression)
        expression = re.sub(r'acos\(([^)]+)\)', r'math.degrees(math.acos(\1))', expression)
        expression = re.sub(r'atan\(([^)]+)\)', r'math.degrees(math.atan(\1))', expression)
    else:
        expression = re.sub(r'sin\(([^)]+)\)', r'math.sin(\1)', expression)
        expression = re.sub(r'cos\(([^)]+)\)', r'math.cos(\1)', expression)
        expression = re.sub(r'tan\(([^)]+)\)', r'math.tan(\1)', expression)
        expression = re.sub(r'asin\(([^)]+)\)', r'math.asin(\1)', expression)
        expression = re.sub(r'acos\(([^)]+)\)', r'math.acos(\1)', expression)
        expression = re.sub(r'atan\(([^)]+)\)', r'math.atan(\1)', expression)
    
    # Handle other mathematical functions
    expression = re.sub(r'sqrt\(([^)]+)\)', r'math.sqrt(\1)', expression)
    expression = re.sub(r'cbrt\(([^)]+)\)', r'(\1)**(1/3)', expression)
    expression = re.sub(r'log\(([^)]+)\)', r'math.log10(\1)', expression)
    expression = re.sub(r'ln\(([^)]+)\)', r'math.log(\1)', expression)
    expression = re.sub(r'exp\(([^)]+)\)', r'math.exp(\1)', expression)
    expression = re.sub(r'abs\(([^)]+)\)', r'abs(\1)', expression)
    expression = re.sub(r'ceil\(([^)]+)\)', r'math.ceil(\1)', expression)
    expression = re.sub(r'floor\(([^)]+)\)', r'math.floor(\1)', expression)
    expression = re.sub(r'round\(([^)]+)\)', r'round(\1)', expression)
    
    # Handle constants
    expression = re.sub(r'\bpi\b', 'math.pi', expression)
    expression = re.sub(r'\be\b', 'math.e', expression)
    
    # Handle factorial
    expression = re.sub(r'(\d+)!', r'math.factorial(\1)', expression)
    
    return expression


def create_safe_environment() -> Dict:
    """Create a safe environment for expression evaluation"""
    return {
        'math': math,
        'abs': abs,
        'round': round,
        'min': min,
        'max': max,
        'sum': sum,
        'pow': pow
    }


def analyze_expression(expression: str, result: Union[int, float]) -> Dict:
    """Analyze the expression and provide insights"""
    analysis = {
        'contains_trigonometry': bool(re.search(r'sin|cos|tan', expression, re.IGNORECASE)),
        'contains_logarithm': bool(re.search(r'log|ln', expression, re.IGNORECASE)),
        'contains_exponent': bool(re.search(r'\^|\*\*|exp', expression)),
        'contains_root': bool(re.search(r'sqrt|cbrt', expression, re.IGNORECASE)),
        'contains_factorial': '!' in expression,
        'expression_length': len(expression),
        'complexity': estimate_complexity(expression)
    }
    
    if isinstance(result, (int, float)):
        analysis['result_properties'] = {
            'is_integer': isinstance(result, int) or result.is_integer(),
            'is_positive': result > 0,
            'is_negative': result < 0,
            'is_zero': result == 0,
            'absolute_value': abs(result),
            'sign': 'positive' if result > 0 else ('negative' if result < 0 else 'zero')
        }
    
    return analysis


def estimate_complexity(expression: str) -> str:
    """Estimate the complexity of the expression"""
    operators = len(re.findall(r'[\+\-\*/\^]', expression))
    functions = len(re.findall(r'sin|cos|tan|log|ln|sqrt|exp', expression, re.IGNORECASE))
    parentheses = expression.count('(')
    
    score = operators + (functions * 2) + parentheses
    
    if score <= 3:
        return 'Simple'
    elif score <= 8:
        return 'Moderate'
    elif score <= 15:
        return 'Complex'
    else:
        return 'Very Complex'


def get_alternative_forms(result: Union[int, float]) -> Dict:
    """Get alternative representations of the result"""
    forms = {}
    
    if isinstance(result, float):
        # Check if it's close to a fraction
        from fractions import Fraction
        try:
            frac = Fraction(result).limit_denominator(1000)
            if abs(float(frac) - result) < 0.0001:
                forms['fraction'] = f"{frac.numerator}/{frac.denominator}"
        except:
            pass
        
        # Check if it's close to a multiple of pi
        if abs(result / math.pi - round(result / math.pi)) < 0.01:
            multiple = round(result / math.pi)
            if multiple == 1:
                forms['in_terms_of_pi'] = 'π'
            elif multiple == -1:
                forms['in_terms_of_pi'] = '-π'
            elif multiple != 0:
                forms['in_terms_of_pi'] = f'{multiple}π'
        
        # Check if it's close to e
        if abs(result / math.e - round(result / math.e)) < 0.01:
            multiple = round(result / math.e)
            if multiple == 1:
                forms['in_terms_of_e'] = 'e'
            elif multiple == -1:
                forms['in_terms_of_e'] = '-e'
            elif multiple != 0:
                forms['in_terms_of_e'] = f'{multiple}e'
    
    # Binary, octal, hexadecimal for integers
    if isinstance(result, int) or (isinstance(result, float) and result.is_integer()):
        int_result = int(result)
        if -1000000 < int_result < 1000000:  # Reasonable range
            forms['binary'] = bin(int_result)
            forms['octal'] = oct(int_result)
            forms['hexadecimal'] = hex(int_result)
    
    return forms if forms else None


def create_error_response(expression: str, error_message: str, detailed: bool) -> Dict:
    """Create a standardized error response"""
    if not detailed:
        return {
            'result': None,
            'expression': expression,
            'success': False,
            'error': error_message
        }
    
    return {
        'result': None,
        'original_expression': expression,
        'success': False,
        'error': error_message,
        'suggestions': [
            'Check for balanced parentheses',
            'Verify all operators are valid',
            'Ensure functions are spelled correctly',
            'Avoid division by zero',
            'Use supported functions: sin, cos, tan, log, ln, sqrt, exp, abs'
        ]
    }


# Additional utility functions for specific calculations

def calculate_statistics(numbers: List[Union[int, float]]) -> Dict:
    """Calculate statistical measures for a list of numbers"""
    if not numbers:
        raise MathCalculationError("Number list cannot be empty.")
    
    n = len(numbers)
    mean = sum(numbers) / n
    sorted_nums = sorted(numbers)
    
    # Median
    if n % 2 == 0:
        median = (sorted_nums[n//2 - 1] + sorted_nums[n//2]) / 2
    else:
        median = sorted_nums[n//2]
    
    # Mode
    from collections import Counter
    counts = Counter(numbers)
    max_count = max(counts.values())
    modes = [num for num, count in counts.items() if count == max_count]
    mode = modes[0] if len(modes) == 1 else modes
    
    # Variance and standard deviation
    variance = sum((x - mean) ** 2 for x in numbers) / n
    std_dev = math.sqrt(variance)
    
    return {
        'count': n,
        'sum': sum(numbers),
        'mean': round(mean, 6),
        'median': round(median, 6),
        'mode': mode,
        'range': max(numbers) - min(numbers),
        'min': min(numbers),
        'max': max(numbers),
        'variance': round(variance, 6),
        'standard_deviation': round(std_dev, 6)
    }


def solve_quadratic(a: float, b: float, c: float) -> Dict:
    """Solve quadratic equation ax² + bx + c = 0"""
    if a == 0:
        raise MathCalculationError("Coefficient 'a' cannot be zero for quadratic equation.")
    
    discriminant = b**2 - 4*a*c
    
    if discriminant > 0:
        root1 = (-b + math.sqrt(discriminant)) / (2*a)
        root2 = (-b - math.sqrt(discriminant)) / (2*a)
        return {
            'roots': [round(root1, 6), round(root2, 6)],
            'type': 'Two real roots',
            'discriminant': discriminant
        }
    elif discriminant == 0:
        root = -b / (2*a)
        return {
            'roots': [round(root, 6)],
            'type': 'One real root (repeated)',
            'discriminant': discriminant
        }
    else:
        real_part = -b / (2*a)
        imag_part = math.sqrt(abs(discriminant)) / (2*a)
        return {
            'roots': [
                f"{round(real_part, 6)} + {round(imag_part, 6)}i",
                f"{round(real_part, 6)} - {round(imag_part, 6)}i"
            ],
            'type': 'Two complex roots',
            'discriminant': discriminant
        }
