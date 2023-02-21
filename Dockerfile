FROM python:3.9
RUN apt-get install openssl
WORKDIR /usr/local/bin
COPY myserver.py .
CMD ["python","myserver.py"]