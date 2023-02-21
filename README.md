

To run this project:
* Create docker image by using Dockerfile:
  - docker build -t dns-server .
* Create docker network by using this command:
  - docker network create --subnet 172.168.1.0/24 testNetwork
* Run the container by using that docker image we created in the previous step by run this command:
  - docker run --rm --network testNetwork -it -p 53:53 dns-server
* Start a new container in the same network(Let's say using Ubuntu machine), run below commands:
  - docker run --rm --network testNetwork -it ubuntu
  - apt update
  - apt install dnsutils
* You can test this by making dig request
  - dig @172.168.1.2 -p 53 google.com
* On successful response server will give 200 response code and inside Ubuntu container you will see the result.