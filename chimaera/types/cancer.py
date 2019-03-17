"""Cancer object."""
import pandas as pd


class Cancer(object):

    def __init__(self, clones):
        self.clones = {
            clone.clone_id: clone
            for clone in clones
        }

    def get_clone(self, clone_id):
        return self.clones[clone_id]

    def to_df(self):
        if len(self.clones):
            return pd.concat(
                clone.to_df()
                for _, clone in self.clones.items()
            )
        return None
