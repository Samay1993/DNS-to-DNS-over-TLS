# What is this project about?
  This script implements a DNS proxy server that intercepts incoming DNS requests over TCP on port 53 and forwards them to a Cloudflare DNS server over TLS for resolution, then sends the response back to the client over the same TCP connection.

# Fuctionalities implemented:
  - Used Python3 to create this project
  - Using Cloudflare as the DNS server to query client request on **1.1.1.1:853**.
  - Only handeling TCP request at this time, but it can handle multiple TCP requests at the same time.

# Project Flow:
  - The server starts by initializing the Cloudflare DNS server's IP address, the server's listening port, and the server's IP address.
  - The _handle_tcp_connection_ function is defined to handle incoming TCP connections. It takes in the connection, address of the client, and the Cloudflare DNS server IP address as arguments.
  - The function receives the incoming DNS request from the client over the TCP connection.
  - It establishes a TLS connection with the Cloudflare DNS server by creating a socket and wrapping it with an SSL context.
  - The DNS request is sent to the Cloudflare DNS server over the TLS connection.
  - The response from the Cloudflare DNS server is received and checked for a valid DNS response.
  - If the response is valid, it is sent back to the client over the TCP connection.
  - The TCP connection is closed, and the function returns.
  - In the main block, the server creates a TCP socket and binds it to the server's IP address and listening port.
  - It listens for incoming TCP connections and creates a new thread for each connection to handle it.
  - The server runs indefinitely until an error occurs or it is stopped manually.

# To run this project:
* Create docker image by using Dockerfile:
  - > docker build -t dns-proxy .
* Create docker network by using this command:
  - > docker network create --subnet 172.168.1.0/24 testNetwork
* Run the container by using that docker image we created in the previous step by run this command:
  - > docker run --rm --network testNetwork -it -p 53:53 dns-proxy
* Start a new container in the same network(Let's say using Ubuntu machine), run below commands:
  - > docker run --rm --network testNetwork -it ubuntu
  - > apt update
  - > apt install dnsutils -y
* You can test this by making dig request
  - > dig @172.168.1.2 -p 53 google.com
* On successful response server will give 200 response code and inside Ubuntu container you will see the result.

# Answering the questions asked in the deliverables:

## Q.1: Imagine this proxy being deployed in an infrastructure. What would be the security concerns you would raise?

While using TLS/TCP to secure pipelines and send DNS queries, it's important to note the known security concerns such as:
  - A man-in-the-middle attack can occur when the browser sends a request to the DNS proxy server, and the proxy server creates a TCP connection with the Upstream DNS server, allowing for potential traffic manipulation.
  - Additionally, unauthorized access to cached information about domain names is a concern. Proper use of keys and signed certificates can help mitigate these issues.

## Q.2: How would you integrate that solution in a distributed, microservices-oriented and containerized architecture?

Integrating the DNS over TLS proxy in a distributed, microservices-oriented, and containerized architecture would involve designing a solution that is scalable, resilient, and fault-tolerant.
  - One possible solution could involve deploying the proxy as a containerized microservice within a container orchestration platform such as Kubernetes. The proxy could be deployed as a stateless service, and can be easily replicated scalability and resilience.
  - To ensure high availability and fault tolerance, multiple instances of the proxy could be deployed, and a load balancer such as Nginx could be used to distribute incoming traffic across these instances.
  - In a containerized architecture, it is also important to ensure that the proxy is deployed securely and that the container images are regularly updated with security patches. This can be achieved by implementing a CI/CD pipeline that automatically builds, tests, and deploys new versions of the container images whenever changes are made to the code.
  - In summary, integrating the DNS over TLS proxy in a distributed, microservices-oriented, and containerized architecture would involve deploying the proxy as a stateless microservice within a container orchestration platform, ensuring high availability and fault tolerance, and implementing a secure and automated CI/CD pipeline for building and deploying new versions of the container images.

## Q.3: What other improvements do you think would be interesting to add to the project?

  - Add caching: Implementing a caching system to store frequently accessed DNS records can significantly reduce the response time for DNS queries.
  - Add load balancing: To handle large volumes of traffic, it would be useful to add load balancing functionality that can distribute requests across multiple instances of the proxy server.
  - Add support for other DNS servers: Currently, the proxy only supports Cloudflare DNS. Adding support for other DNS servers would provide users with more options and increase the flexibility of the proxy.
  - Add security features: Implementing security features such as SSL/TLS encryption, authentication, and authorization can help protect against attacks and unauthorized access to the DNS proxy server.