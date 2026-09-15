from pyspark.sql.functions import pow, radians, sin, cos, atan2, sqrt

def haversine_distance(lat1, lon1, lat2, lon2):
  """
  Calculate the Haversine distance (in miles) between two geographic coordinates.

  Parameters:
    lat1 (float): Latitude of the first point.
    lon1 (float): Longitude of the first point.
    lat2 (float): Latitude of the second point.
    lon2 (float): Longitude of the second point.

  Returns:
    float: Distance between the two points in miles.
  """
  EARTH_RADIUS = 3958.8

  lat1_rad = radians(lat1)
  lon1_rad = radians(lon1)
  lat2_rad = radians(lat2)
  lon2_rad = radians(lon2)

  dlat = lat2_rad - lat1_rad
  dlon = lon2_rad - lon1_rad

  a = pow(sin(dlat / 2), 2) + cos(lat1_rad) * cos(lat2_rad) * pow(
      sin(dlon / 2), 2
  )
  c = 2 * atan2(sqrt(a), sqrt(1 - a))

  return EARTH_RADIUS * c