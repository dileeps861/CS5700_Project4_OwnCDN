"""
This file is the main entry file for the http server. It will start the server and listen to the requests.
"""
import argparse
import sys
import threading
import time

from httpreq.http_replica_server import Server

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Parser for DNS server')
    parser.add_argument('-p', type=int, default=25019, help='The port the http server will bind to')
    parser.add_argument('-o', type=str, default='cs5700cdnorigin.ccs.neu.edu',
                        help='The origin server name which the client will connect to')
    args = parser.parse_args()
    print("Port bound to ", args.p)
    serverObj = Server(args.p, args.o)
    server = serverObj.start_server()

    # server.serve_forever()
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    try:
        while 1:
            time.sleep(1)
            sys.stderr.flush()
            sys.stdout.flush()

    except KeyboardInterrupt:
        pass
    finally:
        server.shutdown()
