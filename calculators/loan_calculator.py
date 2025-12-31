"""
Professional Loan EMI Calculator Module
Provides comprehensive loan calculations with amortization schedules and analysis
"""

from typing import Dict, List, Union, Optional
from decimal import Decimal, ROUND_HALF_UP
import math


class LoanCalculationError(Exception):
    """Custom exception for loan calculation errors"""
    pass


def calculate_loan(
    amount: float,
    rate: float,
    duration: float,
    loan_type: str = "reducing",
    prepayment: Optional[float] = None,
    prepayment_month: Optional[int] = None,
    detailed: bool = False
) -> Dict[str, Union[float, int, str, List, Dict]]:
    """
    Calculate comprehensive loan EMI with detailed amortization schedule
    
    Args:
        amount: Principal loan amount
        rate: Annual interest rate (percentage)
        duration: Loan duration in years
        loan_type: Type of loan - "reducing" or "flat" (default: reducing)
        prepayment: Optional prepayment amount
        prepayment_month: Month number for prepayment
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed loan information and amortization schedule
    
    Raises:
        LoanCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if amount <= 0:
        raise LoanCalculationError("Loan amount must be greater than zero.")
    if rate < 0:
        raise LoanCalculationError("Interest rate cannot be negative.")
    if duration <= 0:
        raise LoanCalculationError("Loan duration must be greater than zero.")
    if amount > 100000000:  # 100 million limit
        raise LoanCalculationError("Loan amount exceeds maximum limit.")
    if rate > 50:
        raise LoanCalculationError("Interest rate seems unusually high. Please verify.")
    if duration > 40:
        raise LoanCalculationError("Loan duration exceeds maximum limit of 40 years.")
    
    # Convert to Decimal for precise calculations
    principal = Decimal(str(amount))
    annual_rate = Decimal(str(rate))
    years = Decimal(str(duration))
    
    # Calculate based on loan type
    if loan_type.lower() == "flat":
        result = calculate_flat_rate_loan(principal, annual_rate, years)
    else:
        result = calculate_reducing_balance_loan(principal, annual_rate, years, prepayment, prepayment_month)
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'emi': result['emi'],
            'total_interest': result['total_interest'],
            'total_payment': result['total_payment'],
            'principal': result['principal']
        }
    
    return result


def calculate_reducing_balance_loan(
    principal: Decimal,
    annual_rate: Decimal,
    years: Decimal,
    prepayment: Optional[float] = None,
    prepayment_month: Optional[int] = None
) -> Dict:
    """Calculate loan with reducing balance method (most common)"""
    
    monthly_rate = annual_rate / (Decimal('12') * Decimal('100'))
    months = int(years * 12)
    
    # Calculate EMI
    if monthly_rate == 0:
        emi = principal / Decimal(str(months))
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    
    # Round EMI to 2 decimal places
    emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Generate amortization schedule
    schedule = []
    balance = principal
    total_interest_paid = Decimal('0')
    total_principal_paid = Decimal('0')
    
    for month in range(1, months + 1):
        interest_payment = balance * monthly_rate
        principal_payment = emi - interest_payment
        
        # Handle prepayment
        if prepayment and prepayment_month and month == prepayment_month:
            prepayment_amount = Decimal(str(prepayment))
            principal_payment += prepayment_amount
            balance -= principal_payment
            
            schedule.append({
                'month': month,
                'emi': float(emi + prepayment_amount),
                'principal': float(principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'interest': float(interest_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'balance': float(max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'prepayment': float(prepayment_amount)
            })
        else:
            balance -= principal_payment
            
            schedule.append({
                'month': month,
                'emi': float(emi),
                'principal': float(principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'interest': float(interest_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'balance': float(max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
                'prepayment': 0
            })
        
        total_interest_paid += interest_payment
        total_principal_paid += principal_payment
        
        # Break if loan is fully paid
        if balance <= 0:
            break
    
    total_payment = emi * Decimal(str(len(schedule)))
    
    # Calculate yearly summary
    yearly_summary = calculate_yearly_summary(schedule)
    
    # Calculate break-even analysis
    break_even = calculate_break_even(float(principal), float(annual_rate), months)
    
    # Calculate affordability metrics
    affordability = calculate_affordability_metrics(float(emi), float(principal))
    
    return {
        'loan_type': 'Reducing Balance',
        'emi': float(emi),
        'monthly_payment': float(emi),
        'total_interest': float(total_interest_paid.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'total_payment': float(total_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'principal': float(principal),
        'interest_rate': float(annual_rate),
        'duration_years': float(years),
        'duration_months': months,
        'actual_months_to_payoff': len(schedule),
        'interest_to_principal_ratio': float((total_interest_paid / principal * 100).quantize(Decimal('0.01'))),
        'amortization_schedule': schedule,
        'yearly_summary': yearly_summary,
        'break_even_analysis': break_even,
        'affordability_metrics': affordability,
        'first_month_breakdown': {
            'principal': schedule[0]['principal'],
            'interest': schedule[0]['interest'],
            'principal_percentage': round((schedule[0]['principal'] / float(emi)) * 100, 2),
            'interest_percentage': round((schedule[0]['interest'] / float(emi)) * 100, 2)
        },
        'last_month_breakdown': {
            'principal': schedule[-1]['principal'],
            'interest': schedule[-1]['interest'],
            'principal_percentage': round((schedule[-1]['principal'] / float(emi)) * 100, 2),
            'interest_percentage': round((schedule[-1]['interest'] / float(emi)) * 100, 2)
        }
    }


def calculate_flat_rate_loan(principal: Decimal, annual_rate: Decimal, years: Decimal) -> Dict:
    """Calculate loan with flat rate method"""
    
    months = int(years * 12)
    
    # Calculate total interest (flat rate applies to original principal)
    total_interest = principal * (annual_rate / Decimal('100')) * years
    total_payment = principal + total_interest
    emi = total_payment / Decimal(str(months))
    
    # Round to 2 decimal places
    emi = emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_interest = total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    total_payment = total_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    
    # Generate simple schedule
    schedule = []
    principal_per_month = principal / Decimal(str(months))
    interest_per_month = total_interest / Decimal(str(months))
    
    for month in range(1, months + 1):
        balance = principal - (principal_per_month * Decimal(str(month)))
        schedule.append({
            'month': month,
            'emi': float(emi),
            'principal': float(principal_per_month.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'interest': float(interest_per_month.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'balance': float(max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'prepayment': 0
        })
    
    yearly_summary = calculate_yearly_summary(schedule)
    
    return {
        'loan_type': 'Flat Rate',
        'emi': float(emi),
        'monthly_payment': float(emi),
        'total_interest': float(total_interest),
        'total_payment': float(total_payment),
        'principal': float(principal),
        'interest_rate': float(annual_rate),
        'duration_years': float(years),
        'duration_months': months,
        'actual_months_to_payoff': months,
        'interest_to_principal_ratio': float((total_interest / principal * 100).quantize(Decimal('0.01'))),
        'amortization_schedule': schedule,
        'yearly_summary': yearly_summary,
        'note': 'Flat rate loans have equal interest payments throughout the loan term'
    }


def calculate_yearly_summary(schedule: List[Dict]) -> List[Dict]:
    """Calculate yearly summary from monthly schedule"""
    yearly_summary = []
    current_year = {'year': 1, 'principal': 0, 'interest': 0, 'total_paid': 0}
    
    for i, month_data in enumerate(schedule, 1):
        current_year['principal'] += month_data['principal']
        current_year['interest'] += month_data['interest']
        current_year['total_paid'] += month_data['emi']
        
        if i % 12 == 0 or i == len(schedule):
            yearly_summary.append({
                'year': current_year['year'],
                'principal_paid': round(current_year['principal'], 2),
                'interest_paid': round(current_year['interest'], 2),
                'total_paid': round(current_year['total_paid'], 2),
                'ending_balance': month_data['balance']
            })
            current_year = {'year': current_year['year'] + 1, 'principal': 0, 'interest': 0, 'total_paid': 0}
    
    return yearly_summary


def calculate_break_even(principal: float, annual_rate: float, months: int) -> Dict:
    """Calculate when principal paid exceeds interest paid"""
    monthly_rate = annual_rate / (12 * 100)
    
    if monthly_rate == 0:
        emi = principal / months
    else:
        emi = (principal * monthly_rate * (1 + monthly_rate) ** months) / \
              ((1 + monthly_rate) ** months - 1)
    
    balance = principal
    cumulative_principal = 0
    cumulative_interest = 0
    break_even_month = None
    
    for month in range(1, months + 1):
        interest = balance * monthly_rate
        principal_payment = emi - interest
        balance -= principal_payment
        
        cumulative_principal += principal_payment
        cumulative_interest += interest
        
        if cumulative_principal > cumulative_interest and break_even_month is None:
            break_even_month = month
            break
    
    return {
        'break_even_month': break_even_month if break_even_month else months,
        'break_even_year': round((break_even_month if break_even_month else months) / 12, 1),
        'message': f"Principal paid exceeds interest paid after {break_even_month if break_even_month else months} months"
    }


def calculate_affordability_metrics(emi: float, principal: float) -> Dict:
    """Calculate affordability and comparison metrics"""
    
    # Recommended income (EMI should be max 40% of monthly income)
    recommended_monthly_income = emi / 0.4
    recommended_annual_income = recommended_monthly_income * 12
    
    # Debt-to-income ratios
    return {
        'recommended_monthly_income': round(recommended_monthly_income, 2),
        'recommended_annual_income': round(recommended_annual_income, 2),
        'emi_to_income_ratio': '40%',
        'note': 'EMI should ideally not exceed 40% of monthly income',
        'loan_to_value_info': 'For home loans, LTV ratio typically ranges from 75-90%'
    }
