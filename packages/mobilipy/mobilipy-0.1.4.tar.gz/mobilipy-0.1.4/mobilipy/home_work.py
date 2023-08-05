from numba import njit
import numpy as np
from haversine import haversine, Unit
import pandas as pd
pd.options.mode.chained_assignment = None

@njit
def _assign_cell(latitude, longitude, cell_size=0.2) -> int:
    """
    Assigns a cell_number based on the cantor pairing function and discretization into 200m * 200m cells.
    Arguments:
        latitude (float): latitude in degrees.
        longitude (float): longitude in degrees.
        cell_size (float, optional): cell side length in km. Defaults to 0.2.

    Returns:
        cell_number (int): Cell number based on the cantor pair function.
    """

    km_east = 111.320 * np.cos(np.deg2rad(latitude)) * longitude
    km_north = 110.574 * latitude
    x_index = km_east // cell_size
    y_index = km_north // cell_size
    cell_number = (1/2)*(y_index + x_index)*(y_index + x_index + 1) + x_index
    return cell_number


def detect_home_work(legs, waypoints) -> tuple(tuple(float, float), tuple(float, float)):
    """Detects home and work locations, tags them with 'Home' or 'Work' in the df

    Args:
        legs (pandas.DataFrame): DataFrame with legs
        waypoints (pandas.DataFrame): the raw waypoints DataFrame 
    
    Returns:
        tuple[tuple[float, float], tuple[float, float]]: tuple of user's home and work locations as [latitude, longitude]
    """
    
    if legs.shape[0] != 0 and waypoints.shape[0] != 0:
        waypoints_ = waypoints[['tracked_at', 'latitude', 'longitude', 'user_id']]
        waypoints_["cell_number"] = _assign_cell(waypoints_.latitude.values, waypoints_.longitude.values)
        waypoints_["cell_number"] = waypoints_["cell_number"].astype('int64')

        # Waypoints_workdates is waypoints filtered to only contain datapoints from workdays between 7:00 and 19:00
        waypoints_workdates = waypoints_.copy()
        waypoints_workdates['hour'] = waypoints_workdates.tracked_at.dt.hour
        waypoints_workdates['weekday'] = waypoints_workdates.tracked_at.dt.weekday
        waypoints_workdates = waypoints_workdates[(waypoints_workdates.hour >= 7) & (waypoints_workdates.hour <= 19) & (waypoints_workdates.weekday < 5)]
        waypoints_workdates = waypoints_workdates.drop(columns=['hour', 'weekday'])

        # Most_visited_cells_workdates finds the most visited cells during workdays
        most_visited_cells_workdates = waypoints_workdates.drop(columns=["tracked_at", "user_id"])
        most_visited_cells_workdates = most_visited_cells_workdates.groupby("cell_number").agg(["count", "mean"])
        most_visited_cells_workdates.columns = most_visited_cells_workdates.columns.droplevel()
        most_visited_cells_workdates.columns = ["count_lat", "mean_lat", "count_lon", "mean_lon"]
        most_visited_cells_workdates = most_visited_cells_workdates.drop(columns="count_lat").reset_index()
        most_visited_cells_workdates = most_visited_cells_workdates.rename(columns={"mean_lat": "latitude", "mean_lon": "longitude"}).sort_values(by="count_lon", ascending=False)

        # Most_visited_cells finds the most visited cells overall
        most_visited_cells = waypoints_.drop(columns=["tracked_at", "user_id"])
        most_visited_cells = most_visited_cells.groupby("cell_number").agg(["count", "mean"])
        most_visited_cells.columns = most_visited_cells.columns.droplevel()
        most_visited_cells.columns = ["count_lat", "mean_lat", "count_lon", "mean_lon"]
        most_visited_cells = most_visited_cells.drop(columns="count_lat").reset_index()
        most_visited_cells = most_visited_cells.rename(columns={"mean_lat": "latitude", "mean_lon": "longitude"}).sort_values(by="count_lon", ascending=False)

        home_user_cell_number = most_visited_cells.iloc[0].cell_number
        home_user = (most_visited_cells.iloc[0]['latitude'], most_visited_cells.iloc[0]['longitude'])
        
        first_workdates_cell_number = most_visited_cells_workdates.iloc[0].cell_number
        first_workdates = (most_visited_cells_workdates.iloc[0]['latitude'], most_visited_cells_workdates.iloc[0]['longitude'])
        
        second_workdates = (most_visited_cells_workdates.iloc[1]['latitude'], most_visited_cells_workdates.iloc[1]['longitude'])
        
        work_user = first_workdates if first_workdates_cell_number != home_user_cell_number else second_workdates

        user_activities = legs[legs.type == 'Stay']

        for index, row in user_activities.iterrows():
            _find_centroid(index, legs, home_user, work_user)
        return home_user, work_user


# Tags legs as home or work if they're close enough to either
def _find_centroid(leg_index, legs, home_user, work_user):
    """
    Tags legs as home or work if they're close enough to either
    Args:
        leg_index (int): index of the leg to be processed
        legs (pandas.DataFrame): DataFrame with legs
        home_user (tuple[latitude, longitude]): user's home location
        work_user (tuple[latitude, longitude]): user's work location
    """
    centroid = (legs.geometry[leg_index][0][0], legs.geometry[leg_index][0][1])
    d_home = haversine(home_user, centroid)
    d_work = haversine(work_user, centroid)
    if d_home < 0.03:
        legs.loc[leg_index, 'purpose'] = 'Home'
    if d_work < 0.03:
        legs.loc[leg_index, 'purpose'] = 'Work'