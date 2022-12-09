# Using a base resolver to make a custom DNS request and handle it
from dnslib.server import BaseResolver, DNSHandler


class Resolver(BaseResolver):
    """
    This class is a DNS resolver that uses an active measurement process to resolve DNS queries.
    All available IPs are stored in a config file which the active measurement uses. This is
    passed as a parameter to the DNS server.
    """

    def __init__(self, strategy):
        self.strategy = strategy

    def resolve(self, request, handler):
        """
        A function that resolves the DNS request and returns the IP address of the closest replica.
        :param request: The DNS request from the client
        :param handler: Handler to handle the DNS request
        :return: An IP address of the closest replica
        """
        print(request)
        print(handler.client_address)
        return request.reply()
        pass
