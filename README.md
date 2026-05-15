# Othello AI — Minimax, Alpha-Beta Pruning & Multi-Factor Heuristics

**ICSI435/535 — Artificial Intelligence | University at Albany**  
**Team Othello:** Nishitha Pushpa Karan · Shreya Amagowni · Jason Zheng

---

## What This Is

A fully playable Othello AI built using classical adversarial search.  
The AI uses **Minimax + Alpha-Beta Pruning + a 5-factor phase-aware heuristic** to play strategically in real time.  
The GUI is built with **Tkinter**, which is bundled with Python — no extra GUI install needed.

---

## How to Run

## Option 1 — Recommended: Using a Virtual Environment
```
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 main.py play
```

## Option 2 — Run Without a Virtual Environment

### 1. Install dependencies
```
pip install -r requirements.txt
```
Only `numpy` and `matplotlib` are required. Tkinter is built into Python (no install needed).

### 2. Play the game (GUI window)
```
python main.py play
```
Select Human vs AI, AI vs AI, or Human vs Human from the menu.

### 3. Watch AI vs AI in terminal
```
python main.py ai
```

### 4. Run all experiments (regenerates graphs in results/)
```
python main.py experiments
```
This takes roughly 10–20 minutes and saves 5 PNG graphs to the `results/` folder.  
Pre-generated results are already included in `results/` for reference.

---

## Project Structure

```
Othello_v1/
├── main.py                    ← Entry point (play / ai / experiments)
├── requirements.txt           ← pip install -r requirements.txt
├── game/
│   └── othello_game.py        ← Board, legal moves, disc flipping, game rules
├── ai/
│   ├── heuristics.py          ← All 5 heuristic factors + phase-aware weights
│   └── ai_agent.py            ← Minimax + Alpha-Beta + node counter + timer
├── gui/
│   └── othello_gui.py         ← Tkinter GUI — click to play
├── experiments/
│   └── experiments.py         ← All 5 heuristic comparison experiments
└── results/                   ← Pre-generated experiment graphs (PNG)
```

---

## The 5 Heuristic Factors

| Factor | What it measures |
|--------|------------------|
| Coin Parity | Disc count difference |
| Mobility | Legal moves available |
| Corner Control | Corners captured (never flippable) |
| Positional Weights | 8×8 strategic value matrix |
| Stability | Discs that can never be flipped |

**Phase-aware weighting** shifts the importance of each factor based on game stage:
- Early game → mobility first  
- Mid game → corners dominate  
- End game → disc count decisive

---

## Notes

- **Iterative deepening** was considered but not implemented; fixed-depth search with move ordering achieves comparable pruning efficiency in practice.
- The experiments module includes a **pure Minimax** function (no pruning) for a fair side-by-side node count comparison with Alpha-Beta.

---

## References

- Knuth & Moore (1975) — Alpha-Beta Pruning theory  
- Rosenbloom (1982) — IAGO world-championship heuristics  
- Sannidhanam & Annamalai — An Analysis of Heuristics in Othello  
- Roodaki — Minimax-Powered-Othello-Game (GitHub) — game engine reference
