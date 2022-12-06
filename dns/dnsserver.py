# Using a base resolver to make a custom DNS request and handle it
from dnslib.server import BaseResolver


class DNS(BaseResolver):
    """
    This class is a DNS resolver that uses an active measurement process to resolve DNS queries.
    All available IPs are stored in a config file which the active measurement uses.
    """
    def __init__(self, strategy):
        self.strategy = strategy

    def resolve(self,request,handler):
        pass
