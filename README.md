# Project 4: Roll Your Own CDN

Authors :

*Nikhil Mollay : 001020022*

*Dileep Kumar Shah : 001044150* 

## High Level Approach
Our high level approach was to first build a DNS server that returns a answer based on geo IP and will do active measurements later on to check the status
of the replicas. We used the Dnslib library t obuild the dns server and the maxmind geoip2 library to get the geo location of the client. We also
tried to sue sc_attach and scamper to get some active measurements from the server itself.

For the Http server we used the urllib2 library to create the http server and to also make calls to the origin server. We used sqlute to cache get results in the replica
to ensure persistence. To cache the data at the replicas we followed a LRU cache eviction policy.

## Contributions 

*Nikhil Mollay* :
Responsible for the following tasks:
1. Implementing the server side code for the CDN
2. DNS resolution for the CDN
3. Geo-IP based routing for the CDN 
4. Active measurement of the CDN performance
5. Testing the code for the DNS.
6. Writing the deployment scripts for the DNS server.
7. Writing the report.

*Dileep Kumar Shah* : 
Responsible for the following tasks:
1. Http server implementation
2. Cache implementation
3. Cache eviction policy implementation
4. Cache replacement policy implementation
5. Testing and debugging the code for http server and cache
6. Writing the report
7. Writing the deployment scripts for the http server.
8. Active measurement of the CDN performance initial code


## Challenges:
This project was extremely challenging for both of us. Trying to understand the infrastructure of the server and the replicas was a big challenge. Understanding the workings 
of the DNS server and the usage of dnslib took some time. Trying to get active measurements work with scamper was extremely difficult and 
it took a lot of time to figure out something that would work and be feasible. Http servers caching also took some effort. We tried tons of 
different caching mechanisms and using a file vs a db approach. Furthermore, testing and debugging the code and understanding the grading beacon took
some time and effort.

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


