
class IPMeasure():
    """
    A class to find the closest IP from the client to the closest replica server based on
    geolocation. Using a maxmind database to find the closest IP to the client. Also maintains a
    queue of closest IPs to the client in order to cycle through IPs if one fails.
    """
    def __init__(self):
        pass

    def find_closest_ip(self, client_ip, replica_ips):
        """
        This function finds the closest IP from the client to the closest replica server based on
        geolocation.
        """
        pass
