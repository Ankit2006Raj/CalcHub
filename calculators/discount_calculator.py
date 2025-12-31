"""
Discount Calculator Module
Calculate discounts, sale prices, and savings
"""

from typing import Dict, List


def calculate_discount(
    original_price: float,
    discount_percent: float = None,
    sale_price: float = None,
    discount_amount: float = None
) -> Dict:
    """
    Calculate discount information
    
    Args:
        original_price: Original price before discount
        discount_percent: Discount percentage (optional)
        sale_price: Final sale price (optional)
        discount_amount: Discount amount in currency (optional)
    
    Returns:
        Dictionary with discount calculations
    """
    if discount_percent is not None:
        # Calculate from discount percentage
        discount_amt = original_price * (discount_percent / 100)
        final_price = original_price - discount_amt
        
    elif sale_price is not None:
        # Calculate from sale price
        discount_amt = original_price - sale_price
        discount_percent = (discount_amt / original_price) * 100
        final_price = sale_price
        
    elif discount_amount is not None:
        # Calculate from discount amount
        discount_amt = discount_amount
        final_price = original_price - discount_amt
        discount_percent = (discount_amt / original_price) * 100
    else:
        raise ValueError("Must provide either discount_percent, sale_price, or discount_amount")
    
    savings = discount_amt
    savings_percent = discount_percent
    
    return {
        'original_price': round(original_price, 2),
        'discount_percent': round(discount_percent, 2),
        'discount_amount': round(discount_amt, 2),
        'final_price': round(final_price, 2),
        'you_save': round(savings, 2),
        'savings_percent': round(savings_percent, 2)
    }



def calculate_multiple_discounts(
    original_price: float,
    discounts: List[float]
) -> Dict:
    """
    Calculate multiple successive discounts
    
    Args:
        original_price: Original price
        discounts: List of discount percentages applied successively
    
    Returns:
        Dictionary with final price and breakdown
    """
    current_price = original_price
    breakdown = []
    
    for i, discount in enumerate(discounts, 1):
        discount_amt = current_price * (discount / 100)
        new_price = current_price - discount_amt
        
        breakdown.append({
            'step': i,
            'discount_percent': discount,
            'price_before': round(current_price, 2),
            'discount_amount': round(discount_amt, 2),
            'price_after': round(new_price, 2)
        })
        
        current_price = new_price
    
    total_savings = original_price - current_price
    effective_discount = (total_savings / original_price) * 100
    
    return {
        'original_price': round(original_price, 2),
        'final_price': round(current_price, 2),
        'total_savings': round(total_savings, 2),
        'effective_discount_percent': round(effective_discount, 2),
        'breakdown': breakdown
    }


def calculate_bulk_discount(
    unit_price: float,
    quantity: int,
    bulk_tiers: List[Dict] = None
) -> Dict:
    """
    Calculate bulk purchase discounts
    
    Args:
        unit_price: Price per unit
        quantity: Number of units
        bulk_tiers: List of dicts with 'min_qty' and 'discount_percent'
    
    Returns:
        Dictionary with bulk pricing information
    """
    if bulk_tiers is None:
        bulk_tiers = [
            {'min_qty': 10, 'discount_percent': 5},
            {'min_qty': 50, 'discount_percent': 10},
            {'min_qty': 100, 'discount_percent': 15}
        ]
    
    # Sort tiers by quantity descending
    sorted_tiers = sorted(bulk_tiers, key=lambda x: x['min_qty'], reverse=True)
    
    # Find applicable discount
    applicable_discount = 0
    for tier in sorted_tiers:
        if quantity >= tier['min_qty']:
            applicable_discount = tier['discount_percent']
            break
    
    original_total = unit_price * quantity
    discount_amount = original_total * (applicable_discount / 100)
    final_total = original_total - discount_amount
    final_unit_price = final_total / quantity
    
    return {
        'unit_price': round(unit_price, 2),
        'quantity': quantity,
        'discount_percent': applicable_discount,
        'original_total': round(original_total, 2),
        'discount_amount': round(discount_amount, 2),
        'final_total': round(final_total, 2),
        'final_unit_price': round(final_unit_price, 2),
        'savings_per_unit': round(unit_price - final_unit_price, 2),
        'bulk_tiers': bulk_tiers
    }


def calculate_tax_and_discount(
    original_price: float,
    discount_percent: float,
    tax_percent: float,
    apply_tax_after_discount: bool = True
) -> Dict:
    """
    Calculate price with both discount and tax
    
    Args:
        original_price: Original price
        discount_percent: Discount percentage
        tax_percent: Tax percentage
        apply_tax_after_discount: Whether to apply tax after discount
    
    Returns:
        Dictionary with final price including tax
    """
    discount_amount = original_price * (discount_percent / 100)
    price_after_discount = original_price - discount_amount
    
    if apply_tax_after_discount:
        tax_amount = price_after_discount * (tax_percent / 100)
        final_price = price_after_discount + tax_amount
    else:
        tax_amount = original_price * (tax_percent / 100)
        final_price = original_price + tax_amount - discount_amount
    
    return {
        'original_price': round(original_price, 2),
        'discount_percent': round(discount_percent, 2),
        'discount_amount': round(discount_amount, 2),
        'price_after_discount': round(price_after_discount, 2),
        'tax_percent': round(tax_percent, 2),
        'tax_amount': round(tax_amount, 2),
        'final_price': round(final_price, 2),
        'total_savings': round(discount_amount, 2)
    }
