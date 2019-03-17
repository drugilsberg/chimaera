"""Random clone optimizer."""
from ..types.clone import Clone
from .clone_optimizer import CloneOptimizer, get_objective
from ..utils import merge_dicts
import pandas as pd
import numpy as np
from scipy.optimize import minimize
from joblib import Parallel, delayed


def analyze_clone(
    patient, clone_id,
    clones_mutations, estimates,
    delta_lb=0.0, delta_ub=4.0,
    **kwargs
):
    """Analyze clones using Random."""
    mutations = clones_mutations[clones_mutations == clone_id].index
    clone = patient.get_mutations_subset(mutations)
    clone_estimates = estimates.loc[mutations]
    optimizer = Random(
        clone, clone_estimates,
        delta_lb=delta_lb, delta_ub=delta_ub
    )
    return Clone(clone_id, *optimizer.optimize(**kwargs))


default_parameters = {
    'n_init': 10,
    'method': 'SLSQP',
    'n_jobs': -1
}


def get_initial_values(number_of_biopsies, number_of_mutations):
    """Sample values for the initial solution."""
    return tuple(
        np.concatenate(
            [
                np.repeat(1., number_of_mutations),
                np.random.uniform(0., 1., number_of_biopsies)
            ])
    )


def _clone_minimize(
    number_of_mutations, B,
    number_of_biopsies, bounds, method
):
    fun = get_objective(number_of_mutations, B)
    x0 = get_initial_values(number_of_biopsies, number_of_mutations)
    return minimize(
        fun=fun,
        x0=x0,
        bounds=bounds,
        method=method,
        tol=1e-12,
        options={'maxiter': 1000, 'disp': False, 'eps': 1e-12}
    )


class Random(CloneOptimizer):
    """Random clone optimization class."""

    def __init__(self, clone, estimates, **kwargs):
        """Build a Random clone optimizer."""
        super(Random, self).__init__(clone, estimates, **kwargs)

    def optimize(self, **kwargs):
        """Optimize clones."""
        parameters = merge_dicts(default_parameters, kwargs)
        runs = Parallel(n_jobs=parameters['n_jobs'])(
            delayed(_clone_minimize)
            (
                self.number_of_mutations, self.B,
                self.number_of_biopsies, self.bounds,
                parameters['method']
            )
            for i in range(parameters['n_init'])
        )
        best_run = np.argmin(map(lambda run: run['fun'], runs))
        solution = runs[best_run]['x']
        return (
            pd.Series(
                solution[:self.number_of_mutations], index=self.mutations
            ),
            pd.Series(
                solution[self.number_of_mutations:], index=self.samples
            )
        )
