from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread
import tkinter as tkt
import time

FORMAT = "utf-8"
SERVER = "localhost"
PORT = 60000
BUFSIZE = 1024
ADDRESS = (SERVER, PORT)
FONT_SMALL = "Arial", 15
FONT_BIG = "Arial", 20
SERVER_OFFLINE = "Il server non è online"
CLOSING = "{close}"

running=True
username=""

def send(message):
    try:
        client_socket.send(bytes(message, FORMAT))
    except:
        if message != CLOSING:
            main_text.insert(tkt.END,SERVER_OFFLINE)

def main_pack():
    main_frame.pack(expand=True, fill="both")
    
def receive():
    while running:
        try:
            message = client_socket.recv(BUFSIZE).decode(FORMAT)
            main_text.insert(tkt.END,message)
        except ConnectionResetError:
            print("Connessione al server interrotta.")
            break
        except Exception:
            pass
        
def enter(event=None):
    message = main_entry.get()
    main_entry.delete(0, tkt.END)
    send(message)

def login():
    global username
    username = login_entry.get()
    if username != "":
        send(username)
        main_label.config(text=username)
        login_frame.destroy()
        main_pack()
    
def on_close():
    print("Chiusura dell'applicazione.")
    window.destroy()
    global running
    running = False
    send(CLOSING)
    
def start_connection():
    global client_socket
    client_socket = socket(AF_INET, SOCK_STREAM)
    while running:
        try:
            client_socket.connect(ADDRESS)
        except Exception:
            print(SERVER_OFFLINE)
            time.sleep(2)
        else:
            send(username)
            print("Connessione al server stabilita.")
            r=Thread(target=receive)
            r.start()
            r.join()
            
            client_socket = socket(AF_INET, SOCK_STREAM)

if __name__ == "__main__":
    client_socket = ""
    # window creation
    window=tkt.Tk()
    window.geometry("800x600")
    window.title("RealTime Chat")
    
    # login configuration
    login_frame=tkt.Frame(window)
    login_label=tkt.Label(login_frame,
                          text="Username",
                          font=FONT_BIG)
    login_entry=tkt.Entry(login_frame,
                          font=FONT_SMALL)
    login_button=tkt.Button(login_frame,
                            text="Login",
                            font=FONT_BIG,
                            command=login)
    login_frame.pack(expand=True, fill="both")
    login_label.pack(pady=10)
    login_entry.pack(pady=10)
    login_button.pack(pady=10)
    
    
    # main configuration
    main_frame=tkt.Frame(window,
                         background="lightgreen")
    main_label=tkt.Label(main_frame,
                         font=FONT_BIG,
                         foreground="green",
                         background="lightgreen")
    main_text=tkt.Listbox(main_frame,
                          font=FONT_SMALL)
    main_entry=tkt.Entry(main_frame,
                         font=FONT_SMALL)
    main_button=tkt.Button(main_frame,
                          font=FONT_BIG,
                          text="Enter",
                          foreground="green",
                          background="lightgreen",
                          command=enter)
    main_entry.bind("<Return>", enter)
    main_label.pack()
    main_text.pack(expand=True, fill="both")
    main_entry.pack(side="left", expand=True, fill="x", padx=5)
    main_button.pack(side="right")
    
    # window loop start
    Thread(target=start_connection).start()
    window.protocol("WM_DELETE_WINDOW", on_close)
    window.mainloop()
