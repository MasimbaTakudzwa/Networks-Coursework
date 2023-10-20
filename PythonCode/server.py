import socket
import threading
import argparse
import logging

# Host at local address
host = '127.0.0.1'
# User argparser to parse port number with -p flag
parser = argparse.ArgumentParser(description='get port number')
parser.add_argument('-p', '--port_number', required=True, type=int,help='Enter the port number')
args = parser.parse_args()

logging.basicConfig(filename='server.log', level=logging.DEBUG)
port = args.port_number

# Prepare socket to host server
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((host, port))
server.listen()

# Create arrays to hold clients information names and chosen nicknames
clients = []
nicknames = []

# Create broadcast function to broadcast messages to group chat
def broadcast(message):

    # Send message to every client
    for client in clients:
        client.send(message)

# Message handler
def handle(client):
    while True:

        # Try receive message and decode it
        try:
            message = client.recv(1024)
            broadcast(message)
            logging.info(f'{client} sent message')

        # If that does not work it must mean client must have left the chat close recources for that client
        except:
            index = clients.index(client)

            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            broadcast(f'{nickname} left the chat.'.encode('ascii'))
            logging.info(f'{client} with nickname {nickname} disconnected from chat')
            nicknames.remove(nickname)
            break


def receieve_message():
    # Get client info and add it to list of clients and nicknames and broadcast nickname has joined chat
    while True:

        client, addr = server.accept()
        print(f"Connected with {str(addr)}")
        client.send('clear'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        logging.info(f'{client} connected to server with address {addr} and nickname {nickname}')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname of client is {nickname}')
        broadcast(f'{nickname} joined the chat'.encode('ascii'))
        client.send('Connected to server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

# Call receive message
receieve_message()