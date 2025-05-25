# change_proneness.py
import os
from radon.complexity import cc_visit
from radon.metrics import mi_visit, h_visit
from radon.raw import analyze

def analyze_code(filepath):
    """
    Analyze the uploaded Python file for change-proneness metrics.
    Returns a dictionary with various metrics.
    """
    metrics = {}
    
    # Read file content
    with open(filepath, 'r') as file:
        code = file.read()
    
    # Cyclomatic Complexity
    metrics['cyclomatic_complexity'] = [
        {'name': item.name, 'complexity': item.complexity}
        for item in cc_visit(code)
    ]
    
    # Maintainability Index
    metrics['maintainability_index'] = mi_visit(code, True)
    
    # Halstead Metrics
    metrics['halstead_metrics'] = h_visit(code)
    
    # Raw Metrics
    raw_metrics = analyze(code)
    metrics['raw_metrics'] = {
        'loc': raw_metrics.loc,
        'lloc': raw_metrics.lloc,
        'sloc': raw_metrics.sloc,
        'comments': raw_metrics.comments,
        'multi': raw_metrics.multi,
        'blank': raw_metrics.blank
    }
    
    return metrics
