FROM python:3.9
RUN apt-get install openssl
WORKDIR /usr/local/bin
COPY dns-proxy.py .
CMD ["python","dns-proxy.py"]