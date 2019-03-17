"""I/O utilities."""
import pandas as pd
from .types.patient import Patient


def read_patient(filename, purity=None, *args, **kwargs):
    mutations = pd.read_csv(filename, *args, **kwargs).fillna(0.0)
    mutations = mutations.loc[mutations.index.dropna()]
    return Patient(mutations, purity=purity)
