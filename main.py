import utils
import matplotlib.pyplot as plt
from GameStat import GameStat
from Game import Game

def win_pct_by_turn():
    n = 10000
    minigame_win_pcts = []
    win_pcts = []
    for i in range(0, 4):
        players = [(100, 0), (100, 0), (100, 0), (100, 0)]    
        players[i] = (0, 0)
        minigame_win_pcts.append([])
        win_pcts.append([])
        for skill in range(0, 101):
            players[i] = (skill, 0)
            minigame_win_pcts[i].append(utils.players_win_pct_4way(players)[i])
            win_pcts[i].append(trial(players, n)[i])
        for j in range(0, 4):
            if j == i: continue
            for skill in range(0, 101):
                players[j] = (100-skill, 0)
                minigame_win_pcts[i].append(utils.players_win_pct_4way(players)[i])
                win_pcts[i].append(trial(players, n)[i])
    print("done")

def plot(minigame_win_pcts, win_pcts):
    for i in range(0, len(minigame_win_pcts)):
        plt.plot(minigame_win_pcts[i], win_pcts[i])
        plt.legend(['First', 'Second', 'Third', 'Fourth'])
    plt.title("Percent of Games Won Based on Minigame Win Percent and Turn Order")
    plt.xlabel("4-player Minigame Win Percent")
    plt.ylabel("Win Percent")
    plt.show()


def add_data(standings, data):
    for i, p in enumerate(standings):
        data.append((p.spaces_moved, i+1))


def plot_data(data):
    avgs = {1:0, 2:0, 3:0, 4:0}
    num_games = len(data)/4
    for d in data:
        plt.plot(d[0], d[1], marker='o')
        avgs[d[1]] += d[0]
    avgs = {i: x/num_games for i, x in avgs.items()}
    plt.title("Number of spaces moved vs Standing")
    plt.xlabel("Total number of spaces moved")
    plt.ylabel("Standing (lower is better)")
    plt.show()


def trial(players, n, gs=GameStat()):
    wins = [0,0,0,0]
    data = []
    for x in range(0, n):
        g = Game(players, NUM_TURNS, stats=gs)
        g.run()
        wins[g.get_winner()] += 1
        gs.num_games += 1
        # add_data(g.state.standings, data)
    gs.print_stats_avg()
    # plot_data(data)
    return [x/n for x in wins]


NUM_TURNS = 50


if __name__ == '__main__':
    print(trial([(25,0), (25,1), (25,2), (25,3)], 1000))
