import socket
import ssl
import binascii
import threading

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

# Handle incoming TCP connections
def handle_tcp_connection(conn, addr, dns):
    print("Handling connection from", addr)
    # Receive incoming DNS request
    data = conn.recv(1024)
    # Establish a TLS connection with the Cloudflare server
    tls_conn_sock = establish_tls_connection(dns)
    print("TLS connection with Cloudflare established.")
    # Send DNS query to Cloudflare server over TLS
    print("Sending query....")
    tls_conn_sock.send(data)
    tcp_result = tls_conn_sock.recv(1024)
    # Check the response
    print("Checking for response now....")
    if tcp_result:
        rcode = binascii.hexlify(tcp_result[:6])
        rcode = str(rcode)[11:]
        if (rcode.rstrip() == '1a0'):
            # Not a DNS query
            print("This is not a DNS query")
        else:
            # Send the response back to the client over TCP
            conn.send(tcp_result)
            print("Response received: 200")
    else:
        print("No TCP result received...")
    # Close the connection
    conn.close()
    print("Connection closed")

if __name__ == '__main__':
    DNS = '1.1.1.1' # Cloudflare DNS server IP
    port = 53 # DNS port
    host = '172.168.1.2' # Server IP
    print("[SERVER] started.....")
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind((host, port))
        s.listen(5)
        while True:
            # Wait for incoming TCP connection
            conn, addr = s.accept()
            # Handle the TCP connection in a new thread
            threading.Thread(target=handle_tcp_connection, args=(conn, addr, DNS)).start()
    except OSError as e:
        print(e)
    finally:
        s.close()
