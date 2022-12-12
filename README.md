# Project 4: Roll Your Own CDN

Authors :

*Nikhil Mollay : 001020022*

*Dileep Kumar Shah : 001044150* 

## High Level Approach
Our approach to this project is to implement a server CDN using the following steps:
1. Create a server that can handle multiple clients
2. DNS lookup to get the IP address of the server
3. Create a cache based on frequency accessed websites.

## Contributions 

*Nikhil Mollay* :
Responsible for the following tasks:
1. Implementing the server side code for the CDN
2. DNS resolution for the CDN
3. Geo-IP based routing for the CDN 
4. Active measurement of the CDN performance

*Dileep Kumar Shah* : 
Responsible for the following tasks:
1. Http server implementation
2. Cache implementation
3. Cache eviction policy implementation
4. Cache replacement policy implementation
5. Testing and debugging the code for http server and cache
6. Writing the report
7. Active measurement of the CDN performance initial code


## Challenges:
1. DNS resolution for the CDN for the was challenging to implement.
2. Geo-IP based routing for the CDN was challenging to understand and implement.
3. Active measurement of the CDN performance was challenging to implement and took a lot of time to understand.
4. Cache and eviction policy implementation was challenging to implement.
5. Understanding the grading beacon, deploy run code on replicas and cdn server was difficult.
6. Testing and debugging the code was challenging.

## How to run the code
1. Go to the directory where the code is present.
2. Run the following command to compile the code:
```
make
```
3. Run the following command to deploy/run/stop the server:
```
./[deploy|run|stop]CDN -p <port> -o <origin> -n <name> -u <username> -i <keyfile>
```

## Testing
1. Used wget to test the http server. Used diff tool to compare the files downloaded from the httserver and the origin file.
2. Used test scripts to test the cache implementation.

## References
1. https://manpages.ubuntu.com/manpages/trusty/man1/scamper.1.html
2. https://www.geeksforgeeks.org/geoip-based-routing/
3. https://github.com/paulc/dnslib/tree/master/dnslib
4. https://github.com/maxmind/GeoIP2-python
5. https://docs.python.org/3/library/urllib.html
6. https://docs.python.org/3/library/sqlite3.html


