"""Sample parsing utilities."""
import re

default_sample_purity = 0.95
sample_features = ['vaf', 'cn', 'ref', 'alt']


class SampleFeatureParser(object):

    def __init__(self, regex):
        self.regex = regex

    def search(self, sample_feature):
        return self.regex.search(sample_feature)

    def get_sample(self, sample_feature):
        search_result = self.regex.search(sample_feature)
        sample = ''
        if search_result:
            span = search_result.span()
            sample = sample_feature[:span[0]] + sample_feature[span[1]:]
        return sample


sample_feature_parsers = {
    pattern: SampleFeatureParser(re.compile('{}'.format(pattern), re.I))
    for pattern in sample_features
}
