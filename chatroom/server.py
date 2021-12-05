from threading import Thread
import re
import socket


help_message = """
to join a room, use  : -join; roomID
to create a room, use: -create; roomID
"""


rooms = {}


def send_msg_in_room(conn, roomID, userName, msg):

    room = rooms[roomID]
    room = list(room)

    # user connection
    for user_conn in room:
        if user_conn != conn:
            user_conn.send(f"'{userName}' said: {msg}".encode())


# remove connection from room
def remove_from_room(roomID, conn):
    room = rooms[roomID]
    room = list(room)

    room.remove(conn)
    rooms[roomID] = room


def create_room(roomID, conn):
    if roomID in rooms.keys():
        conn.send("room ID is exist. try another ID".encode())
        return False

    rooms[roomID] = [conn]
    return True


def add_to_room(roomID, conn):
    
    if roomID not in rooms.keys():
        conn.send("room ID isn't exist. try another ID".encode())
        return False

    room = rooms[roomID]
    room = list(room)

    room.append(conn)
    rooms[roomID] = room
    return True

def handle_client(new_connection, new_addr):

    new_connection.send("Enter your name\n".encode())
    user_name = new_connection.recv(1024).decode()
    user_name = str(user_name).strip()
    if not user_name:
        user_name = "ananymous"

    new_connection.send(
        f"Welcome, join or create room with ID!\ntype -help for more info!\n".encode()
    )

    while True:

        # receive message from client to join or create room
        user_msg = new_connection.recv(1024).decode()
        user_msg = str(user_msg)

        if "-help" in user_msg:
            new_connection.send(help_message.encode())
            continue

        reg = "^(-join|-create)(; )(.+)"
        reg_res = re.search(reg, user_msg)
        if not reg_res:
            new_connection.send("your input is not valid. try again!".encode())
            continue

        room_id = user_msg.split("; ")[1]
        print(room_id)
        print("roomid:    " + room_id)
        if "-create" in user_msg:  # id not exist yet
            created = create_room(roomID=room_id, conn=new_connection)
            if not created:
                continue
            new_connection.send(f"your room is created successfully with {room_id} id".encode())
        elif "-join" in user_msg:
            added = add_to_room(roomID=room_id, conn=new_connection)
            if not added:
                continue
            
            new_connection.send(f"you are in {room_id} room now. type something!".encode())

            
            send_msg_in_room(
                    conn=new_connection,
                    roomID=room_id,
                    userName=user_name,
                    msg=f"{user_name} joined us in {room_id} room",
                )

        
        want_to_leave_room = False
        while True:
            received_msg = new_connection.recv(1024).decode()

            # send back message to client. just for test
            print("received from client " + str(received_msg))

            if received_msg == "-1": # -1 means user wants to leave room and create or join to new room
                                     # but -2 means user wants to leave the chatroom! 
                want_to_leave_room = True
                
            if received_msg == "-1" or received_msg == "-2":
                
                
                received_msg = "goodBYE"
                # say goodbye to all room members
                send_msg_in_room(
                    conn=new_connection,
                    roomID=room_id,
                    userName=user_name,
                    msg=received_msg,
                )
                # remove from room
                remove_from_room(roomID=room_id, conn=new_connection)
                break

            send_msg_in_room(
                conn=new_connection,
                roomID=room_id,
                userName=user_name,
                msg=received_msg,
            )
        
        if want_to_leave_room:
            continue # create or join to new room
        
        break #outer while loop

def runner():
    # next create a socket object
    s = socket.socket()
    print("Socket successfully created")

    port = 12345

    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    s.bind(("", port))
    print("socket binded to %s" % (port))

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

    while True:

        # Establish connection with client.
        conn, addr = s.accept()

        address = str(addr[1])

        print("Got connection from", address)
        # send a thank you message to the client. encoding to send byte type.

        thread = Thread(
            target=handle_client,
            args=(
                conn,
                address,
            ),
        )
        thread.start()


runner()
