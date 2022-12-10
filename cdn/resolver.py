# Using a base resolver to make a custom DNS request and handle it
from dnslib.server import BaseResolver, DNSHandler
from dnslib import DNSRecord, QTYPE, RR, A, RCODE


class Resolver(BaseResolver):
    """
    This class is a DNS resolver that uses an active measurement process to resolve DNS queries.
    All available IPs are stored in a config file which the active measurement uses. This is
    passed as a parameter to the DNS server.
    """

    def __init__(self, strategy, name):
        self.strategy = strategy
        # Passing the name of the DNS server so that it can be added to the response object.
        self.name = name

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
        print(closest_replicas)
        # Create a DNS response
        reply = request.reply()
        reply.add_answer(RR(rname=self.name, rdata=A(closest_replicas[0][0])))
        return reply
