"""Tests georelate.data"""
from georelate.data import load_poll_aid_data


def test_load_poll_aid_data():
    """Tests load_poll_aid_data"""

    poll_df, aid_df = load_poll_aid_data()

    print(poll_df)
    print(aid_df)
