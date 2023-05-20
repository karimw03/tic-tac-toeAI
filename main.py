import tkinter as tk
from tkinter import messagebox
import random

# define constants
EMPTY = "-"
PLAYER_X = "X"
PLAYER_O = "O"
TIE = "Tie"

# define the game board
board = [
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY],
    [EMPTY, EMPTY, EMPTY]
]

# define the minimax algorithm function
def minimax(board, depth, is_maximizing):
    # check if the game is over or if it's reached the maximum depth
    if check_winner(board):
        if check_winner(board) == PLAYER_X:
            return -1
        elif check_winner(board) == PLAYER_O:
            return 1
        else:
            return 0
    if depth == 0:
        return 0

    # evaluate all possible moves
    if is_maximizing:
        best_score = -float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_O
                    score = minimax(board, depth-1, False)
                    board[i][j] = EMPTY
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(3):
            for j in range(3):
                if board[i][j] == EMPTY:
                    board[i][j] = PLAYER_X
                    score = minimax(board, depth-1, True)
                    board[i][j] = EMPTY
                    best_score = min(score, best_score)
        return best_score

# define a function to get the AI's move
def get_ai_move(board):
    best_score = -float("inf")
    best_move = None
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                board[i][j] = PLAYER_O
                score = minimax(board, 5, False)
                board[i][j] = EMPTY
                if score > best_score:
                    best_score = score
                    best_move = (i, j)
    return best_move

# define a function to check for a winner or a tie
def check_winner(board):
    # check for horizontal win
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != EMPTY:
            return board[i][0]
    # check for vertical win
    for i in range(3):
        if board[0][i] == board[1][i] == board[2][i] != EMPTY:
            return board[0][i]
    # check for diagonal win
    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]
    # check for tie
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                return None
    return TIE

# define a function to update the game board
def update_board(button, player):
    row, col = button.grid_info()["row"], button.grid_info()["column"]
    button.config(text=player)
    board[row][col] = player

# define the main game
def play_game():
    # create the Tkinter window
    window = tk.Tk()
    window.title("Tic-Tac-Toe")
    window.geometry("600x620")

    # create the game board buttons
    buttons = []
    for i in range(3):
        row = []
        for j in range(3):
            button = tk.Button(window, text="", font=("Arial", 20), height=5, width=12)
            button.grid(row=i, column=j, sticky="nsew")
            button.config(command=lambda button=button: on_button_click(button))
            row.append(button)
        buttons.append(row)

    # define the function to restart the game
    def restart_game():
        global board
        nonlocal buttons
        board = [[EMPTY for i in range(3)] for j in range(3)]
        for i in range(3):
            for j in range(3):
                buttons[i][j]["text"] = ""

    # create the Restart button
    restart_button = tk.Button(window, text="Restart", font=("Arial", 16), height=2, width=10, command=restart_game)
    restart_button.grid(row=4, column=1, columnspan=2, sticky="nsew")

    # define the function to handle button clicks
    def on_button_click(button):
        if check_winner(board) or check_winner(board) == TIE:
            return
        if button["text"] == "":
            update_board(button, PLAYER_X)
            if check_winner(board) == None:
                ai_row, ai_col = get_ai_move(board)
                update_board(buttons[ai_row][ai_col], PLAYER_O)
        if check_winner(board) or check_winner(board) == TIE:
            winner = check_winner(board)
            if winner == TIE:
                result = "It's a tie!"
            else:
                result = f"{winner} wins!"
            messagebox.showinfo("Game Over", result)

    # start the game loop
    window.mainloop()

# start the game
play_game()




