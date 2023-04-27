#!/usr/bin/python3

# Usage:
#  ./display.py --help
#  ./display.py --port=??? --url=????
#
# Example commands:

#  ./display.py --port=80 --url=http://ut-images.s3.amazonaws.com/wp-content/uploads/2009/09/SED_wall_1920x1200.jpg


import argparse
import string
import socket
import sys
import os
from subprocess import call
from urllib.parse import urlparse

# Size of receive buffer.
# Maximum number of bytes to get from network in one recv() call
max_recv = 64*1024

# Setup configuration
parser = argparse.ArgumentParser(description='Download client for ECPE 170')
parser.add_argument('--url', 
                    action='store',
                    dest='url', 
                    required=True,
                    help='URL of file to download')
parser.add_argument('--port', 
                    action='store',
                    dest='port', 
                    required=True,
                    help='Port number of web server')

args = parser.parse_args()
url = args.url
port = int(args.port)

print("Running download client")
print("Download url: %s" % url)
print("Download port number: %i" % port)

# Split URL into "host", "path", and "filename" variables.
# http://www.google.com/images/srpr/logo3w.png
#  * host=www.google.com
#  * path=/images/srpr
#  * file=logo3w.png

u = urlparse(url)
print("Parsing URL:")
print(" * scheme=%s" % u.scheme)
print(" * netloc=%s" % u.netloc)
print(" * path+file=%s" % u.path)
print(" * path=%s" % os.path.dirname(u.path))
print(" * file=%s" %os.path.basename(u.path))
print()

# Download file (image) from http://host/path/filename
host = u.netloc
path = os.path.dirname(u.path) + '/'
filename = os.path.basename(u.path)

print("Preparing to download object from http://" + host + path + filename)


# *****************************
# STUDENT WORK: 
#  (1) Build the HTTP request string to send to the server
#      and *print it* on the screen.
#
#      Requirements:
#        HTTP 1.1
#        Use the Host header
#        Request the connection be closed after response sent.
#
#      Tip: What is the important sequence of characters that
#      must be provided at the end of the HTTP client request
#      to the server? (otherwise, the server won't begin processing)
# *****************************

request = f"GET {path}{filename} HTTP/1.1\r\nHost: {host}\r\nConnection: close\r\n\r\n"
print("Built Request String: " + request)



# *****************************
# STUDENT WORK: 
#  (2) Create a TCP socket (SOCK_STREAM)
#  (3) Connect to the remote host using the socket
#  (4) Send the HTTP request to the remote host.
#      Tip: Look at the demo client program to see how
#      to convert a unicode string to a byte array
#      prior to transmitting it.
# *****************************


sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((host, 80))
sock.send(bytes(request, 'utf-8'))

# *****************************
# STUDENT WORK: 
#  (5) Receive everything the remote host sends us
#      in chunks of 'max_recv' bytes (64kB).
#      When the server finishes sending us the data,
#      it will close the socket. That is detected locally
#      by receiving an array of length ZERO
#      (i.e. no bytes received)
#  (6) Close the socket - finished with the network now
# *****************************


reponse = b""

while True:
    data = sock.recv(max_recv)
    if not data:
        break
    reponse += data

sock.close()



# *****************************
# STUDENT WORK: 
#  (7) Split the response into two parts:
#        1.) The part before the \r\n\r\n sequence - the HEADER
#        2.) The part after the \r\n\r\n sequence - the DATA
#  (8) Print the HEADER out on the screen - it's ASCII text
#  (9) Save the DATA to disk as a binary file. Somewhere
#      in the /tmp directory would be a great spot.
# *****************************



splitreply =  reponse.split(b'\r\n\r\n')

# Header
header = splitreply[0]
print("Response Header: " + header.decode('utf-8'))

# Image
image = splitreply[1]
f = open('/tmp/image.png', 'wb')
f.write(image)
f.close()


# *****************************
# END OF STUDENT WORK
# *****************************

# Assuming you downloaded the image, and placed its path/filename
# in the variable 'saved_filename', use the 'eog' utility to 
# display the image on screen
call(["eog", "/tmp/image.png"])