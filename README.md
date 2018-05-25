# Mario Party Monte Carlo Simulation
Simulates multiple games of Mario Party, collecting and computing statistics allong the way. 


## How To Run

```python3 Game.py```

Modify player skill values in `Game.py` in the players list in the first value of each tuple. Skill values are based on how often each player wins at a single-player minigame, like a Bowser or DK minigame, and must be between 0-100. This translates directly to multiplayer minigame skill. For example, for the following list `players = [(25, 0), (25, 0), (25, 0), (25, 0)]` each player has an equal chance to win a 4-player minigame, and a 25% chance to win a single-player minigame. 

For another example, consider `players = [(0, 0), (25, 0), (75, 0), (100, 0)]`. Player 1 has a 0% chance of winning, Player 2 has a 12.5% chance of winning (25/(25+75+100)), and so on. (The second value in the tuple is not currently used). 

## TODO

2v2 Minigames, 3v1 Minigames
Items
Shopping Star, Item Star
