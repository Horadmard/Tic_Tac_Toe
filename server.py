import socket 
import threading
 
# Function to handle each client connection 
def handle_client(client, player, client2): 
    global current_player_turn
    while True: 
        try: 
            # data = client.recv(1024).decode('utf-8') 
            data = client.recv(1024)
            if not data: 
                print(f"Player {player} disconnected.") 
                break 

            print(f"Received from Player {player}: {list(data)}")
            
            client.sendall(data)
            client2.sendall(data)

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
    player1, addr1 = server.accept() 
    print(f"Player 1 connected from {addr1}") 
 
    player2, addr2 = server.accept() 
    print(f"Player 2 connected from {addr2}") 
 
    # Start a thread for each client 
    threading.Thread(target=handle_client, args=(player1, 1, player2)).start() 
    threading.Thread(target=handle_client, args=(player2, 2, player1)).start() 
 
if __name__ == "__main__":
    turn = False
    setup_server()