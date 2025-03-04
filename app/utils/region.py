import mpu

class Region:
  """ Utility class which holds the available weather regions and their locations.
      Also provides functionality to find the closest region to a given point
  """
  
  """ The available regions. Uncomment as necessary """
  locations = {
    "auckland": (-36.8406,	174.7400),
    "wellington": (-41.2889,	174.7772),
    # "kaitaia": (-35.1125, 173.2628),
    # "whangarei": (-35.7250, 174.3236),
    # "tauranga": (-37.6833, 176.1667),
    # "hamilton": (-37.7833, 175.2833),
    # "rotorua": (-38.1378, 176.2514),
    # "gisborne": (-38.6625,	178.0178),
    # "taupo": (-38.6875,	176.0694),
    # "napier": (-39.4903,	176.9178),
    # "new-plymouth": (-39.0578, 174.0742),
    # "palmerston-north": (-40.3550, 175.6117),
    # "masterton": (-40.97, 175.65),
    # "blenheim": (-41.5140,	173.9600),
    # "nelson": (-41.2708,	173.2839),
    # "westport": (-41.7581,	171.6022),
    # "franz-josef": (-43.388056, 170.181944),
    # "christchurch": (-43.5310,	172.6365),
    # "timaru": (-44.3931,	171.2508),
    # "queenstown": (-45.031111, 168.6625),
    # "dunedin": (-45.8742,	170.5036),
    # "invercargill": (-46.4131,	168.3475),
    # "stewart-island": (-47, 167.84)
  }
  
  def compute_closest(self, point):
    """ Find the closest region to a given point

    Args:
        point: The point to which the closest region should be found

    Returns:
        An object with name of the closest region and the distance to that region from the give point
    """
    minimum = {
      "name": "",
      "distance": float("inf")
    }
    
    for key, value in self.locations.items():
      distance =  mpu.haversine_distance(point, value)
      if distance < minimum["distance"]:
        minimum = {
          "name": key,
          "distance": distance
        }
           
    return minimum