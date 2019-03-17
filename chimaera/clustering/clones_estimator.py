"""Abstract CloneEstimator."""
from abc import ABCMeta, abstractmethod


class ClonesEstimator(object, metaclass=ABCMeta):

    @abstractmethod
    def estimate(self, mutations_data, **kwargs):
        pass
