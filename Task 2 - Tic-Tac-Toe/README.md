# Task 2 — Tic-Tac-Toe AI

A Tkinter-based Tic-Tac-Toe game with an unbeatable AI powered by the **Minimax algorithm**.

## Features

- Single player mode vs unbeatable Minimax AI
- Two player local multiplayer mode
- Clean Tkinter UI with game status display
- New game reset button
- Depth-bounded Minimax (CWE-400 safe)

## Stack

| Layer | Tech |
|-------|------|
| UI | Python Tkinter |
| AI | Minimax Algorithm |
| Language | Python 3 |

## Run

```bash
python tic_tac_toe.py
```

## Project Structure

```
Task 2 - Tic-Tac-Toe/
└── tic_tac_toe.py    # Game logic + UI + Minimax AI
```

## How It Works

1. Human always plays as **X**, AI plays as **O**
2. On each AI turn, Minimax explores all possible moves up to depth 9
3. AI picks the move with the highest score — making it unbeatable
4. A draw is the best outcome a human can achieve against the AI
