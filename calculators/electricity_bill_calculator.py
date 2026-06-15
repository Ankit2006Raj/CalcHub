from typing import Dict

def calculate_electricity_bill(
    units: float,
    rate_per_unit: float,
    fixed_charge: float = 0.0,
    tax_percentage: float = 0.0
) -> Dict:
    """
    Calculate electricity bill based on units consumed, flat rate, fixed charges and taxes.
    """
    energy_charge = units * rate_per_unit
    subtotal = energy_charge + fixed_charge
    tax_amount = subtotal * (tax_percentage / 100.0)
    total_bill = subtotal + tax_amount
    
    return {
        'units_consumed': round(units, 2),
        'rate_per_unit': round(rate_per_unit, 2),
        'energy_charge': round(energy_charge, 2),
        'fixed_charge': round(fixed_charge, 2),
        'subtotal': round(subtotal, 2),
        'tax_amount': round(tax_amount, 2),
        'total_bill': round(total_bill, 2)
    }
