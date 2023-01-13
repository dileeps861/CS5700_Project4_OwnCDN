# Using a base resolver to make a custom DNS request and handle it
import threading

from dnslib.server import BaseResolver, DNSHandler
from dnslib import DNSRecord, QTYPE, RR, A, RCODE
import cdn.server_load_measure


class Resolver(BaseResolver):
    """
    This class is a DNS resolver that uses an active measurement process to resolve DNS queries.
    All available IPs are stored in a config file which the active measurement uses. This is
    passed as a parameter to the DNS server.
    """

    def __init__(self, strategy, name, port):
        self.server_load = {"139.144.30.25": 0, "173.255.210.124": 0, "139.144.69.56": 0,
                            "185.3.95.25": 0, "139.162.83.107": 0, "192.46.211.228": 0,
                            "170.187.240.5": 0}
        self.strategy = strategy
        # Passing the name of the DNS server so that it can be added to the response object.
        self.name = name
        # threading.Thread(
        #     target=cdn.server_load_measure.ReplicaServerLoadMeasure.get_replica_loads_using_scamper,
        #     args=(["139.144.30.25",
        #            "173.255.210.124",
        #            "139.144.69.56",
        #            "185.3.95.25",
        #            "139.162.83.107",
        #            "192.46.211.228",
        #            "170.187.240.5",
        #            ], port, self.server_load)).start()
        self.port = port

    def resolve(self, request, handler):
        """
        A function that resolves the DNS request and returns the IP address of the closest replica.
        :param request: The DNS request from the client
        :param handler: Handler to handle the DNS request
        :return: An IP address of the closest replica
        """
        client_ip = handler.client_address[0]
        client_port = handler.client_address[1]
        closest_replicas = self.strategy.find_closest_ip(client_ip)
        cdn.server_load_measure.ReplicaServerLoadMeasure.measure_with_scamper_attach()
        # Check server loads using scamper and test the latency of the replicas
        # Create a DNS response
        return request.reply().add_answer(RR(rname=self.name, rdata=A(closest_replicas[0][0])))

    def decide_based_on_load(self, replica_loads, replica_distances):
        """
        This function decides which replica to return based on the load of the replicas. It also
        takes into account the distance of the replicas from the client.
        :param replica_loads: A list of tuples of replica IPs and their load
        :param replica_distances: A list of tuples of replica IPs and their distance from the client
        :return: The IP of the replica with the least load
        """
        replica_loads.sort(key=lambda x: x[1])

        # Decide on which replica to choose based on load and distance

        for server, replica_distances in replica_loads:
            replica_rating = replica_loads[server]

        return replica_loads[0][0]
