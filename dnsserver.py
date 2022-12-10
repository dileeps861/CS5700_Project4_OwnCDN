"""
This script is the entry point for the DNS server. It creates a DNS server and instantiates the
Resolver class and the strategy class, which is to be used by the resolver.
"""

from dnslib.server import DNSServer
from dns.resolver import Resolver
from dns import ip_strategy
import argparse


def start_server(port_number, name_server):
    """
    This function starts the DNS server.
    :param port_number: The port number to bind the DNS server on
    :param name_server: The name of the server.
    """
    print("Port bound to ", port_number)
    print("Name server is ", name_server)
    strategy = ip_strategy.IPMeasure()
    resolver = Resolver(strategy, name_server)
    server = DNSServer(resolver, port=port_number, address=name_server)
    server.start()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for DNS server')
    parser.add_argument('-p', type=int, default=25019, help='The port the dns server will bind to')
    parser.add_argument('-n', type=str, default='localhost',
                        help='The CDN name which the '
                             'server will convert to '
                             'an IP')
    args = parser.parse_args()
    start_server(args.p, args.n)
