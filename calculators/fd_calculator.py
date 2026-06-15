from typing import Dict

def calculate_fd(
    principal: float,
    annual_rate: float,
    years: float,
    compounding_frequency: str = 'quarterly'
) -> Dict:
    """
    Calculate Fixed Deposit Maturity Amount and Interest Earned.
    compounding_frequency options: 'monthly', 'quarterly', 'half-yearly', 'yearly'
    """
    freq_map = {
        'monthly': 12,
        'quarterly': 4,
        'half-yearly': 2,
        'yearly': 1
    }
    
    n = freq_map.get(compounding_frequency.lower(), 4)
    r = annual_rate / 100.0
    
    maturity_amount = principal * ((1 + (r / n)) ** (n * years))
    total_interest = maturity_amount - principal
    
    return {
        'principal': round(principal, 2),
        'interest_rate': round(annual_rate, 2),
        'duration_years': round(years, 2),
        'compounding_frequency': compounding_frequency.capitalize(),
        'maturity_amount': round(maturity_amount, 2),
        'total_interest': round(total_interest, 2)
    }
