# Othello AI — Minimax, Alpha-Beta Pruning & Multi-Factor Heuristics

**ICSI435/535 — Artificial Intelligence | University at Albany**  
**Team Othello:** Nishitha Pushpa Karan · Shreya Amagowni · Jason Zheng

---

## What This Is

A fully playable Othello AI built using classical adversarial search.  
The AI uses **Minimax + Alpha-Beta Pruning + a 5-factor phase-aware heuristic** to play strategically in real time.

---

## How to Run

### 1. Install dependencies
```
python -m pip install pygame numpy matplotlib pandas
```

### 2. Play the game (Pygame window)
```
python main.py play
```
Select Human vs AI, AI vs AI, or Human vs Human from the menu.

### 3. Watch AI vs AI in terminal
```
python main.py ai
```

### 4. Run all experiments (generates graphs)
```
python main.py experiments
```

---

## Project Structure

```
othello_final/
├── main.py                    ← Entry point
├── requirements.txt           ← pip install -r requirements.txt
├── game/
│   └── othello_game.py        ← Board, legal moves, disc flipping, game rules
├── ai/
│   ├── heuristics.py          ← All 5 heuristic factors + phase-aware weights
│   └── ai_agent.py            ← Minimax + Alpha-Beta + node counter + timer
├── gui/
│   └── othello_gui.py         ← Pygame GUI — click to play
└── experiments/
    └── experiments.py         ← All 5 heuristic comparison experiments
```

---

## The 5 Heuristic Factors

| Factor | What it measures |
|--------|-----------------|
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

## References

- Knuth & Moore (1975) — Alpha-Beta Pruning theory  
- Rosenbloom (1982) — IAGO world-championship heuristics  
- Sannidhanam & Annamalai — An Analysis of Heuristics in Othello  
- Roodaki — Minimax-Powered-Othello-Game (GitHub) — game engine base
