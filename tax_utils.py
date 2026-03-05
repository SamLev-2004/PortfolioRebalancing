from typing import List, Dict, Union, Any

def estimate_taxes(trades: List[Dict[str, Any]], tax_bracket_rate: float = 0.40) -> Dict[str, Union[float, Dict[str, Dict[str, float]]]]:
    """
    Estimate Canadian capital gains tax implications of trades.
    
    Args:
        trades: list of trade dicts from calculate_rebalance_trades
        tax_bracket_rate: The user's marginal income tax rate (default 40%)
    
    Returns:
        dict: Total estimated tax liability and breakdown by account
    """
    
    # In Canada, currently 50% of capital gains are taxable
    # We will assume this baseline for the prototype
    inclusion_rate = 0.50
    effective_tax_rate = tax_bracket_rate * inclusion_rate
    
    tax_report: Dict[str, Any] = {
        'total_estimated_tax': 0.0,
        'taxable_gains': 0.0,
        'tax_free_gains': 0.0,
        'account_breakdown': {}
    }
    
    for trade in trades:
        # We only care about SELLs that generated a profit
        if trade['action'] != 'SELL' or trade.get('est_gain', 0) <= 0:
            continue
            
        gain = trade['est_gain']
        account = str(trade.get('account', 'UNKNOWN')).strip().upper()
        
        # Initialize account in report if it doesn't exist
        if account not in tax_report['account_breakdown']:
            tax_report['account_breakdown'][account] = {'gains': 0.0, 'estimated_tax': 0.0}
            
        # Apply Canadian Tax Logic Models
        if account in ['TFSA', 'RRSP', 'FHSA']:
            # Tax-advantaged accounts do not trigger immediate capital gains tax!
            tax_report['tax_free_gains'] += gain
            tax_report['account_breakdown'][account]['gains'] += gain
            
        else:
            # Unregistered / Cash / Margin accounts trigger taxable events
            tax = gain * effective_tax_rate
            
            tax_report['taxable_gains'] += gain
            tax_report['total_estimated_tax'] += tax
            
            tax_report['account_breakdown'][account]['gains'] += gain
            tax_report['account_breakdown'][account]['estimated_tax'] += tax
            
    # Round everything nicely for UI display
    tax_report['total_estimated_tax'] = round(tax_report['total_estimated_tax'], 2)
    tax_report['taxable_gains'] = round(tax_report['taxable_gains'], 2)
    tax_report['tax_free_gains'] = round(tax_report['tax_free_gains'], 2)
    
    for acc in tax_report['account_breakdown']:
        tax_report['account_breakdown'][acc]['gains'] = round(tax_report['account_breakdown'][acc]['gains'], 2)
        tax_report['account_breakdown'][acc]['estimated_tax'] = round(tax_report['account_breakdown'][acc]['estimated_tax'], 2)
        
    return tax_report
