"""Tkinter Tic-Tac-Toe with local multiplayer and an unbeatable Minimax AI."""

import tkinter as tk
from tkinter import messagebox


EMPTY = ""
HUMAN = "X"
AI = "O"


class TicTacToeApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Tic-Tac-Toe")
        self.root.resizable(False, False)
        self.mode = tk.StringVar(value="ai")
        self.status = tk.StringVar()
        self.board = [EMPTY] * 9
        self.current_player = HUMAN
        self.game_over = False
        self.buttons: list[tk.Button] = []
        self._build_ui()
        self.new_game()

    def _build_ui(self) -> None:
        container = tk.Frame(self.root, padx=18, pady=18)
        container.pack()

        tk.Label(container, text="Tic-Tac-Toe", font=("Arial", 22, "bold")).pack(pady=(0, 10))
        modes = tk.Frame(container)
        modes.pack(pady=(0, 10))
        tk.Radiobutton(modes, text="Single player (vs AI)", variable=self.mode,
                       value="ai", command=self.new_game).pack(side="left", padx=5)
        tk.Radiobutton(modes, text="Two players", variable=self.mode,
                       value="multi", command=self.new_game).pack(side="left", padx=5)

        board_frame = tk.Frame(container, bd=2, relief="solid")
        board_frame.pack()
        for index in range(9):
            button = tk.Button(
                board_frame, text="", font=("Arial", 26, "bold"), width=4, height=2,
                command=lambda i=index: self.play(i), relief="ridge", bd=1,
            )
            button.grid(row=index // 3, column=index % 3, sticky="nsew")
            self.buttons.append(button)

        tk.Label(container, textvariable=self.status, font=("Arial", 12, "bold")).pack(pady=10)
        tk.Button(container, text="New game", command=self.new_game, font=("Arial", 11)).pack()

    def new_game(self) -> None:
        self.board = [EMPTY] * 9
        self.current_player = HUMAN
        self.game_over = False
        for button in self.buttons:
            button.config(text="", state="normal")
        self._set_status()

    def play(self, index: int) -> None:
        if self.game_over or self.board[index]:
            return
        self._place(index, self.current_player)
        if self._finish_if_needed():
            return

        if self.mode.get() == "ai":
            self.current_player = AI
            self._set_status()
            self.root.after(250, self.ai_turn)
        else:
            self.current_player = AI if self.current_player == HUMAN else HUMAN
            self._set_status()

    def ai_turn(self) -> None:
        if self.game_over:
            return
        move = self.best_move()
        if move is not None:
            self._place(move, AI)
        if not self._finish_if_needed():
            self.current_player = HUMAN
            self._set_status()

    def _place(self, index: int, player: str) -> None:
        self.board[index] = player
        self.buttons[index].config(text=player, disabledforeground="#1d4ed8", state="disabled")

    def _set_status(self) -> None:
        if self.mode.get() == "ai":
            self.status.set("Your turn (X)" if self.current_player == HUMAN else "AI is thinking…")
        else:
            self.status.set(f"Player {self.current_player}'s turn")

    def _finish_if_needed(self) -> bool:
        winner = self.winner(self.board)
        if winner or EMPTY not in self.board:
            self.game_over = True
            for button in self.buttons:
                button.config(state="disabled")
            result = "It's a draw!" if not winner else f"{('AI' if self.mode.get() == 'ai' and winner == AI else 'Player')} {winner} wins!"
            self.status.set(result)
            messagebox.showinfo("Game over", result)
            return True
        return False

    @staticmethod
    def winner(board: list[str]) -> str | None:
        for a, b, c in ((0, 1, 2), (3, 4, 5), (6, 7, 8),
                        (0, 3, 6), (1, 4, 7), (2, 5, 8),
                        (0, 4, 8), (2, 4, 6)):
            if board[a] and board[a] == board[b] == board[c]:
                return board[a]
        return None

    def best_move(self) -> int | None:
        best_score = -float("inf")
        move = None
        for index, value in enumerate(self.board):
            if not value:
                self.board[index] = AI
                score = self.minimax(self.board, False, 0)
                self.board[index] = EMPTY
                if score > best_score:
                    best_score, move = score, index
        return move

    def minimax(self, board: list[str], maximizing: bool, depth: int, max_depth: int = 9) -> int:
        winner = self.winner(board)
        if winner == AI:
            return 10 - depth
        if winner == HUMAN:
            return depth - 10
        if EMPTY not in board or depth >= max_depth:
            return 0

        scores = []
        player = AI if maximizing else HUMAN
        for index, value in enumerate(board):
            if not value:
                board[index] = player
                scores.append(self.minimax(board, not maximizing, depth + 1, max_depth))
                board[index] = EMPTY
        return max(scores) if maximizing else min(scores)


if __name__ == "__main__":
    root = tk.Tk()
    TicTacToeApp(root)
    root.mainloop()
