#AUTHOR Shad0wcry

import socket
import threading
import tkinter as tk
import multiprocessing

class ChatClient:
    def __init__(self, name, host, port):
        self.name = name
        self.host = host
        self.port = port
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.host, self.port))
        self.client_socket.send(name.encode('ascii'))

        self.top = tk.Tk()
        self.top.title(f"{self.name}'s Chat Window")
        self.messages_frame = tk.Frame(self.top)
        self.my_msg = tk.StringVar()  
        self.my_msg.set("")  
        self.scrollbar = tk.Scrollbar(self.messages_frame)  
        self.msg_list = tk.Listbox(self.messages_frame, height=15, width=50, yscrollcommand=self.scrollbar.set)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.msg_list.pack(side=tk.LEFT, fill=tk.BOTH)
        self.messages_frame.pack()
        self.entry_field = tk.Entry(self.top, textvariable=self.my_msg)
        self.entry_field.bind("<Return>", self.send)
        self.entry_field.pack()
        self.send_button = tk.Button(self.top, text="Send", command=self.send)
        self.send_button.pack()
        self.top.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.receive_thread = threading.Thread(target=self.receive)
        self.receive_thread.start()

        self.top.mainloop()

    def receive(self):
        while True:
            try:
                msg = self.client_socket.recv(1024).decode("utf8")
                self.msg_list.insert(tk.END, msg)
            except:
                break

    def send(self, event=None):
        msg = self.my_msg.get()
        self.my_msg.set("")  
        self.client_socket.send(bytes(f"{self.name}: {msg}", "utf8"))

    def on_closing(self, event=None):
        self.my_msg.set("{quit}")
        self.send()

if __name__ == "__main__":
    p1 = multiprocessing.Process(target=ChatClient, args=("Alice", "localhost", 33000))
    p2 = multiprocessing.Process(target=ChatClient, args=("Bob", "localhost", 33000))
    p1.start()
    p2.start()