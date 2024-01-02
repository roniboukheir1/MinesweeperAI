# Minesweeper AI

## Introduction

Minesweeper AI is a sophisticated implementation of the classic Minesweeper game, enhanced with an artificial intelligence that can assist in making moves. The game has been developed in Python and utilizes the Pygame library for rendering the game's graphical user interface.

## Features

- Classic Minesweeper gameplay with customizable board sizes and mine counts.
- An AI assistant that can suggest safe moves or make random moves when no safe move is apparent.
- Visual and interactive GUI built with Pygame.
- Reset functionality to start a new game at any point.

## Installation

To run Minesweeper AI on your machine, follow these steps:

1. Ensure you have Python 3. installed on your system. You can download Python [here](https://www.python.org/downloads/).

2. Clone the repository to your local machine: `https://github.com/roniboukheir1/MinesweeperAI.git`
   
3. Navigate to the cloned repository's directory.

4. Install the required dependencies: `pip3 install pygame`

5. Run the game: `python MinesweeperGame.py`

## Usage

- Left-click on a cell to uncover it.
- Right-click to place a flag on a cell you suspect contains a mine.
- Click the "AI Move" button to let the AI make a move.
- Click the "Reset" button to start a new game.

## How it Works

### Minesweeper Class

- Initializes the game with a specified grid size and number of mines.
- Randomly places mines on the grid.
- Calculates the number of adjacent mines for each cell.

### MinesweeperAI Class

- Keeps track of safe moves, mines, and other game knowledge.
- Analyzes the game state to suggest the next move.
- Can make a random move if no safe move is identified.

### Pygame Interface

- Renders the game board and responds to user interactions.
- Displays flags, mines, and numbers indicating the count of adjacent mines.
- Provides buttons for AI assistance and game reset.

## Contributing

We welcome contributions to Minesweeper AI. If you have suggestions or bug reports, please open an issue. If you'd like to contribute to the codebase, please open a pull request.

---

Enjoy playing Minesweeper AI and testing your skills against the AI assistant!


