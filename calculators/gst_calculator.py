from typing import Dict

def calculate_gst(
    amount: float,
    gst_rate: float,
    mode: str = 'add'
) -> Dict:
    """
    Calculate GST. 
    mode options: 'add' (exclusive to inclusive), 'remove' (inclusive to exclusive)
    """
    if mode.lower() == 'remove':
        net_amount = amount / (1 + (gst_rate / 100.0))
        gst_amount = amount - net_amount
        gross_amount = amount
    else:
        net_amount = amount
        gst_amount = amount * (gst_rate / 100.0)
        gross_amount = amount + gst_amount
        
    cgst = gst_amount / 2
    sgst = gst_amount / 2
    
    return {
        'mode': mode.lower(),
        'gst_rate': round(gst_rate, 2),
        'net_amount': round(net_amount, 2),
        'gst_amount': round(gst_amount, 2),
        'cgst': round(cgst, 2),
        'sgst': round(sgst, 2),
        'gross_amount': round(gross_amount, 2)
    }
