# TetrisAI

A Tetris clone written from scratch in Python with pygame, and an AI that learns to play it. The AI
scores every possible placement of the current piece and picks the best one; the scoring function
is either a hand-tuned heuristic or a small neural network whose weights are evolved with a genetic
algorithm.

Project for the *AI for Computer Games* course (November 2024 – January 2025).

## How the AI plays

1. For the current piece, the environment enumerates every reachable final position (each rotation
   and column) and computes the path of moves to get there.
2. Each candidate board is described by features: the height of every column, the number of holes,
   the height difference and the average height, plus the next piece.
3. A scoring function rates each candidate and the piece is moved to the best one:
   - **Heuristic agent:** a weighted sum of holes, heights and points.
   - **Evolved agent:** a feed-forward network maps the features to a score.

## Genetic algorithm

The network weights are the chromosome. Each generation:

- every individual plays a full game in its own process (12 processes in parallel);
- fitness is the game score penalised by average height and holes, so the AI learns to keep the
  board clean as well as to score;
- parents are chosen by fitness-proportional selection, combined by uniform crossover and mutated
  with Gaussian noise;
- the best individual so far is carried over unchanged (elitism) and saved to disk.

Trained weights are stored in [`Models/`](Models/). The repository also contains an experimental
Deep Q-Learning agent with a CNN (`src/AI/model.py`).

## Getting started

```bash
git clone https://github.com/manuel48265/TetrisAI.git
cd TetrisAI
pip install pygame numpy tensorflow aenum pytest
PYTHONPATH=. python -m src.test_game
```

The program asks for a mode:

| Mode | What it does |
|---|---|
| 1 | Play manually |
| 2 | Watch the heuristic AI play |
| 3 | Run the heuristic AI without graphics |
| 4 | Train the genetic algorithm |
| 5 | Watch the best evolved model play |

Run the tests:

```bash
PYTHONPATH=. pytest test/test*.py
```

The test files are named `testX.py`, so they are passed explicitly; pytest does not collect them on
its own.

## Repository structure

```text
src/
├── board.py, piece.py, game.py     # game logic
├── UI.py, controler.py             # pygame interface and input
├── utils/                          # piece shapes, rotations, random bag, game timer
└── AI/
    ├── tetrisEnviroment.py         # placements, board features, heuristic and model scoring
    ├── GeneticModels.py            # genetic algorithm
    └── model.py, preprocessing.py  # experimental CNN / Deep Q-Learning agent
test/                               # pytest suite for the board, pieces, timer and model
Models/                             # evolved network weights
```
