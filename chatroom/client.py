from threading import Thread
import socket            
 


def handle_printing(socket):
    while True:
        received_msg = socket.recv(1024).decode()
        
        if not received_msg:
            break
        
        received_msg = str(received_msg)
        for line in received_msg.splitlines():
            print(f"> {line}")




def runner():
    
    # Create a socket object
    s = socket.socket()        
    
    port = 12345              
    s.connect(('127.0.0.1', port))
    print("client connected to server successfully!")

    thread = Thread(target = handle_printing, args = (s, ))
    thread.start()

    while True:
        text = input()
        
        s.send(text.encode())

        if text == "-2":
            break

    s.close()
    
runner()