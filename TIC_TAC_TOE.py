
# Task 2: Tic-Tac-Toe AI with GUI Interface
# Enhanced version with graphical user interface

import tkinter as tk
from tkinter import messagebox, ttk
import math
import random

class TicTacToeGUI:
    def __init__(self, difficulty="impossible"):
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.human = 'X'
        self.ai = 'O'
        self.difficulty = difficulty
        self.moves_count = 0

        # Create GUI
        self.root = tk.Tk()
        self.root.title("🎮 Tic-Tac-Toe AI - Minimax")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Style
        self.root.configure(bg='#2c3e50')

        # Create widgets
        self.create_widgets()

    def create_widgets(self):
        """Create GUI widgets"""
        # Title
        title_label = tk.Label(
            self.root,
            text="🤖 Tic-Tac-Toe AI",
            font=("Arial", 20, "bold"),
            bg='#2c3e50',
            fg='#ecf0f1'
        )
        title_label.pack(pady=10)

        # Difficulty selection
        diff_frame = tk.Frame(self.root, bg='#2c3e50')
        diff_frame.pack(pady=5)

        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=("Arial", 12),
            bg='#2c3e50',
            fg='#ecf0f1'
        ).pack(side=tk.LEFT, padx=5)

        self.difficulty_var = tk.StringVar(value=self.difficulty)
        difficulty_combo = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["easy", "medium", "hard", "impossible"],
            state="readonly",
            width=10
        )
        difficulty_combo.pack(side=tk.LEFT, padx=5)
        difficulty_combo.bind("<<ComboboxSelected>>", self.change_difficulty)

        # Game board
        self.board_frame = tk.Frame(self.root, bg='#34495e')
        self.board_frame.pack(pady=20)

        self.buttons = []
        for i in range(3):
            row_buttons = []
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    text=' ',
                    font=("Arial", 24, "bold"),
                    width=3,
                    height=1,
                    bg='#ecf0f1',
                    fg='#2c3e50',
                    command=lambda r=i, c=j: self.human_move(r, c)
                )
                btn.grid(row=i, column=j, padx=2, pady=2)
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        # Status label
        self.status_label = tk.Label(
            self.root,
            text="Your turn! (You are X)",
            font=("Arial", 14),
            bg='#2c3e50',
            fg='#3498db'
        )
        self.status_label.pack(pady=10)

        # Control buttons
        control_frame = tk.Frame(self.root, bg='#2c3e50')
        control_frame.pack(pady=10)

        reset_btn = tk.Button(
            control_frame,
            text="🔄 New Game",
            font=("Arial", 12),
            bg='#e74c3c',
            fg='white',
            command=self.reset_game
        )
        reset_btn.pack(side=tk.LEFT, padx=10)

        quit_btn = tk.Button(
            control_frame,
            text="❌ Quit",
            font=("Arial", 12),
            bg='#95a5a6',
            fg='white',
            command=self.root.quit
        )
        quit_btn.pack(side=tk.LEFT, padx=10)

    def change_difficulty(self, event):
        """Change AI difficulty"""
        self.difficulty = self.difficulty_var.get()
        self.status_label.config(text=f"Difficulty: {self.difficulty.upper()}")

    def update_button(self, row, col, player):
        """Update button appearance"""
        self.buttons[row][col].config(
            text=player,
            state='disabled',
            bg='#3498db' if player == self.human else '#e74c3c',
            fg='white'
        )

    def human_move(self, row, col):
        """Handle human player move"""
        if self.board[row][col] != ' ':
            return

        # Make human move
        self.board[row][col] = self.human
        self.update_button(row, col, self.human)
        self.moves_count += 1

        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_over(winner)
            return

        # AI turn
        self.status_label.config(text="🤖 AI is thinking...")
        self.root.after(500, self.ai_move)  # Delay for effect

    def ai_move(self):
        """Handle AI move"""
        ai_row, ai_col = self.find_best_move()
        self.board[ai_row][ai_col] = self.ai
        self.update_button(ai_row, ai_col, self.ai)
        self.moves_count += 1

        # Check for winner
        winner = self.check_winner()
        if winner:
            self.game_over(winner)
            return

        self.status_label.config(text="Your turn! (You are X)")

    def game_over(self, winner):
        """Handle game over"""
        if winner == self.human:
            message = "🎉 Congratulations! You won!"
            self.status_label.config(text="You won!", fg='#27ae60')
        elif winner == self.ai:
            message = "🤖 AI wins! Better luck next time!"
            self.status_label.config(text="AI wins!", fg='#e74c3c')
        else:
            message = "🤝 It's a tie!"
            self.status_label.config(text="It's a tie!", fg='#f39c12')

        # Disable all buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(state='disabled')

        messagebox.showinfo("Game Over", message)

    def reset_game(self):
        """Reset the game"""
        self.board = [[' ' for _ in range(3)] for _ in range(3)]
        self.moves_count = 0

        # Reset buttons
        for i in range(3):
            for j in range(3):
                self.buttons[i][j].config(
                    text=' ',
                    state='normal',
                    bg='#ecf0f1',
                    fg='#2c3e50'
                )

        self.status_label.config(text="Your turn! (You are X)", fg='#3498db')

    # Minimax algorithm methods (same as console version)
    def evaluate(self):
        """Evaluate the board state"""
        # Check rows
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == 
                self.board[row][2] != ' '):
                if self.board[row][0] == self.ai:
                    return 10
                elif self.board[row][0] == self.human:
                    return -10

        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == 
                self.board[2][col] != ' '):
                if self.board[0][col] == self.ai:
                    return 10
                elif self.board[0][col] == self.human:
                    return -10

        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == 
            self.board[2][2] != ' '):
            if self.board[0][0] == self.ai:
                return 10
            elif self.board[0][0] == self.human:
                return -10

        if (self.board[0][2] == self.board[1][1] == 
            self.board[2][0] != ' '):
            if self.board[0][2] == self.ai:
                return 10
            elif self.board[0][2] == self.human:
                return -10

        return 0

    def is_moves_left(self):
        """Check if there are moves left"""
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    return True
        return False

    def minimax(self, depth, is_maximizing, alpha=float('-inf'), beta=float('inf')):
        """Minimax with Alpha-Beta pruning"""
        score = self.evaluate()

        if score == 10:
            return score - depth
        if score == -10:
            return score + depth
        if not self.is_moves_left():
            return 0

        if is_maximizing:
            best = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.ai
                        best = max(best, self.minimax(depth + 1, False, alpha, beta))
                        self.board[i][j] = ' '
                        alpha = max(alpha, best)
                        if beta <= alpha:
                            break
            return best
        else:
            best = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == ' ':
                        self.board[i][j] = self.human
                        best = min(best, self.minimax(depth + 1, True, alpha, beta))
                        self.board[i][j] = ' '
                        beta = min(beta, best)
                        if beta <= alpha:
                            break
            return best

    def find_best_move(self):
        """Find best move based on difficulty"""
        available_moves = []
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    available_moves.append((i, j))

        if self.difficulty == "easy" and random.random() < 0.7:
            return random.choice(available_moves)
        elif self.difficulty == "medium" and random.random() < 0.4:
            return random.choice(available_moves)
        elif self.difficulty == "hard" and random.random() < 0.1:
            return random.choice(available_moves)

        # Use minimax
        best_val = float('-inf')
        best_move = (-1, -1)

        for i in range(3):
            for j in range(3):
                if self.board[i][j] == ' ':
                    self.board[i][j] = self.ai
                    move_val = self.minimax(0, False)
                    self.board[i][j] = ' '

                    if move_val > best_val:
                        best_move = (i, j)
                        best_val = move_val

        return best_move

    def check_winner(self):
        """Check for winner"""
        score = self.evaluate()
        if score == 10:
            return self.ai
        elif score == -10:
            return self.human
        elif not self.is_moves_left():
            return 'tie'
        return None

    def run(self):
        """Start the GUI"""
        self.root.mainloop()

if __name__ == "__main__":
    game = TicTacToeGUI("impossible")
    game.run()
