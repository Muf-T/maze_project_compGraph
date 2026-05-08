# Maze Builder & Runner

A Python-based graphical application that uses **PyOpenGL** and **Pygame** to generate a random "proper" maze and solve it using automated backtracking.

## Features

- **Dynamic Generation:** Watch the "mouse" eat through walls in real-time.
- **Proper Maze Logic:** Every cell is guaranteed to be reachable via a unique path.
- **Automated Solver:** A backtracking algorithm finds the path from the North entrance to the South exit.
- **Challenge Mode:** Includes a 1-in-20 chance of creating cycles, making the maze non-linear and more difficult to solve.

## How it Works

### 1. Data Structure

The maze is represented using two 2D arrays as per the assignment requirements:

- `northWall[R][C]`: Tracks horizontal walls.
- `eastWall[R][C]`: Tracks vertical walls.
- A "phantom row" is used to manage the bottom boundary of the maze.

### 2. Maze Generation (The "Mouse")

The project implements a **Depth-First Search (DFS)** algorithm.

- An invisible "mouse" starts at a random cell and moves to unvisited neighbors, "eating" (removing) the wall between them.
- If the mouse reaches a dead end, it uses a **Stack** to backtrack to the last cell with unvisited neighbors.
- This ensures that all $R \times C$ cells are connected.

### 3. Solving Algorithm

The solver uses a **Backtracking** approach:

- **Red Dots:** Represent the current path the solver is exploring.
- **Blue Dots:** Represent "dead ends" that the solver has visited and discarded after backtracking.

## Requirements

- Python 3.x
- Pygame
- PyOpenGL

## How to Run

```bash
python main.py
```

[![Watch the Video](https://cdn.loom.com/sessions/thumbnails/d052626e59764e45b2268d17e86c5f25-with-play.gif)](https://www.loom.com/share/d052626e59764e45b2268d17e86c5f25)
