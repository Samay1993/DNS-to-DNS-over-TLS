import socket
import ssl
import binascii

# Add length to DNS query datagram
def add_length(dns_query):
    pre_length = b"\x00" + bytes([len(dns_query)])
    query = pre_length + dns_query
    return query

# Send DNS query to Cloudflare server over TLS
def send_query(tls_conn_sock, dns_query):
    tcp_query = add_length(dns_query)
    tls_conn_sock.send(tcp_query)
    result = tls_conn_sock.recv(1024)
    return result

# Establish a TLS connection with the Cloudflare server
def establish_tls_connection(dns):
    tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    tcp_sock.settimeout(10)
    context = ssl.create_default_context()
    context.verify_mode = ssl.CERT_REQUIRED
    context.load_verify_locations('/etc/ssl/certs/ca-certificates.crt')
    tls_sock = context.wrap_socket(tcp_sock, server_hostname=dns)
    tls_sock.connect((dns, 853))
    return tls_sock

# Handle incoming DNS requests
def handle_dns_request(data, address, dns):
    print("Handeling request...")
    # Establish a TLS connection with the Cloudflare server
    tls_conn_sock = establish_tls_connection(dns)
    print("TLS connection with Cloudflare established.")
    # Send DNS query to Cloudflare server over TLS
    tcp_result = send_query(tls_conn_sock, data)
    print("Sending query....")
    # Check the response
    print("Checking for response now....")
    if tcp_result:
        rcode = binascii.hexlify(tcp_result[:6])
        rcode = str(rcode)[11:]
        if (rcode.rstrip() == '1a0'):
            # Not a DNS query
            print("This is not a DNS query")
        else:
            # Send the response back to the client over UDP
            udp_result = tcp_result[2:]
            s.sendto(udp_result, address)
            print("Response received: 200")
    else:
        print("This is not a DNS query")

if __name__ == '__main__':
    DNS = '1.1.1.1' # Cloudflare DNS server IP
    port = 53 # DNS port
    host = '172.168.1.2' # Server IP
    print("[SERVER] started.....")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind((host, port))
        while True:
            # Receive incoming DNS request
            data, addr = s.recvfrom(1024)
            # Handle the DNS request
            handle_dns_request(data, addr, DNS)
    except OSError as e:
        print(e)
    finally:
        s.close()
