"""
othello_gui.py
--------------
Othello AI - Graphical Interface using Tkinter.
Tkinter is built into Python - NO installation required.
Works on Python 3.8, 3.9, 3.10, 3.11, 3.12, 3.13, 3.14+
Works on Windows, Mac, and Linux.

Run:  python main.py play
  OR  python gui/othello_gui.py

Team Othello - ICSI435/535 Artificial Intelligence
University at Albany
"""

import tkinter as tk
import threading
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from game.othello_game import OthelloGame, BLACK, WHITE, EMPTY
from ai.ai_agent import OthelloAI

# ── Layout ────────────────────────────────────────────────────
CELL     = 68
BOARD_PX = CELL * 8
MARGIN   = 28
WIN_W    = BOARD_PX + MARGIN * 2

# ── Colors ────────────────────────────────────────────────────
C_BG         = "#1a1a1a"
C_BOARD      = "#1e6b1e"
C_GRID       = "#145214"
C_BLACK_DISC = "#111111"
C_WHITE_DISC = "#f0f0f0"
C_DOT        = "#4ecb4e"
C_LAST       = "#ffff00"
C_STATUS_BG  = "#0d0d0d"
C_TEXT       = "#ffffff"
C_GREEN_TEXT = "#4ecb4e"
C_AMBER      = "#f0a500"
C_RED        = "#e05050"


class OthelloApp:
    def __init__(self, root, mode="human_vs_ai", depth=4):
        self.root      = root
        self.mode      = mode
        self.depth     = depth
        self.thinking  = False
        self.last_move = None
        self.move_num  = 0

        self.root.title("Othello AI  ·  Team Othello  ·  ICSI435/535")
        self.root.resizable(False, False)
        self.root.configure(bg=C_BG)

        self._init_game()
        self._build_ui()
        self._draw_board()
        self._set_status("Black's turn — click a green dot to place your disc")

        if mode == "ai_vs_ai":
            self.root.after(600, self._ai_turn)

    def _init_game(self):
        self.game     = OthelloGame()
        self.ai_white = OthelloAI(WHITE, depth=self.depth, heuristic="multi")
        self.ai_black = OthelloAI(BLACK, depth=self.depth, heuristic="multi") \
                        if self.mode == "ai_vs_ai" else None

    # ── Build UI ──────────────────────────────────────────────
    def _build_ui(self):
        # Top label
        mode_names = {
            "human_vs_ai":    "Human (Black)  vs  AI (White)",
            "ai_vs_ai":       "AI (Black)  vs  AI (White)",
            "human_vs_human": "Human (Black)  vs  Human (White)",
        }
        top = tk.Frame(self.root, bg=C_BG)
        top.pack(fill="x")
        tk.Label(top,
                 text=f"  OTHELLO AI  ·  {mode_names[self.mode]}  ·  Depth {self.depth}",
                 bg=C_BG, fg=C_GREEN_TEXT,
                 font=("Courier", 11, "bold")).pack(side="left", pady=8)
        tk.Button(top, text="New Game", command=self._reset,
                  bg="#2a6b2a", fg=C_TEXT,
                  font=("Courier", 10), relief="flat",
                  padx=12, pady=3, cursor="hand2"
                  ).pack(side="right", padx=10, pady=6)

        # Canvas
        self.canvas = tk.Canvas(
            self.root,
            width=WIN_W, height=BOARD_PX + MARGIN * 2,
            bg=C_BG, highlightthickness=0
        )
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self._on_click)

        # Status bar
        sf = tk.Frame(self.root, bg=C_STATUS_BG, height=50)
        sf.pack(fill="x")
        sf.pack_propagate(False)
        self.score_var  = tk.StringVar(value="Black: 2    White: 2")
        self.status_var = tk.StringVar(value="")
        tk.Label(sf, textvariable=self.score_var,
                 bg=C_STATUS_BG, fg=C_TEXT,
                 font=("Courier", 14, "bold")).pack(side="left", padx=14, pady=10)
        tk.Label(sf, textvariable=self.status_var,
                 bg=C_STATUS_BG, fg=C_AMBER,
                 font=("Courier", 11)).pack(side="left", padx=6)
        self.nodes_var = tk.StringVar(value="")
        tk.Label(sf, textvariable=self.nodes_var,
                 bg=C_STATUS_BG, fg=C_GREEN_TEXT,
                 font=("Courier", 10)).pack(side="right", padx=14)

        # Node log panel
        lf = tk.Frame(self.root, bg="#0a0a0a")
        lf.pack(fill="x")
        tk.Label(lf, text="  AI Node Counter & Time Log  (Depth · Nodes Explored · Time per Move):",
                 bg="#0a0a0a", fg=C_GREEN_TEXT,
                 font=("Courier", 9, "bold")).pack(anchor="w", padx=8, pady=2)
        self.log = tk.Text(lf, height=6, bg="#0a0a0a", fg="#88ff88",
                           font=("Courier", 9), state="disabled",
                           relief="flat", padx=8, pady=4)
        self.log.pack(fill="x")
        sb = tk.Scrollbar(lf, command=self.log.yview)
        self.log.configure(yscrollcommand=sb.set)

    # ── Draw board ────────────────────────────────────────────
    def _draw_board(self):
        c = self.canvas
        c.delete("all")

        # Board
        c.create_rectangle(
            MARGIN, MARGIN,
            MARGIN + BOARD_PX, MARGIN + BOARD_PX,
            fill=C_BOARD, outline=""
        )

        # Grid
        for i in range(9):
            x = MARGIN + i * CELL
            y = MARGIN + i * CELL
            c.create_line(x, MARGIN, x, MARGIN + BOARD_PX, fill=C_GRID, width=1)
            c.create_line(MARGIN, y, MARGIN + BOARD_PX, y, fill=C_GRID, width=1)

        # Corner markers
        for ri, ci in [(2,2),(2,6),(6,2),(6,6)]:
            px = MARGIN + ci * CELL
            py = MARGIN + ri * CELL
            c.create_oval(px-4, py-4, px+4, py+4, fill=C_GRID, outline="")

        # Last move highlight
        if self.last_move:
            r, col = self.last_move
            x1 = MARGIN + col * CELL + 3
            y1 = MARGIN + r   * CELL + 3
            c.create_rectangle(x1, y1, x1+CELL-6, y1+CELL-6,
                               outline=C_LAST, width=3)

        # Legal move dots (human turns only)
        if not self.game.is_game_over() and not self.thinking:
            p = self.game.current_player
            is_human = (
                (self.mode == "human_vs_ai"    and p == BLACK) or
                 self.mode == "human_vs_human"
            )
            if is_human:
                for r, col in self.game.get_legal_moves():
                    px = MARGIN + col * CELL + CELL // 2
                    py = MARGIN + r   * CELL + CELL // 2
                    r2 = CELL // 6
                    c.create_oval(px-r2, py-r2, px+r2, py+r2,
                                  fill=C_DOT, outline="")

        # Discs
        pad = 5
        for r in range(8):
            for col in range(8):
                val = self.game.board[r][col]
                if val == EMPTY:
                    continue
                x1 = MARGIN + col * CELL + pad
                y1 = MARGIN + r   * CELL + pad
                x2 = x1 + CELL - pad * 2
                y2 = y1 + CELL - pad * 2
                color   = C_BLACK_DISC if val == BLACK else C_WHITE_DISC
                outline = "#2a2a2a"    if val == BLACK else "#cccccc"
                c.create_oval(x1+2, y1+2, x2+2, y2+2,
                              fill="#050505", outline="")
                c.create_oval(x1, y1, x2, y2,
                              fill=color, outline=outline, width=1.5)

        # Game over overlay
        if self.game.is_game_over():
            self._draw_gameover()

    def _draw_gameover(self):
        c      = self.canvas
        winner = self.game.get_winner()
        b, w   = self.game.get_score()
        mid    = MARGIN + BOARD_PX // 2

        if winner == BLACK:
            msg   = f"BLACK WINS!   {b} vs {w}"
            color = "#dddddd"
        elif winner == WHITE:
            msg   = f"WHITE WINS!   {b} vs {w}"
            color = "#ffffff"
        else:
            msg   = f"DRAW!   {b} vs {w}"
            color = C_AMBER

        c.create_rectangle(
            MARGIN + 30, mid - 55,
            MARGIN + BOARD_PX - 30, mid + 55,
            fill="#111111", outline=C_GREEN_TEXT, width=2
        )
        c.create_text(mid, mid - 18, text=msg, fill=color,
                      font=("Courier", 22, "bold"))
        c.create_text(mid, mid + 22,
                      text="Click 'New Game' to play again",
                      fill=C_GREEN_TEXT, font=("Courier", 12))

    # ── Status helpers ────────────────────────────────────────
    def _set_status(self, msg):
        b, w = self.game.get_score()
        self.score_var.set(f"Black: {b}    White: {w}")
        self.status_var.set(msg)

    def _log(self, player, nodes, elapsed, move):
        self.move_num += 1
        line = (f"Move {self.move_num:>3}  {player:<8}  "
                f"Nodes: {nodes:>9,}  "
                f"Time: {elapsed:>6.3f}s  "
                f"Move: ({move[0]},{move[1]})\n")
        self.log.configure(state="normal")
        self.log.insert("end", line)
        self.log.see("end")
        self.log.configure(state="disabled")
        self.nodes_var.set(f"Last AI:  {nodes:,} nodes  ·  {elapsed:.3f}s")

    # ── Human click ───────────────────────────────────────────
    def _on_click(self, event):
        if self.thinking or self.game.is_game_over():
            return

        p = self.game.current_player
        is_human = (
            (self.mode == "human_vs_ai"    and p == BLACK) or
             self.mode == "human_vs_human"
        )
        if not is_human:
            return

        col = (event.x - MARGIN) // CELL
        row = (event.y - MARGIN) // CELL
        if not (0 <= row < 8 and 0 <= col < 8):
            return

        if (row, col) not in self.game.get_legal_moves():
            self._set_status("Invalid move!  Click one of the green dots.")
            return

        self.game.apply_move(row, col)
        self.last_move = (row, col)
        self._draw_board()

        if self.game.is_game_over():
            self._finish()
            return

        if self.mode == "human_vs_ai":
            self._set_status("White's turn  ·  AI is thinking...")
            self.root.after(80, self._ai_turn)
        else:
            name = "Black" if self.game.current_player == BLACK else "White"
            self._set_status(f"{name}'s turn  ·  click a green dot")

    # ── AI turn ───────────────────────────────────────────────
    def _ai_turn(self):
        if self.game.is_game_over():
            return

        p  = self.game.current_player
        ai = None
        if self.mode == "human_vs_ai" and p == WHITE:
            ai, name = self.ai_white, "White"
        elif self.mode == "ai_vs_ai":
            ai   = self.ai_black if p == BLACK else self.ai_white
            name = "Black" if p == BLACK else "White"

        if ai is None:
            return

        self.thinking = True
        self._set_status(f"{name}'s turn  ·  AI is thinking...")
        self._draw_board()

        board_copy = self.game.board.copy()
        result     = [None]

        def run():
            move = ai.get_best_move(board_copy)
            result[0] = (move, ai.nodes_explored, ai.last_move_time)

        t = threading.Thread(target=run, daemon=True)
        t.start()
        self._poll(t, result, name)

    def _poll(self, thread, result, name):
        if thread.is_alive():
            self.root.after(40, lambda: self._poll(thread, result, name))
            return

        self.thinking = False
        move, nodes, elapsed = result[0]

        if move and not self.game.is_game_over():
            self.game.apply_move(*move)
            self.last_move = move
            self._log(name, nodes, elapsed, move)

        self._draw_board()

        if self.game.is_game_over():
            self._finish()
            return

        p = self.game.current_player
        if self.mode == "ai_vs_ai":
            n = "Black" if p == BLACK else "White"
            self._set_status(f"{n}'s turn  ·  AI is thinking...")
            self.root.after(350, self._ai_turn)
        elif self.mode == "human_vs_ai":
            self._set_status("Black's turn  ·  click a green dot to place your disc")

    # ── Game over ─────────────────────────────────────────────
    def _finish(self):
        winner = self.game.get_winner()
        b, w   = self.game.get_score()
        msg = ("Black Wins!" if winner == BLACK else
               "White Wins!" if winner == WHITE else "Draw!")
        self._set_status(f"Game Over  ·  {msg}  ({b} - {w})")
        self._draw_board()

    # ── Reset ─────────────────────────────────────────────────
    def _reset(self):
        self.thinking  = False
        self.last_move = None
        self.move_num  = 0
        self._init_game()
        self.log.configure(state="normal")
        self.log.delete("1.0", "end")
        self.log.configure(state="disabled")
        self.nodes_var.set("")
        self._draw_board()
        self._set_status("Black's turn  ·  click a green dot to place your disc")
        if self.mode == "ai_vs_ai":
            self.root.after(600, self._ai_turn)


# ── Menu ──────────────────────────────────────────────────────
class MenuApp:
    def __init__(self, root):
        self.root  = root
        self.depth = tk.IntVar(value=4)
        root.title("Othello AI  ·  Select Game Mode")
        root.configure(bg=C_BG)
        root.resizable(False, False)

        tk.Label(root, text="OTHELLO AI",
                 bg=C_BG, fg=C_GREEN_TEXT,
                 font=("Courier", 38, "bold")).pack(pady=(30, 4))

        tk.Label(root,
                 text="Minimax  ·  Alpha-Beta Pruning  ·  Multi-Factor Heuristics",
                 bg=C_BG, fg="#777777",
                 font=("Courier", 11)).pack(pady=(0, 2))

        tk.Label(root,
                 text="Team Othello  ·  ICSI435/535  ·  University at Albany",
                 bg=C_BG, fg="#444444",
                 font=("Courier", 10)).pack(pady=(0, 26))

        # Depth
        df = tk.Frame(root, bg=C_BG)
        df.pack(pady=(0, 18))
        tk.Label(df, text="AI Search Depth:",
                 bg=C_BG, fg=C_TEXT,
                 font=("Courier", 12)).pack(side="left", padx=8)
        tk.Scale(df, from_=1, to=7, orient="horizontal",
                 variable=self.depth, length=200,
                 bg=C_BG, fg=C_TEXT, troughcolor="#1a5c1a",
                 highlightthickness=0,
                 font=("Courier", 10)).pack(side="left")
        tk.Label(df, text="(3=fast · 5=strong · 7=slow)",
                 bg=C_BG, fg="#555555",
                 font=("Courier", 10)).pack(side="left", padx=10)

        # Buttons
        for label, mode, bg1, bg2 in [
            ("  ▶   Human vs AI   (You play Black)",    "human_vs_ai",    "#1a5c1a", "#246024"),
            ("  ▶   AI vs AI      (Watch both AIs)",    "ai_vs_ai",       "#1a3d5c", "#24526a"),
            ("  ▶   Human vs Human (Two players)",      "human_vs_human", "#3d1a5c", "#52246a"),
        ]:
            tk.Button(root, text=label,
                      font=("Courier", 14, "bold"),
                      bg=bg1, fg=C_TEXT,
                      activebackground=bg2, activeforeground=C_TEXT,
                      relief="flat", padx=20, pady=13,
                      width=36, cursor="hand2",
                      command=lambda m=mode: self._launch(m)
                      ).pack(pady=5)

        tk.Label(root,
                 text="\nDepth 4 is recommended for real-time play\n"
                      "Higher depth = smarter AI but slower moves\n",
                 bg=C_BG, fg="#444444",
                 font=("Courier", 9)).pack(pady=4)

    def _launch(self, mode):
        win = tk.Toplevel(self.root)
        OthelloApp(win, mode=mode, depth=self.depth.get())
        win.focus_force()


# ── Entry points ──────────────────────────────────────────────
def run_menu():
    root = tk.Tk()
    MenuApp(root)
    root.mainloop()


def run_game(mode="human_vs_ai", depth=4):
    root = tk.Tk()
    OthelloApp(root, mode=mode, depth=depth)
    root.mainloop()


if __name__ == "__main__":
    run_menu()
