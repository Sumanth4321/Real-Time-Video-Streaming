import cv2
import socket
import numpy as np
i=0
j=0
#HOST = '192.168.1.4' # IP address of server 
HOST = input("Enter IP address of server:")
#PORT = 65432        # The port used by the server
PORT = int(input("Enter server PORT number:"))
while(True):
    length=0
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket is created
    s.connect((HOST, PORT)) # Connection is made with server (Ping)
    s.sendall(b'ready') # Sending the server that client is Ready to recieve data
    dat = s.recv(1024) # Recieving byte length as bytes
    s.close() # Closing the established connection
    dat1=str(dat)
    dat1=dat1[2:-1]
    dat2=int(dat1) # Getting byte length from the received bytes
    data1=bytes([]) # Empty byte object
    s=socket.socket(socket.AF_INET, socket.SOCK_STREAM) # TCP socket is created (New)
    s.connect((HOST, PORT)) # Connection is made with server again
    while(length<dat2): # Looping until all the data is recieved
        data = s.recv(4096) # Receiving the actual data in pieces
        data1 = data1+data # Received piece is added to previous piece
        length = len(data1) # Length of recieved bytes is updated every iteration
    data1=list(data1) # Recieved bytes are converted to 1d array
    l=data1.pop(0) # First data in the list is stored in l and removed from array(Dimension of image)
    try:
        l1=np.reshape(data1,(l,int(len(data1)/(l*3)),3)) # Converting 1d array to 3d array 
        l1=l1.astype(np.uint8) # Type conversion so that opencv module can process and display the frame
        cv2.imshow("Papyrus", l1) # Displaying the recieved frame(image)
        cv2.waitKey(1)
        j=j+1
        #print(l,int(len(data1)))
        #print("Frames decoded:",j)
    except:
        i=i+1
        #print("Frame decode error / Frames lost:",i)

        
    
