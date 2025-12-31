"""
Currency Converter Calculator Module
Provides real-time currency conversion with exchange rates
"""

from typing import Dict, List, Optional
from datetime import datetime


# Exchange rates (base: USD) - In production, fetch from API
EXCHANGE_RATES = {
    'USD': 1.0,
    'EUR': 0.92,
    'GBP': 0.79,
    'JPY': 149.50,
    'CNY': 7.24,
    'INR': 83.12,
    'AUD': 1.52,
    'CAD': 1.36,
    'CHF': 0.88,
    'MXN': 17.08,
    'BRL': 4.97,
    'ZAR': 18.65,
    'RUB': 92.50,
    'KRW': 1310.50,
    'SGD': 1.34,
    'HKD': 7.82,
    'NOK': 10.58,
    'SEK': 10.35,
    'DKK': 6.86,
    'NZD': 1.63,
    'AED': 3.67,
    'SAR': 3.75,
    'THB': 35.20,
    'MYR': 4.68
}

CURRENCY_NAMES = {
    'USD': 'US Dollar',
    'EUR': 'Euro',
    'GBP': 'British Pound',
    'JPY': 'Japanese Yen',
    'CNY': 'Chinese Yuan',
    'INR': 'Indian Rupee',
    'AUD': 'Australian Dollar',
    'CAD': 'Canadian Dollar',
    'CHF': 'Swiss Franc',
    'MXN': 'Mexican Peso',
    'BRL': 'Brazilian Real',
    'ZAR': 'South African Rand',
    'RUB': 'Russian Ruble',
    'KRW': 'South Korean Won',
    'SGD': 'Singapore Dollar',
    'HKD': 'Hong Kong Dollar',
    'NOK': 'Norwegian Krone',
    'SEK': 'Swedish Krona',
    'DKK': 'Danish Krone',
    'NZD': 'New Zealand Dollar',
    'AED': 'UAE Dirham',
    'SAR': 'Saudi Riyal',
    'THB': 'Thai Baht',
    'MYR': 'Malaysian Ringgit'
}


def convert_currency(amount: float, from_currency: str, to_currency: str) -> Dict:
    """
    Convert amount from one currency to another
    
    Args:
        amount: Amount to convert
        from_currency: Source currency code (e.g., 'USD')
        to_currency: Target currency code (e.g., 'EUR')
    
    Returns:
        Dictionary with conversion results
    """
    from_currency = from_currency.upper()
    to_currency = to_currency.upper()
    
    if from_currency not in EXCHANGE_RATES:
        return {'error': f'Currency {from_currency} not supported'}
    if to_currency not in EXCHANGE_RATES:
        return {'error': f'Currency {to_currency} not supported'}
    if amount <= 0:
        return {'error': 'Amount must be greater than zero'}
    
    # Convert to USD first, then to target currency
    amount_in_usd = amount / EXCHANGE_RATES[from_currency]
    converted_amount = amount_in_usd * EXCHANGE_RATES[to_currency]
    
    exchange_rate = EXCHANGE_RATES[to_currency] / EXCHANGE_RATES[from_currency]
    
    return {
        'original_amount': round(amount, 2),
        'converted_amount': round(converted_amount, 2),
        'from_currency': from_currency,
        'to_currency': to_currency,
        'from_currency_name': CURRENCY_NAMES[from_currency],
        'to_currency_name': CURRENCY_NAMES[to_currency],
        'exchange_rate': round(exchange_rate, 6),
        'inverse_rate': round(1 / exchange_rate, 6),
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }


def get_all_currencies() -> List[Dict]:
    """Get list of all supported currencies"""
    return [
        {'code': code, 'name': name, 'rate': rate}
        for code, (name, rate) in 
        zip(EXCHANGE_RATES.keys(), zip(CURRENCY_NAMES.values(), EXCHANGE_RATES.values()))
    ]


def compare_multiple_currencies(amount: float, from_currency: str, to_currencies: List[str]) -> Dict:
    """
    Compare conversion to multiple currencies
    
    Args:
        amount: Amount to convert
        from_currency: Source currency
        to_currencies: List of target currencies
    
    Returns:
        Dictionary with multiple conversions
    """
    results = []
    for to_currency in to_currencies:
        result = convert_currency(amount, from_currency, to_currency)
        if 'error' not in result:
            results.append(result)
    
    return {
        'original_amount': amount,
        'from_currency': from_currency.upper(),
        'conversions': results
    }
