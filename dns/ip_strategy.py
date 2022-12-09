class IPMeasure():
    """
    A class to find the closest IP from the client to the closest replica server based on
    geolocation. Using a maxmind database to find the closest IP to the client. Also maintains a
    queue of closest IPs to the client in order to cycle through IPs if one fails.
    """

    def __init__(self):
        # Precalculated lat long for all the replica IPs.
        self.replica_ip_lat_long = {"139.144.30.25": (33.844, -84.4784),
                                    "173.255.210.124": (37.5625, -122.0004),
                                    "139.144.69.56": (50.1188, 8.6843),
                                    "185.3.95.25": (51.5164, -0.093),
                                    "139.162.83.107": (35.6893, 139.6899),
                                    "192.46.211.228": (19.0748, 72.8856),
                                    "170.187.240.5": (-33.8715, 151.2006),
                                    }

    def find_closest_ip(self, client_ip, replica_ips):
        """
        This function finds the closest IP from the client to the closest replica server based on
        geolocation.
        """
        pass

    def client_location_from_db(self):
        """
        This function finds the location of the client from the maxmind database. Uses geoip2
        database.
        :return:
        """
        pass

    def check_if_private(self, ip_address):
        """
        This function checks if the IP address is private or not. We convert the IP address to
        its decimal form to check if the values fall within the private IP ranges.
        :param ip_address: The IP address to check
        :return: True if the IP is private, False otherwise
        """
        pass