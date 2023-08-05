# Mobilipy
**Mobilipy** is a mobility analysis package that lets you identify complete trip information (meaning segmentation into trips and activities, mode detection as well as home and work location detection) from raw GPS data. It also enables working with GTFS data. IN addition to that, It proposes two ways to make the data more private.  
  
Below is an example usage of the pipeline:

## Preparation
```python
from sdscmob import plot, preparation, waypointsdataframe, segmentation, mode_detection, legs, gtfs_helper, home_work, privacy  
w_df = waypointsdataframe.WaypointsDataFrame(data)  
df_prepared = preparation.prepare(w_df)
```
## Segmentation
```python
route_clusters_detected = segmentation.segment(df_prepared)
```  
## Mode detection
```python
route_clusters_detected = mode_detection.mode_detection(route_clusters_detected)
```  
## Legs
```python
legs_user = legs.get_user_legs(route_clusters_detected, user_id)
```  
## Home and work detection
```python
home_location, work_location = home_work.detect_home_work(legs_user, df_prepared)
```
## Privacy
```python
obfuscated_df, shifted_home, shifted_work = privacy.obfuscate(w_df, [home, work])
aggregated_data = privacy.aggregate(w_df)
```  
## GTFS
```
gtfs_helper.GTFS_Helper(directory='./gtfs/')
```  