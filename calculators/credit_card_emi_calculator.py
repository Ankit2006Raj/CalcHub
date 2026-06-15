from typing import Dict, List, Optional
from decimal import Decimal, ROUND_HALF_UP

def calculate_cc_emi(
    amount: float,
    annual_rate: float,
    months: int,
    processing_fee_percent: float = 1.0,
    gst_rate: float = 18.0
) -> Dict:
    """
    Calculate Credit Card EMI including processing fees and GST on interest.
    """
    principal = Decimal(str(amount))
    rate = Decimal(str(annual_rate))
    tenure = months
    proc_fee_pct = Decimal(str(processing_fee_percent))
    gst_pct = Decimal(str(gst_rate))

    monthly_rate = rate / (Decimal('12') * Decimal('100'))
    
    # Processing fee + GST on it
    processing_fee = principal * (proc_fee_pct / Decimal('100'))
    gst_on_pf = processing_fee * (gst_pct / Decimal('100'))
    total_pf = processing_fee + gst_on_pf

    # Calculate base EMI (without GST on interest)
    if monthly_rate == 0:
        base_emi = principal / Decimal(str(tenure))
    else:
        base_emi = (principal * monthly_rate * (1 + monthly_rate) ** tenure) / \
                   ((1 + monthly_rate) ** tenure - 1)

    base_emi = base_emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    schedule = []
    balance = principal
    total_interest = Decimal('0')
    total_gst_on_interest = Decimal('0')
    total_amount_payable = total_pf

    for month in range(1, tenure + 1):
        interest = balance * monthly_rate
        gst_on_interest = interest * (gst_pct / Decimal('100'))
        
        principal_payment = base_emi - interest
        actual_emi = base_emi + gst_on_interest
        
        balance -= principal_payment
        
        schedule.append({
            'month': month,
            'principal': float(principal_payment.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'interest': float(interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'gst_on_interest': float(gst_on_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'total_emi': float(actual_emi.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
            'balance': float(max(balance, Decimal('0')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP))
        })
        
        total_interest += interest
        total_gst_on_interest += gst_on_interest
        total_amount_payable += actual_emi

    # Comparison (Upfront vs EMI)
    # Upfront is just principal.
    extra_cost = total_amount_payable - principal

    return {
        'principal': float(principal),
        'processing_fee': float(processing_fee.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'gst_on_pf': float(gst_on_pf.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'total_pf': float(total_pf.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'base_emi': float(base_emi),
        'total_interest': float(total_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'total_gst_on_interest': float(total_gst_on_interest.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'total_amount_payable': float(total_amount_payable.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'extra_cost_of_emi': float(extra_cost.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)),
        'amortization_schedule': schedule
    }
