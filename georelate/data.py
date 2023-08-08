"""Allow the user to load example datasets."""

import pandas as pd


def _load_poll_df():
    """Fictitious polling locations.

    Returns:
        pd.DataFrame: Fictitious polling locations.
    """
    return pd.DataFrame(
        [
            {"local_id": 1, "lat": -6.69255, "lon": -39.76566},
            {"local_id": 2, "lat": -4.76871, "lon": -39.61186},
            {"local_id": 3, "lat": -3.28926, "lon": -40.75443},
        ]
    )


def _load_aid_df():
    """Fictitious aid locations.

    Returns:
        pd.DataFrame: Fictitious aid locations.
    """
    return pd.DataFrame(
        [
            {"project_id_aid": "p1", "lat_aid": -6.61616, "long_aid": -39.9799},
            {"project_id_aid": "p2", "lat_aid": -4.76871, "long_aid": -39.77116},
            {"project_id_aid": "p3", "lat_aid": -4.26065, "long_aid": -39.3903},
        ]
    )


def load_poll_aid_data():
    """Loads a fictitious dataset to demonstrate the functionality of the library.
    It contains a table of polling location and a table of aid locations.
    This dataset is inspired by a real one.
    The analysis that georelate assists with is building a design matrix to determine
    whether foreign aid effects vote results at the polling station level.

    Returns:
        tuple[pd.DataFrame, pd.DataFrame]: (Fictitious polling locations, Fictitious aid locations)
    """
    return (_load_poll_df(), _load_aid_df())
