"""Select the CloneEstimator."""
import logging
logger = logging.getLogger('chimaera.clones_estimators')
from .clustering.hdbscan import Hdbscan


def get_clones_estimator(method, *args, **kwargs):
    clustering_method = None
    if method == 'hdbscan':
        clustering_method = Hdbscan(*args, **kwargs)
    else:
        raise RuntimeError('method={} not supported!'.format(method))
    return clustering_method
