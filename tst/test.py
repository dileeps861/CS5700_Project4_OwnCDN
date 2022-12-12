from dnslib import DNSRecord

if __name__ == '__main__':
    q = DNSRecord.question('www.example.com')
    a = q.send('localhost', 25019)

    print(DNSRecord.parse(a))