from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

FORMAT = "utf-8"
HOST = "localhost"
PORT = 60000
BUFSIZE = 1024
ADDRESS = (HOST, PORT)

clients = {}

def server_handle():
    SERVER.bind(ADDRESS)
    SERVER.listen(5)
    print("In attesa di connessioni...")
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s si è connesso." % client_address)
        client.send(bytes("Benvenuto in chatroom!",FORMAT))
        Thread(target=client_handle, args=(client,client_address)).start()

def close_client(client, msg, nome):
    print(msg)
    client.close()
    del clients[client]
    broadcast(bytes("%s ha abbandonato la chat." % nome, FORMAT))

def client_handle(client,client_address):
    try:
        nome = client.recv(BUFSIZE).decode(FORMAT)
        if nome == "{close}":
            print("%s:%s si è disconnesso." % client_address)
            client.close()
            return
    except ConnectionResetError:
        close_client(client, ("%s:%s si è disconnesso a causa di un problema." % client_address), nome)
    
    msg = "%s si è unito all chat!" % nome
    broadcast(bytes(msg, FORMAT))
    clients[client] = nome
    
    while True:
        try:
            msg = client.recv(BUFSIZE)
            if msg == bytes("{close}", FORMAT):
                close_client(client, ("%s:%s si è disconnesso." % client_address), nome)
                break
            broadcast(msg, nome+": ")
        except ConnectionResetError:
            close_client(client, ("%s:%s si è disconnesso a causa di un problema." % client_address), nome)
            break



def broadcast(msg, prefisso=""):
    for utente in clients:
        utente.send(bytes(prefisso, FORMAT)+msg)
    
if __name__ == "__main__":
    SERVER = socket(AF_INET, SOCK_STREAM)
    ACCEPT_THREAD = Thread(target=server_handle)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()
