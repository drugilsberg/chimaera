"""Definition of chimaera pipelines."""
from .io import read_patient
from .frequency_approximation import frequency_approximation
from .clones_estimators import get_clones_estimator
from .clones_analyzers import get_clone_analyzer
from .types.clone import analyze_clones
from .types.cancer import Cancer
import logging


def chimaera(
    input_file, sep, clones_estimator_name, clone_analyzer_name,
    delta_lb=0.0, delta_ub=4.0
):
    """Run generic chimaera pipeline."""
    logger = logging.getLogger('chimaera_{}'.format(clones_estimator_name))
    logger.info('Reading patient data file {}.'.format(input_file))
    patient = read_patient(
        input_file, sep=sep, index_col=0
    )
    logger.info('Approximating frequencies.')
    estimates = frequency_approximation(patient)
    logger.info(
        'Estimating clones using {}.'.format(clones_estimator_name)
    )
    clones_estimator = get_clones_estimator(clones_estimator_name)
    clones_mutations = clones_estimator.estimate(estimates)
    logger.info('Optimizing clones using.'.format(clone_analyzer_name))
    clone_analyzer = get_clone_analyzer(clone_analyzer_name)
    clones = analyze_clones(
        clone_analyzer, patient, clones_mutations, estimates,
        delta_lb=delta_lb, delta_ub=delta_ub
    )
    cancer = Cancer(clones)
    return {
        'cancer_df': cancer.to_df(),
        'frequency_approximation_df': estimates,
        'mutations_df': patient.mutations_df,
        'samples_info_df': patient.samples_info_df
    }


def chimaera_hdbscan(
    input_file, sep, min_clone_size, clone_analyzer_name,
    delta_lb=0.0, delta_ub=4.0
):
    """Run chimaera hdbscan pipeline."""
    logger = logging.getLogger('chimaera_hdbscan')
    logger.info('Reading patient data file {}.'.format(input_file))
    patient = read_patient(
        input_file, sep=sep, index_col=0
    )
    logger.info('Approximating frequencies.')
    estimates = frequency_approximation(patient)
    logger.info(
        'Estimating clones using hdbscan.'
    )
    clones_estimator = get_clones_estimator('hdbscan')
    clones_mutations = clones_estimator.estimate(
        estimates, min_cluster_size=min_clone_size
    )
    logger.info('Optimizing clones using.'.format(clone_analyzer_name))
    clone_analyzer = get_clone_analyzer(clone_analyzer_name)
    clones = analyze_clones(
        clone_analyzer, patient, clones_mutations, estimates,
        delta_lb=delta_lb, delta_ub=delta_ub
    )
    cancer = Cancer(clones)
    return {
        'cancer_df': cancer.to_df(),
        'frequency_approximation_df': estimates,
        'mutations_df': patient.mutations_df,
        'samples_info_df': patient.samples_info_df
    }
