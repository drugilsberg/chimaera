"""Clones definition and utilities."""
import pandas as pd
import numpy as np


def analyze_clones(
    clone_analyzer, patient, clones_mutations, estimates,
    delta_lb=0.0, delta_ub=4.0,
    **kwargs
):
    """Helper function to run clones analysis."""
    return [
        clone_analyzer(
            patient, clone_id, clones_mutations, estimates,
            delta_lb=delta_lb, delta_ub=delta_ub,
            **kwargs
        )
        for clone_id in range(1, max(clones_mutations) + 1)
    ]


class Clone(object):
    """Clone class definition."""

    def __init__(self, clone_id, deltas, frequencies):
        """Build a Clone."""
        self.clone_id = clone_id
        self.deltas = deltas
        self.frequencies = frequencies

    def __str__(self):
        """Stringify a Clone."""
        return '\n'.join([
            'Clone: {}'.format(self.clone_id),
            'Frequencies:\n{}'.format(self.frequencies),
            'Mutated Allele Copy Numbers:\n{}'.format(self.deltas)
        ])

    def to_df(self):
        """Clone to a pandas.DataFrame."""
        return clone_to_df(self)


def clone_to_df(clone):
    """Convert a clone to a pandas.DataFrame."""
    number_of_mutations = clone.deltas.shape[0]
    clone_stats = pd.DataFrame(
        np.stack([clone.frequencies for _ in range(number_of_mutations)]),
        columns=clone.frequencies.index,
        index=clone.deltas.index
    )
    clone_stats['alt_cn'] = clone.deltas
    clone_stats['clone_id'] = clone.clone_id
    return clone_stats
