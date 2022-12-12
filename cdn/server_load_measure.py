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
    def get_replica_loads_using_scamper(replica_ips, replica_port, replica_ip_ratings_pairs):
        scamper_cmd = "timeout 3s scamper -c \"trace -d " + str(replica_port) + " -P tcp-ack\""
        for ip in replica_ips:
            scamper_cmd += " -i " + ip[0]
        cmd = os.popen(scamper_cmd)
        out = cmd.read()
        cmd.close()
        # Parse scamper output
        ip_logs = out.split("traceroute")
        print(ip_logs)
        for single_ip_log in ip_logs:
            single_ip_log = single_ip_log.strip()
            if single_ip_log == "":
                continue
            ip_log_lines = single_ip_log.split("\n")
            # Parse replica ip
            replica_ip = ip_log_lines[0].split("to")[1].strip()
            ratings = 0
            if len(ip_log_lines) > 0:
                # last hop has star which means the replica was unreachable.
                if "*" in ip_log_lines[len(ip_log_lines) - 1]:
                    ratings = -10
                else:
                    # a star in one of the hops means the replica was reachable but some packets
                    # were probably lost.
                    for single_ip_log_line in ip_log_lines:
                        if "*" in single_ip_log_line:
                            ratings = -5
                            break

            replica_ip_ratings_pairs[replica_ip] = ratings

    @staticmethod
    def measure_with_scamper_attach():
        command = "sc_attach -c 'ping' -i replicas.txt -p 26099"
        cmd = os.popen(command)
        out = cmd.read()
        cmd.close()
        print(out)
