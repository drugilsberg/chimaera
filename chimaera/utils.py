"""Generic utilities."""
def merge_dicts(*dicts):
    merged = {}
    for dictionary in dicts:
        merged.update(dictionary)
    return merged


def drop_df_columns(df, *names):
    for name in names:
        try:
            df = df.drop(name, axis=1)
        except ValueError:
            pass
    return df
