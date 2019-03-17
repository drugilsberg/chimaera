"""Frequency approximation utilities."""


def sample_frequency_estimates(mutations_df, sample_series):
    return 2. * mutations_df[sample_series['vaf']] * \
        mutations_df[sample_series['cn']] / \
        (
        mutations_df[sample_series['cn']] - 2. * (
            1. - sample_series['purity']
        )
    )


def frequency_approximation(patient):
    estimates = patient.samples_info_df.apply(
        lambda sample: sample_frequency_estimates(
            patient.mutations_df, sample
        ),
        axis=1
    ).T
    # correction needed
    estimates[estimates > 1.] = 1
    return estimates
