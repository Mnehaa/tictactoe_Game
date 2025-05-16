import tkinter as tk #Used to create GUI windows, buttons, etc.
from tkinter import messagebox, simpledialog #Shows pop-up messages & Used to ask the user a question in a pop-up
import math #Used for infinity (math.inf) in AI calculations.

class TicTacToe:
    def __init__(self, root):
        self.root = root #The main window of the app (Tkinter's GUI window).
        self.root.title("Tic-Tac-Toe: Choose Mode")
        self.mode = simpledialog.askstring("Game Mode", "Choose mode: 'AI' or '2P'").strip().upper()

        self.board = [['.' for _ in range(3)] for _ in range(3)] #empty grids are created
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.current_player = 'X'
        self.create_board()

    def create_board(self):
        for r in range(3):
            for c in range(3):
                btn = tk.Button(self.root, text="", font=('Arial', 32), width=5, height=2,
                                command=lambda r=r, c=c: self.player_move(r, c)) #For each cell, a Tkinter button is created.
                btn.grid(row=r, column=c)
                self.buttons[r][c] = btn

    def player_move(self, r, c):
        if self.board[r][c] == '.':
            self.board[r][c] = self.current_player
            self.buttons[r][c].config(text=self.current_player, state='disabled')

            if self.check_game_over():
                return

            if self.mode == 'AI' and self.current_player == 'X':
                self.current_player = 'O'
                self.root.after(500, self.ai_move) #executes after 5s
            elif self.mode == '2P':
                self.current_player = 'O' if self.current_player == 'X' else 'X'

    def ai_move(self):
        move = self.best_move()
        if move:
            r, c = move
            self.board[r][c] = 'O'
            self.buttons[r][c].config(text='O', state='disabled')
        self.check_game_over()
        self.current_player = 'X'

    def check_game_over(self):
        result = self.check_win()
        if result:
            if result == 'X':
                messagebox.showinfo("Game Over", "Player X Wins! 🎉")
            elif result == 'O':
                if self.mode == 'AI':
                    messagebox.showinfo("Game Over", "Abhinav (AI) Wins! 🤖")
                else:
                    messagebox.showinfo("Game Over", "Player O Wins! 🎉")
            else:
                messagebox.showinfo("Game Over", "It's a Tie!")
            self.reset_board()
            return True
        return False

    def check_win(self):
        b = self.board
        for i in range(3):
            if b[i][0] == b[i][1] == b[i][2] != '.':
                return b[i][0]
            if b[0][i] == b[1][i] == b[2][i] != '.':
                return b[0][i]
        if b[0][0] == b[1][1] == b[2][2] != '.':
            return b[0][0]
        if b[0][2] == b[1][1] == b[2][0] != '.':
            return b[0][2]
        for row in b:
            if '.' in row:
                return None
        return 'Tie'

    def minimax(self, board, depth, is_max):
        result = self.check_win()
        if result == 'O':
            return 1
        if result == 'X':
            return -1
        if result == 'Tie':
            return 0

        if is_max:
            best = -math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == '.':
                        board[r][c] = 'O'
                        best = max(best, self.minimax(board, depth+1, False))
                        board[r][c] = '.'
            return best
        else:
            best = math.inf
            for r in range(3):
                for c in range(3):
                    if board[r][c] == '.':
                        board[r][c] = 'X'
                        best = min(best, self.minimax(board, depth+1, True))
                        board[r][c] = '.'
            return best

    def best_move(self):
        best_score = -math.inf
        move = None
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == '.':
                    self.board[r][c] = 'O'
                    score = self.minimax(self.board, 0, False)
                    self.board[r][c] = '.'
                    if score > best_score:
                        best_score = score
                        move = (r, c)
        return move

    def reset_board(self):
        self.board = [['.' for _ in range(3)] for _ in range(3)]
        for r in range(3):
            for c in range(3):
                self.buttons[r][c].config(text='', state='normal')
        self.current_player = 'X'


# Run the game
if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
