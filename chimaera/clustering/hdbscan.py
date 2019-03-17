"""CloneEstimator based on hdbscan."""
from .clones_estimator import ClonesEstimator
from ..utils import merge_dicts
import pandas as pd
import hdbscan
import logging
from scipy.spatial.distance import pdist, squareform


logger = logging.getLogger('chimaera.clustering.hdbscan')


default_parameters = {
    'min_cluster_size': 5
}


class Hdbscan(ClonesEstimator):
    def __init__(self):
        pass

    def estimate(self, mutations_data, **kwargs):
        try:
            precomputed = squareform(
                pdist(mutations_data, 'cityblock') / mutations_data.shape[1]
            )
        except BaseException:
            logger.exception(
                'Problem with mutations_data: {}'.format(mutations_data)
            )
            raise RuntimeError('Problem in computing distances for hdbscan.')
        kwargs.pop('metric', None)
        model = hdbscan.HDBSCAN(
            metric='precomputed',
            **merge_dicts(default_parameters, kwargs)
        )
        model.fit(precomputed)
        return pd.Series(model.labels_ + 1, index=mutations_data.index)
