"""This script return a list of the closest replica servers in its zone. Using the scamper tool
to find all the closest IPs"""


class ActiveMeasure:
    """
    A class that actively measures the load in the server and also returns a list of all the
    closest replicas from the origin of the request.
    """

    def __init__(self):
        pass

    def find_closest_ips(self, client_ip):
        """
        This function finds the closest IPs from the client to based on an active measurement
        strategy. Uses scamper which runs remotely on the replicas to ping the client. The
        replica with the lowest RTT is the closest replica.
        """
        pass