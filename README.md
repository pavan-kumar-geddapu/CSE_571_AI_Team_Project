# Autonomous Pacman: AI-Powered Self-Learning Maze Navigator

## CSE 571 Artificial Intelligence
Created an AI-based Pacman game utilizing search algorithms and reinforcement learning, enabling the agent to autonomously learn from its environment and find paths in complex mazes

## Topic: Bi-directional Search

All changes to the code were done in search.py and searchAgent.py.

### Script

environmentCreationScript.py has code to create random layouts, run algorithms, capture results and compare.
Run results were stored in results directory. It contains three csv files for three problem types (position search problem, corners problem, food search problem).

you can run it using command:
```bash
python environmentCreationScript.py
```

### Abbreviations
bfs = breadthFirstSearch

dfs = depthFirstSearch

astar = aStarSearch

ucs = uniformCostSearch

bds = biDirectionalSearch

hbds = heuristicBiDirectionalSearch

### Individual Run commands
These are similar to individual project commands.

Example command for bi-directional search.
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=bds
```

Example command for heuristic bi-directional search.
```bash
python pacman.py -l mediumMaze -p SearchAgent -a fn=hbds
```



