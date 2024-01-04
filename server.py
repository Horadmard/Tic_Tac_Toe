import socket 
import threading

player_X_turns = True

# Function to handle each client connection 
def handle_client(client, player, client2): 
    while True: 
        try: 
            # data = client.recv(1024).decode('utf-8') 
            data = client.recv(1024)
            if not data: 
                print(f"Player {player} disconnected.") 
                break 

            print(f"Received from Player {player}: {list(data)}")
            if (player == 'x' and player_X_turns) or (player == 'O' and not player_X_turns):
                client.sendall(data)
                client2.sendall(data)
                player_X_turns = not player_X_turns


                
            
        except Exception as e: 
            print(f"Error handling Player {player}: {str(e)}") 
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
 
    # Accept two client connections 
    # player1, addr1 = server.accept() 
    client_X = server.accept()
    print(f"Player 1 connected from {client_X[1]}") 
 
    # player2, addr2 = server.accept()
    client_O = server.accept() 
    print(f"Player 2 connected from {client_O[1]}")
 
    # Start a thread for each client 
    threading.Thread(target=handle_client, args=(client_X[0], 'X', client_O[0])).start()
    threading.Thread(target=handle_client, args=(client_O[0], 'O', client_X[0])).start() 
 
if __name__ == "__main__":
    setup_server()