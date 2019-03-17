"""Clone optimizer definion and utilities."""
import numpy as np
from abc import ABCMeta, abstractmethod


def get_objective(number_of_mutations, B):
    """Get the objective function."""
    return lambda x: np.linalg.norm(
        np.outer(
            x[:number_of_mutations],
            x[number_of_mutations:]
        ) - B
    )


class CloneOptimizer(object, metaclass=ABCMeta):
    """Clone optimizer class."""

    def __init__(self, clone, estimates, delta_lb=0.0, delta_ub=4.0):
        self.B = (
            clone.mutations_df[clone.samples_info_df['vaf']].values *
            clone.mutations_df[clone.samples_info_df['cn']].values /
            clone.samples_info_df['purity'].values
        )
        self.number_of_mutations = self.B.shape[0]
        self.number_of_biopsies = self.B.shape[1]
        self.mutations = clone.mutations_df.index
        self.samples = estimates.columns
        self._problem_setup(delta_lb, delta_ub)

    def _problem_setup(self, delta_lb, delta_ub):
        number_of_biopsies = self.B.shape[1]
        self.bounds = tuple(
            [(delta_lb, delta_ub) for i in range(self.number_of_mutations)] +
            [(0, 1) for i in range(number_of_biopsies)]
        )

    def optimize(self, **kwargs):
        pass
