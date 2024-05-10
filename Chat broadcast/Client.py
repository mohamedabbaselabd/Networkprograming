import socket
import tkinter as tk
from tkinter import ttk
import threading

def send_message():
    message = input_entry.get()
    chat_listbox.insert(tk.END, f"{alias}: {message}")
    client_socket.send(message.encode())
    input_entry.delete(0, tk.END)

def receive_messages():
    while True:
        try:
            data = client_socket.recv(1024).decode()
            chat_listbox.insert(tk.END, data)
        except:
            print("An error occurred while receiving messages.")
            client_socket.close()
            break

def connect_to_server():
    global client_socket, alias
    host = '127.0.0.1'
    port = 7002
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))
    print("Connected to the server.")
    alias = input("Enter your alias: ")
    client_socket.send(alias.encode())
    receive_thread = threading.Thread(target=receive_messages)
    receive_thread.start()

# Create GUI
window = tk.Tk()
window.title("Chat Client")

mainframe = ttk.Frame(window)
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.W, tk.E, tk.S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

chat_listbox = tk.Listbox(mainframe, width=50, height=20)
chat_listbox.grid(column=1, row=1, padx=10, pady=10)

input_entry = ttk.Entry(mainframe, width=50)
input_entry.grid(column=1, row=2, padx=10, pady=10)

send_button = ttk.Button(mainframe, text="Send", command=send_message)
send_button.grid(column=1, row=3, padx=10, pady=10)

connect_to_server()

window.mainloop()
