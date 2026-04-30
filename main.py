"""
main.py
-------
Entry point for Othello AI.

Run modes:
  python main.py play          -- Opens game window (Tkinter GUI - no install needed)
  python main.py ai            -- AI vs AI in terminal
  python main.py experiments   -- Run all heuristic experiments

Requirements: pip install numpy matplotlib pandas
GUI uses Tkinter which is built into Python - no extra install needed.

Team Othello - ICSI435/535 Artificial Intelligence
University at Albany
"""

import sys

def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "play"

    if mode == "play":
        print("Opening Othello AI game window...")
        print("Tkinter GUI - no extra installation required.")
        from gui.othello_gui import run_menu
        run_menu()

    elif mode == "ai":
        print("Running AI vs AI demo in terminal...")
        print("(Watch nodes and time printed after every move)\n")
        from game.othello_game import OthelloGame, BLACK, WHITE
        from ai.ai_agent import OthelloAI

        game  = OthelloGame()
        black = OthelloAI(BLACK, depth=4, heuristic="multi")
        white = OthelloAI(WHITE, depth=4, heuristic="coin_parity")

        print("Black = Multi-factor heuristic (our AI)")
        print("White = Disc-count only (baseline)")
        print("="*55)

        move_num = 0
        while not game.is_game_over():
            move_num += 1
            p  = game.current_player
            ai = black if p == BLACK else white
            move = ai.get_best_move(game.board)
            if move:
                game.apply_move(*move)
                name = "Black" if p == BLACK else "White"
                print(f"\nMove {move_num:>3} ({name}) → {move}")
                ai.print_stats()
                print(game)

        b, w    = game.get_score()
        winner  = game.get_winner()
        print(f"\n{'='*55}")
        print(f"GAME OVER  |  Black: {b}  White: {w}")
        print(f"Winner: {'Black (Multi-factor)' if winner==BLACK else 'White (Disc-count)' if winner==WHITE else 'Draw'}")

    elif mode == "experiments":
        print("Running all heuristic experiments...")
        print("This will take 10-20 minutes.\n")
        from experiments.experiments import (
            experiment_node_count,
            experiment_heuristic_comparison,
            experiment_phase_aware,
            experiment_ablation,
            experiment_depth_vs_winrate,
        )
        experiment_node_count()
        experiment_heuristic_comparison()
        experiment_phase_aware()
        experiment_ablation()
        experiment_depth_vs_winrate()
        print("\nAll done! Check the results/ folder for graphs.")

    else:
        print(f"Unknown mode: {mode}")
        print("Usage: python main.py [play | ai | experiments]")

if __name__ == "__main__":
    main()
