"""
Mortgage Calculator Module
Calculate mortgage payments, amortization schedules, and affordability metrics
"""

from typing import Dict, List
from decimal import Decimal, ROUND_HALF_UP


def calculate_mortgage(
    home_price: float,
    down_payment: float,
    interest_rate: float,
    loan_term: int,
    property_tax: float = 0,
    home_insurance: float = 0,
    pmi: float = 0,
    hoa_fees: float = 0
) -> Dict:
    """
    Calculate comprehensive mortgage information
    
    Args:
        home_price: Total home price
        down_payment: Down payment amount
        interest_rate: Annual interest rate (percentage)
        loan_term: Loan term in years
        property_tax: Annual property tax
        home_insurance: Annual home insurance
        pmi: Monthly PMI (Private Mortgage Insurance)
        hoa_fees: Monthly HOA fees
    
    Returns:
        Dictionary with mortgage details and amortization schedule
    """
    # Calculate loan amount
    loan_amount = home_price - down_payment
    down_payment_percent = (down_payment / home_price) * 100
    
    # Convert to Decimal for precision
    principal = Decimal(str(loan_amount))
    annual_rate = Decimal(str(interest_rate))
    years = loan_term
    
    # Calculate monthly payment
    monthly_rate = annual_rate / (Decimal('12') * Decimal('100'))
    months = years * 12
    
    if monthly_rate == 0:
        monthly_payment = principal / Decimal(str(months))
    else:
        monthly_payment = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
                         ((1 + monthly_rate) ** months - 1)
    
    monthly_payment = monthly_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Additional monthly costs
    monthly_property_tax = Decimal(str(property_tax)) / Decimal('12')
    monthly_insurance = Decimal(str(home_insurance)) / Decimal('12')
    monthly_pmi = Decimal(str(pmi))
    monthly_hoa = Decimal(str(hoa_fees))
    
    total_monthly_payment = monthly_payment + monthly_property_tax + monthly_insurance + monthly_pmi + monthly_hoa
    
    # Generate amortization schedule
    schedule = []
    balance = principal
    total_interest = Decimal('0')
    
    for month in range(1, months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = monthly_payment - interest_payment
        balance -= principal_payment
        
        total_interest += interest_payment
        
        schedule.append({
            'month': month,
            'payment': float(monthly_payment),
            'principal': float(principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'interest': float(interest_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'balance': float(max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        })
    
    total_paid = monthly_payment * Decimal(str(months))
    
    return {
        'home_price': home_price,
        'down_payment': down_payment,
        'down_payment_percent': round(down_payment_percent, 2),
        'loan_amount': float(principal),
        'interest_rate': interest_rate,
        'loan_term_years': loan_term,
        'monthly_principal_interest': float(monthly_payment),
        'monthly_property_tax': float(monthly_property_tax.quantize(Decimal('0.01'))),
        'monthly_insurance': float(monthly_insurance.quantize(Decimal('0.01'))),
        'monthly_pmi': float(monthly_pmi),
        'monthly_hoa': float(monthly_hoa),
        'total_monthly_payment': float(total_monthly_payment.quantize(Decimal('0.01'))),
        'total_interest': float(total_interest.quantize(Decimal('0.01'))),
        'total_paid': float(total_paid.quantize(Decimal('0.01'))),
        'total_cost': float((total_paid + Decimal(str(down_payment))).quantize(Decimal('0.01'))),
        'amortization_schedule': schedule[:12],  # First year
        'ltv_ratio': round((loan_amount / home_price) * 100, 2),
        'recommended_income': float((total_monthly_payment / Decimal('0.28')).quantize(Decimal('0.01')))
    }
