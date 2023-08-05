from sdscmob import home_work
from sdscmob import legs
from sdscmob import mode_detection
from sdscmob import preparation
from sdscmob import segmentation

import pandas as pd

def analyse(df, user_id) -> pd.DataFrame:
    """Returns complete trip information from a raw GPS waypoints DataFrame. Segments the data into trips, detects the mode of transport and tags the home and work locations.

    Args:
        df (pandas.DataFrame): waypoints DataFrame
        user_id (str): user's ID

    Returns:
        pandas.DataFrame: DataFrame with selected user's legs
    """
    df_prepared = preparation.prepare(df)
    route_clusters_detected = segmentation.segment(df_prepared)
    route_clusters_detected = mode_detection.mode_detection(route_clusters_detected)
    legs_user = legs.get_user_legs(route_clusters_detected, user_id)
    home_work.detect_home_work(legs_user, df_prepared)
        
    return legs_user