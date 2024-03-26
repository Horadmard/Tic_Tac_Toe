import socket
import threading

X_turn = True

# X ID = 0, O ID = 1

def handle_client(client, player_name, client2):
    while True:
        try:

            data = client.recv(1024)

            data = list(data)
            game_status = data[2]
            data.pop()
            if player_name == 'X':
                data.append(0)
            else:
                data.append(1)

            if not data:
                print(f"Player {player_name} disconnected.")
                break

            print(f"Received from Player {player_name}: {list(data)}")

            data = bytes(data)
            global X_turn
            if not game_status:
                if (player_name == 'X' and X_turn) or (player_name == 'O' and not X_turn):
                    client.sendall(data)
                    client2.sendall(data)
                    X_turn = not X_turn
                else:
                    pass
            else:
                client.sendall(data)
                client2.sendall(data)
                X_turn = True


        except Exception as e:
            print(f"Error handling Player {player_name}: {str(e)}")
            break

    client.close()


# Setup the server
def setup_server():

    host = '127.0.0.1'
    port = 5555

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen()

    print(f"Server listening on {host}:{port}")

    # Accept two client connections:
    client_X = server.accept()
    # tell client "who you are" first client is X
    msg = 'X'
    msg = bytes(msg, "utf-8")
    client_X[0].sendall(msg)
    print(f"Player 1 connected from {client_X[1]}")

    client_O = server.accept()
    # second client is O
    msg = 'O'
    msg = bytes(msg, "utf-8")
    client_O[0].sendall(msg)
    print(f"Player 2 connected from {client_O[1]}")

    # Start a thread for each client
    threading.Thread(target=handle_client, args=(
        client_X[0], 'X', client_O[0])).start()
    threading.Thread(target=handle_client, args=(
        client_O[0], 'O', client_X[0])).start()


if __name__ == "__main__":
    setup_server()
