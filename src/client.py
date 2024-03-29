import socket
from threading import Thread
from tkinter import Tk, Canvas

def update(self, logical_position, player):
    if not self.reset_board:
        if player == 0:
            self.draw_X(logical_position[:2])
            self.board_status[logical_position[0]
                              ][logical_position[1]] = -1
        else:
            self.draw_O(logical_position)
            self.board_status[logical_position[0]][logical_position[1]] = 1

        # Check if game is concluded
        if self.is_gameover():
            self.display_gameover()
    else:
        # Play Again
        self.canvas.delete("all")
        self.play_again()
        self.reset_board = False


def receive_message(sock, game):
    i = 0
    while True:
        try:
            data = sock.recv(1024)
            i += 1
            # the first data sended by server is the name of player
            if i == 1:
                game.player_name = data.decode("utf-8")
                game.window.title(f'Tic-Tac-Toe _ player {game.player_name}')
                continue

            if not data:
                print("Disconnected from the server.")
                break

            data = list(data)
            print("Received from server:", data)

            logical_position = data[:2]
            update(game, logical_position, data[2])

        except Exception as e:
            print(f"Error receiving data: {str(e)}")
            break


def connect_server(game):
    host = '127.0.0.1'
    port = 5555

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    # Start a thread to receive messages from the server
    Thread(target=receive_message, args=(client, game)).start()

    return client


def send_massage(client, message):
    client.sendall(message)


class Tic_Tac_Toe():

    size_of_board = 800
    symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
    symbol_thickness = 30
    symbol_X_color = '#EE4035'
    symbol_O_color = '#0492CF'
    Green_color = '#7BC043'

    def __init__(self):

        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.client = connect_server(self)
        self.canvas = Canvas(
            self.window, width=self.size_of_board, height=self.size_of_board)
        self.canvas.pack()

        # Input from user in form of clicks
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_name = 'X'
        self.board_status = [[0 for i in range(3)] for i in range(3)]

        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False

        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * self.size_of_board / 3,
                                    0, (i + 1) * self.size_of_board / 3, self.size_of_board)

        for i in range(2):
            self.canvas.create_line(0, (i + 1) * self.size_of_board / 3,
                                    self.size_of_board, (i + 1) * self.size_of_board / 3)

    def play_again(self):
        self.initialize_board()
        self.board_status = [[0 for i in range(3)] for i in range(3)]

    def draw_O(self, logical_position):

        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                                outline=self.symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] - self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] + self.symbol_size, width=self.symbol_thickness,
                                fill=self.symbol_X_color)
        self.canvas.create_line(grid_position[0] - self.symbol_size, grid_position[1] + self.symbol_size,
                                grid_position[0] + self.symbol_size, grid_position[1] - self.symbol_size, width=self.symbol_thickness,
                                fill=self.symbol_X_color)

    def display_gameover(self):

        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = self.symbol_X_color
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = self.symbol_O_color
        else:
            self.tie_score += 1
            text = 'Its a tie'
            color = 'gray'

        self.canvas.delete("all")
        self.canvas.create_text(
            self.size_of_board / 2, self.size_of_board / 3, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(self.size_of_board / 2, 5 * self.size_of_board / 8,
                                font="cmr 40 bold", fill=self.Green_color, text=score_text)

        score_text = 'Player 1 (X) : ' + str(self.X_score) + '\n'
        score_text += 'Player 2 (O) : ' + str(self.O_score) + '\n'
        score_text += 'Tie                : ' + str(self.tie_score)
        self.canvas.create_text(self.size_of_board / 2, 3 * self.size_of_board / 4,
                                font="cmr 30 bold", fill=self.Green_color, text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(self.size_of_board / 2, 15 * self.size_of_board / 16, font="cmr 20 bold", fill="gray",
                                text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        grid_position = [
            (self.size_of_board // 3) *
            (logical_position[0]) + self.symbol_size + 50,
            (self.size_of_board // 3) *
            (logical_position[1]) + self.symbol_size + 50
        ]
        return grid_position

    def convert_grid_to_logical_position(self, grid_position):
        ranges = [range(i*(self.size_of_board // 3), (i+1) *
                        (self.size_of_board // 3)) for i in range(3)]
        logical_position = [0, 0]

        for i, coord_range in enumerate(ranges):
            if grid_position[0] in coord_range:
                logical_position[0] = i

            if grid_position[1] in coord_range:
                logical_position[1] = i

        return logical_position

    def is_grid_occupied(self, logical_position):
        if self.board_status[logical_position[0]][logical_position[1]] == 0:
            return False
        else:
            return True

    def is_winner(self, player):

        player = -1 if player == 'X' else 1

        # Three in a row
        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        # Diagonals
        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):

        coord = [(i, j) for i, row in enumerate(self.board_status)
                 for j, value in enumerate(row) if value == 0]
        tie = False
        if len(coord) == 0:
            tie = True

        return tie

    def is_gameover(self):
        # Either someone wins or all grid occupied
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
            self.tie = self.is_tie()

        gameover = self.X_wins or self.O_wins or self.tie

        if self.X_wins:
            print('X wins')
        if self.O_wins:
            print('O wins')
        if self.tie:
            print('Its a tie')

        return gameover

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)
        data = logical_position
        if not self.reset_board:
            data.append(0)
        else:
            data.append(1)
        # send the logical_position to server, decode it or not?
        if not self.is_grid_occupied(logical_position) or self.reset_board:
            send_massage(self.client, bytes(data))


if __name__ == "__main__":
    game_instance = Tic_Tac_Toe()
    game_instance.mainloop()
