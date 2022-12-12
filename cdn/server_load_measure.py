# Code to measure the replica server load
import os

class ReplicaServerLoadMeasure:
    def __init__(self):
        self.geo_ip_locator = None
        self.load = 0

    def get_load(self):
        return self.load

    def reset_load(self):
        self.load = 0

    # Run scamper command to probe replica IPs
    @staticmethod
    def measure_with_scamper_attach():
        command = "sc_attach -c 'ping' -i replicas.txt -p 26099"
        cmd = os.popen(command)
        out = cmd.read()
        cmd.close()
        print(out)
