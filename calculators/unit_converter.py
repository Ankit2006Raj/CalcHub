"""
Unit Converter Calculator Module
Supports length, weight, temperature, volume, area, speed conversions
"""

from typing import Dict, List


# Conversion factors (to base unit)
CONVERSIONS = {
    'length': {
        'base': 'meter',
        'units': {
            'meter': 1,
            'kilometer': 1000,
            'centimeter': 0.01,
            'millimeter': 0.001,
            'mile': 1609.34,
            'yard': 0.9144,
            'foot': 0.3048,
            'inch': 0.0254
        }
    },
    'weight': {
        'base': 'kilogram',
        'units': {
            'kilogram': 1,
            'gram': 0.001,
            'milligram': 0.000001,
            'metric_ton': 1000,
            'pound': 0.453592,
            'ounce': 0.0283495,
            'stone': 6.35029
        }
    },
    'volume': {
        'base': 'liter',
        'units': {
            'liter': 1,
            'milliliter': 0.001,
            'cubic_meter': 1000,
            'gallon_us': 3.78541,
            'gallon_uk': 4.54609,
            'quart': 0.946353,
            'pint': 0.473176,
            'cup': 0.236588,
            'fluid_ounce': 0.0295735,
            'tablespoon': 0.0147868,
            'teaspoon': 0.00492892
        }
    },
    'temperature': {
        'base': 'celsius',
        'units': ['celsius', 'fahrenheit', 'kelvin']
    },
    'area': {
        'base': 'square_meter',
        'units': {
            'square_meter': 1,
            'square_kilometer': 1000000,
            'square_centimeter': 0.0001,
            'hectare': 10000,
            'acre': 4046.86,
            'square_mile': 2589988,
            'square_yard': 0.836127,
            'square_foot': 0.092903,
            'square_inch': 0.00064516
        }
    },
    'speed': {
        'base': 'meter_per_second',
        'units': {
            'meter_per_second': 1,
            'kilometer_per_hour': 0.277778,
            'mile_per_hour': 0.44704,
            'foot_per_second': 0.3048,
            'knot': 0.514444
        }
    }
}


def convert_unit(value: float, from_unit: str, to_unit: str, category: str) -> Dict:
    """
    Convert value from one unit to another
    
    Args:
        value: Value to convert
        from_unit: Source unit
        to_unit: Target unit
        category: Unit category (length, weight, temperature, etc.)
    
    Returns:
        Dictionary with conversion results
    """
    if category not in CONVERSIONS:
        return {'error': f'Category {category} not supported'}
    
    # Special handling for temperature
    if category == 'temperature':
        return convert_temperature(value, from_unit, to_unit)
    
    units = CONVERSIONS[category]['units']
    
    if from_unit not in units:
        return {'error': f'Unit {from_unit} not found in {category}'}
    if to_unit not in units:
        return {'error': f'Unit {to_unit} not found in {category}'}
    
    # Convert to base unit, then to target unit
    base_value = value * units[from_unit]
    result = base_value / units[to_unit]
    
    return {
        'original_value': value,
        'converted_value': round(result, 6),
        'from_unit': from_unit,
        'to_unit': to_unit,
        'category': category,
        'formula': f'{value} {from_unit} = {round(result, 6)} {to_unit}'
    }


def convert_temperature(value: float, from_unit: str, to_unit: str) -> Dict:
    """Convert temperature between Celsius, Fahrenheit, and Kelvin"""
    
    # Convert to Celsius first
    if from_unit == 'celsius':
        celsius = value
    elif from_unit == 'fahrenheit':
        celsius = (value - 32) * 5/9
    elif from_unit == 'kelvin':
        celsius = value - 273.15
    else:
        return {'error': f'Temperature unit {from_unit} not supported'}
    
    # Convert from Celsius to target
    if to_unit == 'celsius':
        result = celsius
    elif to_unit == 'fahrenheit':
        result = (celsius * 9/5) + 32
    elif to_unit == 'kelvin':
        result = celsius + 273.15
    else:
        return {'error': f'Temperature unit {to_unit} not supported'}
    
    return {
        'original_value': value,
        'converted_value': round(result, 2),
        'from_unit': from_unit,
        'to_unit': to_unit,
        'category': 'temperature',
        'formula': f'{value}° {from_unit.capitalize()} = {round(result, 2)}° {to_unit.capitalize()}'
    }


def get_all_units(category: str) -> List[str]:
    """Get all units for a category"""
    if category not in CONVERSIONS:
        return []
    
    if category == 'temperature':
        return CONVERSIONS[category]['units']
    
    return list(CONVERSIONS[category]['units'].keys())


def get_all_categories() -> List[str]:
    """Get all available categories"""
    return list(CONVERSIONS.keys())
