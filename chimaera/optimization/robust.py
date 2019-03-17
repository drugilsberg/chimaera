"""Robust clone optimizer."""
from ..types.clone import Clone
from .clone_optimizer import CloneOptimizer, get_objective
from ..utils import merge_dicts
import pandas as pd
import numpy as np
from scipy.optimize import minimize


def robust_analyze_clone(
    patient, clone_id,
    clones_mutations, estimates,
    delta_lb=0.0, delta_ub=4.0,
    **kwargs
):
    """Analyze clones using Robust."""
    mutations_selected = clones_mutations == clone_id
    mutations = clones_mutations[mutations_selected].index
    clone = patient.get_mutations_subset(mutations)
    clone_estimates = estimates.loc[mutations]
    optimizer = Robust(
        clone, clone_estimates,
        delta_lb=delta_lb, delta_ub=delta_ub
    )
    initial_frequencies = clone_estimates.median()
    inital_deltas = clone.mutations_df.loc[mutations][
        patient.samples_info_df['cn']
    ].median(axis=1)
    return Clone(
        clone_id,
        *optimizer.optimize(inital_deltas, initial_frequencies, **kwargs)
    )


default_parameters = {
    'method': 'SLSQP'
}


def get_x0(initial_deltas, initial_frequencies):
    """Get initial solution."""
    return tuple(
        np.concatenate(
            [
                initial_deltas.values,
                initial_frequencies.values
            ])
    )


def _clone_minimize(
    number_of_mutations, B,
    number_of_biopsies, bounds, method, x0
):
    fun = get_objective(number_of_mutations, B)
    return minimize(
        fun=fun,
        x0=x0,
        bounds=bounds,
        method=method,
        tol=1e-12,
        options={'maxiter': 1000, 'disp': False, 'eps': 1e-12}
    )


class Robust(CloneOptimizer):
    """Robust clone optimization class."""

    def __init__(self, clone, estimates, **kwargs):
        """Build a Robust clone optimizer."""
        super(Robust, self).__init__(clone, estimates, **kwargs)

    def optimize(self, initial_deltas, initial_frequencies, **kwargs):
        """Optimize clones."""
        parameters = merge_dicts(default_parameters, kwargs)

        run = _clone_minimize(
            self.number_of_mutations, self.B,
            self.number_of_biopsies, self.bounds,
            parameters['method'],
            get_x0(initial_deltas, initial_frequencies)
        )
        solution = run['x']
        return (
            pd.Series(
                solution[:self.number_of_mutations], index=self.mutations
            ),
            pd.Series(
                solution[self.number_of_mutations:], index=self.samples
            )
        )
