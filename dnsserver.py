"""
This script is the entry point for the DNS server. It creates a DNS server and instantiates the
Resolver class and the strategy class, which is to be used by the resolver.
"""

from dnslib.server import DNSServer
from dns.resolver import Resolver
import argparse


def start_server(port_number, name_server):
    """
    This function starts the DNS server.
    :param port_number: The port number to run the DNS server on
    :param name_server: The name of the server
    """

    pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for DNS server')
    parser.add_argument('-p', type=int, default=25019, help='The port the dns server will bind to')
    parser.add_argument('-n', type=str, default='cs5700cdn.example.com',
                        help='The CDN name which the '
                             'server will convert to '
                             'an IP')
