import socket
from threading import Thread

PORT = 5081
is_client_connected = False
is_expert_connected = False


def forward_msg(first_socket, second_socket):
    while True:
        msg = first_socket.recv(4096)
        second_socket.send(msg)


def main():
    global is_client_connected, is_expert_connected
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", PORT))
    server_socket.listen()
    print("Listening...")

    while not is_expert_connected or not is_client_connected:
        tmp_socket, tmp_address = server_socket.accept()
        sock_name = tmp_socket.recv(1024).decode()

        if sock_name == "client":
            client_socket, client_address = tmp_socket, tmp_address
            is_client_connected = True
            print("client connected!")

        elif sock_name == "expert":
            expert_socket, expert_address = tmp_socket, tmp_address
            is_expert_connected = True
            print("expert connected!")

    client_to_expert_thread = Thread(target=lambda: forward_msg(client_socket, expert_socket))
    client_to_expert_thread.start()

    forward_msg(expert_socket, client_socket)  # NOQA


if __name__ == "__main__":
    main()
