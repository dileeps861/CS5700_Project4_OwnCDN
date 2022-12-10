import random
from math import sqrt

import geoip2.errors
from geoip2.database import Reader


class IPMeasure:
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
        self.private_ip_ranges = [(167772160, 184549375), (2886729728, 2887778303), (3232235520,
                                                                               3232301055)]
        # Maintain a cache and result of all seen client IPs upto this point
        self.ip_cache = {}

    def find_closest_ip(self, client_ip):
        """
        This function finds the closest IP from the client to the closest replica server based on
        geolocation.
        """
        if self.check_if_private(client_ip):
            # If the IP is private, we return a random shuffled order of replica IPs.
            return random.shuffle(list(self.replica_ip_lat_long.values()))

        # Find the closest IP to the current one using a distance algorithm
        ip_distance_vector = []  # This stores a tuple with the IP and the associated distance
        for key, value in self.replica_ip_lat_long.items():
            print("Here!")
            ip_distance_vector.append(
                (key, self.calculate_distance(value, self.client_location_from_db(client_ip))))

        # Returning a list of all replicas which are closest to the client
        ip_distance_vector.sort(key=lambda x: x[1])
        return ip_distance_vector

    def client_location_from_db(self, client_ip):
        """
        This function finds the location of the client from the maxmind database. Uses geoip2
        database.
        :return: A set of latitude and longitude of the client.
        """
        with Reader('./res/GeoLite2-City.mmdb') as reader:
            try:
                response = reader.city(client_ip)
                return response.location.latitude, response.location.longitude
            except geoip2.errors.AddressNotFoundError:
                return random.choice(list(self.replica_ip_lat_long.values()))

    def check_if_private(self, ip_address):
        """
        This function checks if the IP address is private or not. We convert the IP address to
        its decimal form to check if the values fall within the private IP ranges.
        :param ip_address: The IP address to check
        :return: True if the IP is private, False otherwise
        """
        ip_in_decimal = self.convert_ip_to_decimal(ip_address)

        for ips in self.private_ip_ranges:
            if ips[0] <= ip_in_decimal <= ips[1]:
                return True

        return False

    def convert_ip_to_decimal(self, ip_address):
        """
        This function converts the IP address to its decimal form.
        :param ip_address: The IP address to convert
        :return: The decimal form of the IP address
        """
        ip_in_decimal = 0
        ip_nums = ip_address.split('.')

        for i in range(0, 4):
            p = 3 - i
            ip = int(ip_nums[i])
            ip_in_decimal += ip * (256 ** p)

        return ip_in_decimal

    def calculate_distance(self, replica_coordinates, client_coordinates):
        """
        This function calculates the distance between the client and the replica server using
        Euclidean distance between the two coordinates.
        :param replica_coordinates: The coordinates of the replica server
        :param client_coordinates: The coordinates of the client
        :return: The distance between the client and the replica server
        """
        return sqrt(((replica_coordinates[0] - client_coordinates[0]) ** 2) + (
                    (replica_coordinates[1] - client_coordinates[1]) ** 2))
