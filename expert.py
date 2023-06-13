import socket
import tkinter as tk
from threading import Thread

IP = "127.0.0.1"
PORT = 5081

expert_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
expert_socket.connect((IP, PORT))

expert_socket.send("expert".encode())
print("connected to server")

root = tk.Tk()
root.title("expert")
root.geometry("800x600")
root.configure(bg="#a2f456")

msg_var = tk.StringVar()

messages_box = tk.Listbox(root, height=30)
messages_box.pack(fill="both", padx=10, pady=10)

messages_entry = tk.Entry(root, textvariable=msg_var)
messages_entry.bind("<Return>", lambda event: send())
messages_entry.pack(fill="both", pady=10, padx=20)

send_button = tk.Button(root, text="send", command=lambda: send())
send_button.pack(fill="both", pady=10, padx=20)


def send():
    expert_socket.send(msg_var.get().encode())
    messages_box.insert(tk.END, f"you: {msg_var.get()}")
    msg_var.set("")
    print("msg sent")


def receive():
    while True:
        msg = expert_socket.recv(1024).decode()
        messages_box.insert(tk.END, f"client: {msg}")


receive_thread = Thread(target=lambda: receive())
receive_thread.start()

root.mainloop()
