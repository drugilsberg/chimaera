"""Select the CloneAnalyzer."""
from .optimization.random import analyze_clone
from .optimization.robust import robust_analyze_clone


def get_clone_analyzer(method):
    clone_analyzer = None
    if method == 'random':
        clone_analyzer = analyze_clone
    elif method == 'robust':
        clone_analyzer = robust_analyze_clone
    return clone_analyzer
