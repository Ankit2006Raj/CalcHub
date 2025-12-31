"""
Professional Compound Interest Calculator Module
Provides comprehensive investment calculations with detailed projections
"""

from typing import Dict, Union, List, Optional
from decimal import Decimal, ROUND_HALF_UP
import math


class CompoundInterestCalculationError(Exception):
    """Custom exception for compound interest calculation errors"""
    pass


def calculate_compound_interest(
    principal: float,
    rate: float,
    time: int,
    frequency: int,
    monthly_contribution: float = 0,
    contribution_timing: str = "end",
    inflation_rate: float = 0,
    detailed: bool = False
) -> Dict[str, Union[float, int, str, List, Dict]]:
    """
    Calculate comprehensive compound interest with investment analysis
    
    Args:
        principal: Initial principal amount
        rate: Annual interest rate (percentage)
        time: Time period in years
        frequency: Compounding frequency (1=annually, 4=quarterly, 12=monthly, 365=daily)
        monthly_contribution: Optional monthly contribution amount
        contribution_timing: 'start' or 'end' of period
        inflation_rate: Annual inflation rate for real returns
        detailed: If False, returns simple format for backward compatibility
    
    Returns:
        Dictionary containing detailed investment analysis and projections
    
    Raises:
        CompoundInterestCalculationError: If input parameters are invalid
    """
    # Validate inputs
    if principal < 0:
        raise CompoundInterestCalculationError("Principal amount cannot be negative.")
    if rate < 0:
        raise CompoundInterestCalculationError("Interest rate cannot be negative.")
    if time <= 0:
        raise CompoundInterestCalculationError("Time period must be greater than zero.")
    if frequency not in [1, 2, 4, 12, 52, 365]:
        raise CompoundInterestCalculationError("Frequency must be 1, 2, 4, 12, 52, or 365.")
    if monthly_contribution < 0:
        raise CompoundInterestCalculationError("Monthly contribution cannot be negative.")
    if inflation_rate < 0 or inflation_rate > 100:
        raise CompoundInterestCalculationError("Inflation rate must be between 0 and 100.")
    
    # Calculate compound interest
    r = rate / 100
    n = frequency
    t = time
    
    # Future value of principal
    fv_principal = principal * (1 + r / n) ** (n * t)
    
    # Future value of contributions (if any)
    fv_contributions = 0
    total_contributions = 0
    
    if monthly_contribution > 0:
        # Convert monthly to per-period contribution
        periods_per_year = n
        contribution_per_period = monthly_contribution * 12 / periods_per_year
        total_periods = n * t
        
        # Future value of annuity formula
        if contribution_timing.lower() == "start":
            # Annuity due
            fv_contributions = contribution_per_period * (((1 + r/n) ** total_periods - 1) / (r/n)) * (1 + r/n)
        else:
            # Ordinary annuity
            fv_contributions = contribution_per_period * (((1 + r/n) ** total_periods - 1) / (r/n))
        
        total_contributions = monthly_contribution * 12 * t
    
    total_amount = fv_principal + fv_contributions
    compound_interest = total_amount - principal - total_contributions
    
    # Generate detailed breakdown
    breakdown = generate_breakdown(principal, rate, time, frequency, monthly_contribution, contribution_timing)
    
    # Calculate effective annual rate
    effective_rate = ((1 + r / n) ** n - 1) * 100
    
    # Calculate real returns (adjusted for inflation)
    real_returns = calculate_real_returns(total_amount, principal + total_contributions, inflation_rate, time)
    
    # Calculate investment metrics
    metrics = calculate_investment_metrics(
        principal, total_contributions, compound_interest, total_amount, time, rate
    )
    
    # Backward compatibility: return simple format if detailed=False
    if not detailed:
        return {
            'principal': principal,
            'rate': rate,
            'time': time,
            'frequency': frequency,
            'compound_interest': round(compound_interest, 2),
            'total_amount': round(total_amount, 2),
            'breakdown': breakdown[:time]  # Only yearly breakdown for compatibility
        }
    
    # Calculate comparison scenarios
    comparison = compare_frequencies(principal, rate, time, monthly_contribution)
    
    # Generate recommendations
    recommendations = generate_investment_recommendations(
        principal, rate, time, monthly_contribution, compound_interest
    )
    
    return {
        'investment_summary': {
            'initial_principal': round(principal, 2),
            'total_contributions': round(total_contributions, 2),
            'total_invested': round(principal + total_contributions, 2),
            'compound_interest_earned': round(compound_interest, 2),
            'final_amount': round(total_amount, 2),
            'total_return_percentage': round((compound_interest / (principal + total_contributions)) * 100, 2) if (principal + total_contributions) > 0 else 0
        },
        'interest_details': {
            'annual_rate': rate,
            'effective_annual_rate': round(effective_rate, 4),
            'compounding_frequency': get_frequency_name(frequency),
            'compounds_per_year': frequency,
            'total_compounds': frequency * time
        },
        'contribution_details': {
            'monthly_contribution': monthly_contribution,
            'contribution_timing': contribution_timing,
            'total_contributions': round(total_contributions, 2),
            'contribution_growth': round(fv_contributions - total_contributions, 2) if monthly_contribution > 0 else 0
        },
        'time_analysis': {
            'investment_period_years': time,
            'investment_period_months': time * 12,
            'doubling_time_years': round(calculate_doubling_time(rate, frequency), 2),
            'rule_of_72_estimate': round(72 / rate, 2) if rate > 0 else None
        },
        'breakdown': breakdown,
        'real_returns': real_returns,
        'investment_metrics': metrics,
        'frequency_comparison': comparison,
        'recommendations': recommendations,
        'notes': [
            'Compound interest is calculated on principal + accumulated interest',
            'More frequent compounding results in higher returns',
            'Regular contributions significantly boost long-term growth',
            'Past performance does not guarantee future results',
            'Consider taxes and fees in real-world scenarios'
        ]
    }


def generate_breakdown(
    principal: float,
    rate: float,
    time: int,
    frequency: int,
    monthly_contribution: float,
    contribution_timing: str
) -> List[Dict]:
    """Generate year-by-year breakdown of investment growth"""
    breakdown = []
    r = rate / 100
    n = frequency
    
    current_balance = principal
    total_contributed = principal
    
    for year in range(1, time + 1):
        year_start_balance = current_balance
        year_contributions = monthly_contribution * 12
        
        # Calculate growth for this year
        if monthly_contribution > 0:
            # Add monthly contributions throughout the year
            for month in range(12):
                if contribution_timing.lower() == "start":
                    current_balance += monthly_contribution
                    total_contributed += monthly_contribution
                
                # Apply interest for the month
                periods_in_month = frequency / 12
                current_balance *= (1 + r / n) ** periods_in_month
                
                if contribution_timing.lower() == "end":
                    current_balance += monthly_contribution
                    total_contributed += monthly_contribution
        else:
            # No contributions, just compound the balance
            current_balance *= (1 + r / n) ** n
        
        year_interest = current_balance - year_start_balance - year_contributions
        
        breakdown.append({
            'year': year,
            'starting_balance': round(year_start_balance, 2),
            'contributions': round(year_contributions, 2),
            'interest_earned': round(year_interest, 2),
            'ending_balance': round(current_balance, 2),
            'total_contributed': round(total_contributed, 2),
            'total_interest': round(current_balance - total_contributed, 2)
        })
    
    return breakdown


def get_frequency_name(frequency: int) -> str:
    """Get human-readable frequency name"""
    frequency_names = {
        1: 'Annually',
        2: 'Semi-annually',
        4: 'Quarterly',
        12: 'Monthly',
        52: 'Weekly',
        365: 'Daily'
    }
    return frequency_names.get(frequency, f'{frequency} times per year')


def calculate_doubling_time(rate: float, frequency: int) -> float:
    """Calculate time for investment to double"""
    if rate <= 0:
        return float('inf')
    r = rate / 100
    n = frequency
    return math.log(2) / (n * math.log(1 + r / n))


def calculate_real_returns(
    final_amount: float,
    total_invested: float,
    inflation_rate: float,
    years: int
) -> Dict:
    """Calculate inflation-adjusted returns"""
    if inflation_rate == 0:
        return {
            'note': 'No inflation rate provided',
            'nominal_return': round(final_amount - total_invested, 2)
        }
    
    # Adjust for inflation
    inflation_multiplier = (1 + inflation_rate / 100) ** years
    real_value = final_amount / inflation_multiplier
    real_gain = real_value - total_invested
    
    return {
        'nominal_final_amount': round(final_amount, 2),
        'inflation_rate': inflation_rate,
        'inflation_adjusted_value': round(real_value, 2),
        'purchasing_power_loss': round(final_amount - real_value, 2),
        'real_gain': round(real_gain, 2),
        'real_return_percentage': round((real_gain / total_invested) * 100, 2) if total_invested > 0 else 0
    }


def calculate_investment_metrics(
    principal: float,
    contributions: float,
    interest: float,
    final_amount: float,
    years: int,
    rate: float
) -> Dict:
    """Calculate various investment performance metrics"""
    total_invested = principal + contributions
    
    # ROI (Return on Investment)
    roi = (interest / total_invested) * 100 if total_invested > 0 else 0
    
    # CAGR (Compound Annual Growth Rate)
    if total_invested > 0 and years > 0:
        cagr = ((final_amount / total_invested) ** (1 / years) - 1) * 100
    else:
        cagr = 0
    
    # Average annual return
    avg_annual_return = interest / years if years > 0 else 0
    
    return {
        'roi_percentage': round(roi, 2),
        'cagr_percentage': round(cagr, 2),
        'average_annual_return': round(avg_annual_return, 2),
        'interest_to_principal_ratio': round(interest / principal, 2) if principal > 0 else 0,
        'final_to_initial_ratio': round(final_amount / total_invested, 2) if total_invested > 0 else 0
    }


def compare_frequencies(
    principal: float,
    rate: float,
    time: int,
    monthly_contribution: float
) -> Dict:
    """Compare returns across different compounding frequencies"""
    frequencies = {
        'annually': 1,
        'semi_annually': 2,
        'quarterly': 4,
        'monthly': 12,
        'daily': 365
    }
    
    comparison = {}
    for name, freq in frequencies.items():
        r = rate / 100
        n = freq
        t = time
        
        # Principal growth
        fv = principal * (1 + r / n) ** (n * t)
        
        # Add contributions if any
        if monthly_contribution > 0:
            contribution_per_period = monthly_contribution * 12 / n
            total_periods = n * t
            fv += contribution_per_period * (((1 + r/n) ** total_periods - 1) / (r/n))
        
        comparison[name] = {
            'frequency': freq,
            'final_amount': round(fv, 2),
            'interest_earned': round(fv - principal - (monthly_contribution * 12 * time), 2)
        }
    
    return comparison


def generate_investment_recommendations(
    principal: float,
    rate: float,
    time: int,
    monthly_contribution: float,
    interest_earned: float
) -> List[str]:
    """Generate personalized investment recommendations"""
    recommendations = []
    
    if monthly_contribution == 0:
        recommendations.append('Consider adding regular monthly contributions to accelerate growth')
    
    if rate < 5:
        recommendations.append('Low interest rate - consider diversifying into higher-yield investments')
    elif rate > 15:
        recommendations.append('High return rate - ensure you understand the associated risks')
    
    if time < 5:
        recommendations.append('Short investment horizon - consider extending for better compound growth')
    elif time >= 20:
        recommendations.append('Long investment horizon - excellent for maximizing compound interest')
    
    if principal < 10000 and monthly_contribution > 0:
        recommendations.append('Regular contributions are key - you\'re building wealth systematically')
    
    recommendations.extend([
        'Start investing early to maximize compound interest benefits',
        'Reinvest dividends and interest for exponential growth',
        'Review and rebalance your portfolio annually',
        'Consider tax-advantaged accounts for better returns',
        'Diversify across different asset classes to manage risk'
    ])
    
    return recommendations
