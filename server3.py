import socket
import cv2
import numpy as np
from random import randint

#v1 = cv2.VideoCapture('2.mp4') # Streaming a locally stored video file
v1 = cv2.VideoCapture(0)  # Capturing video from webcam
print("Video capture start")
HOST = socket.gethostbyname(socket.gethostname()) # To get server IP address
#HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 65432        # Port to listen on (non-privileged ports are > 1023)
#PORT = randint(20000,65535) # Randomizing server PORT to avoid connection problems if PORT is in use
i=0
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket is created
s.bind((HOST, PORT)) # TCP socket is associated with provided HOST ip address and PORT
print("Server running")
print("Connect to IP:"+HOST+" Port:"+str(PORT))
while(True):
    i=i+1
    (p,a)=v1.read() # Frames from video are captured
    #print(a)
    a=cv2.resize(a, (320, 240))
    #a=cv2.resize(a, (150, 144))
    l=[len(a)] # Dimension of image 
    #print(l)
    a1=bytearray(a) # 3d array is converted to bytes
    a2=bytearray(l) # Dimension is converted to bytes
    tl=str(len(a1)+len(a2))
    a3=bytearray(tl,'utf-8') # Total bytes length converted to bytes
    #print("packetsize",tl)
    s.listen() # Server program is listening for connections from client
    conn, addr = s.accept() # Server accepts connection with client after client pings the server
    data = conn.recv(1024) # Confirming whether the client is Ready to recieve data
    
    if(data): # Confirming whether the client is Ready to recieve data
        conn.sendall(a3) # Sending bytes length to inform client not to close connection until this amount of bytes are transferred
        s.listen() # Waiting for client to process and connect
        conn, addr = s.accept() # Server accepts connection with client after client pings the server
        conn.sendall(a2+a1) # Server sending actual data (Dimension + 3d array)
        #print("Frames sent",i)
print("Closed")
