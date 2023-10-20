import socket
import threading
import logging
nickname = input(str("Choose a nickname"))
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('127.0.0.1', 65535))

# Create function for receiving message
def recieve_message():
    while True:

        try:
            message = client.recv(1024).decode('ascii')
            # Line added to make sure client has connected server and send nickname of client.
            if message == 'clear':
                client.send(nickname.encode('ascii'))
                pass
            else:
                logging.info(f'{client} with nickname {nickname} recieved message')
                print(message)

        except:
            logging.info("Error occurred")
            print("Error occurred")
            client.close()
            break

# Message entering and sending function
def write_message():
    while True:
        message = f'{nickname}: {input("")}'
        client.send(message.encode('ascii'))
        logging.info(f'{client} with {nickname} sent message')

# Use threads to simultaneously display and send messages allowing users to continuously send and view up to date chat room
recieve_thread = threading.Thread(target=recieve_message)
recieve_thread.start()

write_thread = threading.Thread(target=write_message)
write_thread.start()