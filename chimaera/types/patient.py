"""Patient object."""
import pandas as pd
import numpy as np
import traceback
from .samples import default_sample_purity
from .samples import sample_feature_parsers, sample_features


class Patient(object):

    def __init__(self, mutations_df, samples_info_df=None, purity=None):
        # mutations
        self.mutations_df = mutations_df

        # reading samples info
        if samples_info_df is not None:
            self.samples_info_df = samples_info_df
        else:
            try:
                self.samples_info_df = get_samples_info(mutations_df)
            except Exception:
                traceback.print_exc()
                raise Exception('Impossible to get samples information.')

        self.number_of_samples = self.samples_info_df.shape[0]

        if purity is not None:
            try:
                self.samples_info_df['purity'] = pd.Series(purity)
            except Exception:
                traceback.print_exc()
                raise Exception('Impossible to use provided purity.')
        elif not ('purity' in self.samples_info_df):
            self.samples_info_df['purity'] = np.repeat(
                default_sample_purity,
                self.number_of_samples
            )

    def get_mutations_subset(self, mutations):
        return Patient(self.mutations_df.loc[mutations], self.samples_info_df)

    def get_samples_subset(self, samples):
        selected_samples_info_df = self.samples_info_df.loc[samples]
        selected_columns = selected_samples_info_df[
            ['alt', 'cn', 'ref', 'vaf']
        ].values.flatten().tolist()
        return Patient(
            self.mutations_df[selected_columns],
            selected_samples_info_df)


def get_samples_info(mutations_df):
    return pd.DataFrame({
        sample_feature: pd.Series({
            sample_feature_parsers[sample_feature].get_sample(column): column
            for column in mutations_df.columns
            if sample_feature_parsers[sample_feature].search(column)
        })
        for sample_feature in sample_features
    })
