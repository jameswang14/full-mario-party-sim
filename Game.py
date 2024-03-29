import random
import math
import utils
import numpy as np
from board.Board import Board
from board.BoardParser import parse_board_from_file
from board.BlueTile import BlueTile
from board.RedTile import RedTile
from board.GreenTile import GreenTile
from board.BowserTile import BowserTile
from board.DKTile import DKTile
from board.DuelTile import DuelTile
from board.ItemTile import ItemTile
from board.ShopTile import ShopTile
from board.IntersectionTile import IntersectionTile
from items.ItemBase import ItemType

from Player import Player
from GameStat import GameStat
from state.State import State

# KNOWN VALUES - Based on averages from 5 multiplayer boards in Mario Party 7 #
RED_PCT = 0.12524186787
GREEN_PCT = 0.0860890342
DK_PCT = 0.03283618376
BOWSER_PCT = 0.03283618376
DUEL_PCT = 0.05211141851
ITEM_PCT = 0.05778546277
SHOP_PCT = 0.03283618376
BLUE_PCT = 1 - (RED_PCT + GREEN_PCT + DK_PCT + BOWSER_PCT + DUEL_PCT)
# ----------------------------------------------------------- #

# ESTIMATES #
MIN_STAR_DIST = 10
MAX_STAR_DIST = 40
GREEN_STAR_PCT = 0.05
BOWSER_MINIGAME_PCT = 0.5
BOWSER_TAKE_STAR_PCT = 0.1 
BOWSER_MIN_COIN_TAKE = 5
BOWSER_MAX_COIN_TAKE = 50
BATTLE_MINIGAME_PCT = 0.1
# ----------------------------------------------------------- #

def count(l, t):
    return len([x for x in l if x == t])

class Game(object):
    def __init__(self, players, max_turns, stats=GameStat()):
        self.board = parse_board_from_file("./board/board_test.txt")
        self.state = State(players, max_turns, self.board, stats)
        self.total_skill = sum([x[0] for x in players])
        self.stats = stats

    def run(self):
        self.start_game()
        while self.state.turn_num < self.state.max_turns:
            self.update_standings() 
            self.turn()
            self.minigame()
            self.state.turn_num += 1
        self.bonus_stars()
        self.update_standings() 

    def start_game(self):
        for p in self.state.players:
            p.coins = 10
            self.state.player_to_tile[p] = self.board.start

    def turn(self):
        for p in self.state.players:
            p.use_item(self.state)
            # if we use a mushroom, rolls are handled on item.apply so we don't need to roll again
            if self.state.current_roll == 0:
                p.roll(self.state)
            next_tile = None
            while self.state.current_roll > 0:
                next_tile = self.state.player_to_tile[p].next[0]
                if next_tile == self.state.star: 
                    p.buy_star(next_tile, self.state)
                elif next_tile._id in self.state.tiles_with_items and self.state.tiles_with_items[next_tile._id].type == ItemType.PASS:
                    self.state.tiles_with_items[next_tile._id].apply(p, self.state)
                    del self.state.tiles_with_items[next_tile._id]
                elif isinstance(next_tile, ItemTile) or isinstance(next_tile, ShopTile):
                    next_tile.apply(p, self.state, self.stats)
                elif not isinstance(next_tile, IntersectionTile):
                    # TODO replace naive logic
                    next_tile = random.choice(self.state.player_to_tile[p].next)
                    self.state.current_roll -= 1
                    p.spaces_moved += 1
                    self.stats.inc("spaces_moved")
                    if "zapped" in p.status:
                        self.stats.inc("coins_lost_to_zap", amt=3)
                        p.coins = max(0, p.coins - 3)

                self.state.player_to_tile[p] = next_tile
            
            if next_tile._id in self.state.tiles_with_items:
                self.state.tiles_with_items[next_tile._id].apply(p, self.state)
            else:
                next_tile.apply(p, self.state, self.stats)
            p.update_status()


    def minigame(self):
        win_amt = 0
        battle = False
        # Battle Mini-game
        if random.random() < BATTLE_MINIGAME_PCT: 
            battle = True
            bounty = 5 * random.choice([1, 2, 4, 6, 8, 10])
            for p in self.state.players:
                win_amt += min(bounty, p.coins)
                p.coins -= min(bounty, p.coins)
            self.stats.inc("num_battle")
            self.stats.inc("total_battle_bounty", win_amt)

        else: win_amt = 10
        # Battle or 4-player Minigame
        if battle or count(self.state.minigame_assign.values(), 'blue') == 4 or count(self.state.minigame_assign.values(), 'red') == 4:
            r = random.random()
            p = 0.0
            win_pcts = [p.skill/self.total_skill for p in self.state.players]
            for i, pct in enumerate(win_pcts):
                p += pct
                if r < p:
                    self.state.players[i].coins += win_amt
                    self.state.players[i].minigames_won += 1
                    break

            self.stats.inc("num_four_vs_four")

        # 3v1 Minigame - we use the average skill of the group of 3 to calculate the chance they win the minigame
        elif count(self.state.minigame_assign.values(), 'blue') == 3 or count(self.state.minigame_assign.values(), 'red') == 3:
            dominant = 'blue'
            if count(self.state.minigame_assign.values(), 'red') == 3: 
                dominant = 'red'
            three_team = [p for p in self.state.players if self.state.minigame_assign[p] == dominant]
            single_team = [p for p in self.state.players if self.state.minigame_assign[p] != dominant]
            avg_skill = np.mean([x.skill for x in three_team])
            win_pct = avg_skill / (avg_skill + single_team[0].skill)

            if random.random() < win_pct:
                for x in three_team:
                    x.coins += 10
                    x.minigames_won += 1

            else:
                single_team[0].coins += 10
                single_team[0].minigames_won += 1 

            self.stats.inc("num_three_vs_one")

        # 2v2 Minigame - we use the average skill of each team to calculate their chance to win the minigame
        else:
            team_one = [p for p in self.state.players if self.state.minigame_assign[p] == 'blue']
            team_two = [p for p in self.state.players if self.state.minigame_assign[p] == 'red']
            avg_skill_one = np.mean([x.skill for x in team_one])
            avg_skill_two = np.mean([x.skill for x in team_two])
            win_pct = avg_skill_one / (avg_skill_one + avg_skill_two)

            if random.random() < win_pct:
                for x in team_one:
                    x.coins += 10
                    x.minigames_won += 1

            else:
                for x in team_two:
                    x.coins += 10
                    x.minigames_won += 1

            self.stats.inc("num_two_vs_two")

    def green_square(self, p):
        r = random.choice([1,2,3])

        # +Coins/Star - Coins are pretty much guaranteed, usually the question is how many. 
        # Stars are much more rare
        if r == 1:
            p.coins += random.randint(1, 20)
            if random.random() <= GREEN_STAR_PCT:
                p.stars += 1
                self.stats.inc("green_star")
                self.stats.inc("num_stars")

        # -Coins - I don't think there are any green spaces that make you lose coins in MP7, but 
        # they're usually present in other games so I've included it here
        if r == 2:
            p.coins -= random.randint(1, 10)

        # Teleport - Note: These don't contribute to the movement bonus star
        if r == 3:
            p.spaces_from_star = random.randint(0, MAX_STAR_DIST)
            if p.spaces_from_star == 0:
                self.buy_star(p) # Yes it's possible to get two stars in one turn!
                self.stats.inc("num_stars")

        if random.random() < 0.3: self.state.minigame_assign[p] = 'red' # with a 50/50 chance, I noticed the number of 1v3 minigames seemed higher than it should be
        else: self.state.minigame_assign[p] = 'blue'

        p.green += 1

    # Bowser really differs from game to game, but we keep it simple and assume
    # he either straight up takes from you or forces you to play a minigame
    def bowser_square(self, p):
        self.stats.inc("num_bowsers")

        # Bowser straight up takes stuff from you
        if random.random() < (1-BOWSER_MINIGAME_PCT):
            if random.random() < BOWSER_TAKE_STAR_PCT:
                p.stars -= 1 
            else:                    
                p.coins -= random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)

        # Bowser mini-game: These are interesting since they're survival games rather than battles. 
        # In my experience, these mini-games vary in widely in difficulty but are generally not that 
        # easy to win. The single-player games do seem to be easier than the multiplayer ones, 
        # but for a multiplayer game only one player has to win to avoid all penalties for everyone. 
        else:
            # Single-player: apply a slight bonus since single-player games tend to be pretty easy
            if random.random() < 0.5: 
                # Failed - apply penalty
                if random.random() < 1-(p.skill / 100 + 0.05):
                    if random.random() < BOWSER_TAKE_STAR_PCT:
                        p.stars -= 1
                    else:
                        p.coins -= random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)
            # Multi-player: only one player has to pass
            else:
                game_pass = False
                for x in self.state.players:
                    if random.random() < p.skill / 100:
                        game_pass = True
                        break
                if not game_pass:
                    if random.random() < BOWSER_TAKE_STAR_PCT:
                        for x in self.state.players: x.stars -= 1
                    else:
                        t = random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)
                        for x in self.state.players: x.coins -= t

        self.state.minigame_assign[p] = 'red'


    # In other Mario Parties, DK usually does more. A star may only be acquired in single-player minigames
    def dk_square(self, p):
        # Single-Player DK
        if random.random() < 0.5:
            if random.random() < p.skill/100.0: # Wins
                r_dk = random.choice([1,2,3,4])
                if r_dk == 4:
                    p.stars += 1
                else:
                    p.coins += 10 * r_dk
        # Multi-Player DK
        else:
            r_dk = random.choice([1,2,3])
            total_bananas = 35
            for x in self.state.players:
                x.coins += int(x.skill/self.total_skill * total_bananas) * r_dk

        self.state.minigame_assign[p] = 'blue'

    # Duels are especailly key since they can drastically turn a game around. Choosing an optimal 
    # duel opponent can be tricky, since it depends both on how many turns are remaining, how many stars/coins everyone has,
    # and the relative skill level of players. For example, while it makes sense to pick the weakest player, if she
    # has no stars, or if you're second and close to first, then it doesn't make sense to select her. It becomes even more
    # tricky in older MP games as the stakes aren't random and instead can be chosen. 
    #
    # Here, we'll stick with MP7 duel mechanics and make the stakes random with the possibilities being 
    # nothing, 10 coins, half coins, all coins, 1 star, 2 stars.
    #
    # To select an opponent, we'll assume players are always rational and choose the most +EV opponent. This may not necessarily
    # true in practice, since all that matters is first place so sometimes it makes sense to take larger risks. In other cases 
    # such as near the end of a game, it makes sense to take less risks and always choose the weakest opponent if you're in first.
    # 
    # Calculating EV is a bit tricky since we're working with both stars and coins. While stars are usually bought for 20 coins, 
    # it'd be very incorrect to use this conversion rate. Assuming that the farthest a star can be is 40 blocks, it would require at least 
    # two 3x dice blocks to reach it as quick as possible, giving us an actual cost of about 60 coins. Additionally, stars become
    # way more valuable as turns pass. So we assign stars a base value of 60 coins and exponentially scale their value up to 300 as 
    # time increases. This increase potential upside for those not in first. 
    # 
    # Time should also increase potential downside for winning players (TODO)
    # 
    # And because only first place matters, we calculate EV relative to first place. So if you're in first place, EV is based off 
    # your "distance" to second place. For all other positions, EV is your "distance" to first place. Distance is measured by coins (after conversion).
    def duel_square(self, p):
        self.stats.inc("num_duels")
        ev = self.calc_duel_ev(p)
        duel_target = max(ev, key=ev.get)

        if p != self.state.standings[0]:
            self.stats.inc("num_duels_by_not_first")
            if duel_target == self.state.standings[0]:
                self.stats.inc("duel_top_player")

        win_pct = p.skill / max((duel_target.skill + p.skill), 1)
        winner = duel_target
        loser = p
        if random.random() < win_pct:
            winner = p
            loser = duel_target

        opt = random.choice([1,2,3,4,5,6])
        # Win 10 coins
        if opt == 2:
            self.stats.inc("coins_from_duels", min(loser.coins, 10))
            winner.coins += min(loser.coins, 10)
            loser.coins -= min(loser.coins, 10)

        # Win half coins
        if opt == 3:
            self.stats.inc("coins_from_duels", loser.coins / 2)
            winner.coins += loser.coins / 2
            loser.coins /= 2

        # Win all coins
        if opt == 4:
            self.stats.inc("coins_from_duels", loser.coins)
            winner.coins += loser.coins
            loser.coins = 0

        # Win one star
        if opt == 5:
            self.stats.inc("stars_from_duels", min(loser.stars, 1))
            winner.stars += min(loser.stars, 1)
            loser.stars -= min(loser.stars, 1)

        # Win two stars
        if opt == 6:
            self.stats.inc("stars_from_duels", min(loser.stars, 2))
            winner.stars += min(loser.stars, 2)
            loser.stars -= min(loser.stars, 2)

        if random.random() < 0.5: self.state.minigame_assign[p] = 'red'
        else: self.state.minigame_assign[p] = 'blue'


    def calc_duel_ev(self, p):
        ev = {}
        for x in self.state.players:
            if x == p: continue
            win_pct = p.skill / max((x.skill + p.skill), 1)
            star_to_coins = 60 * math.exp(math.log(5) * (self.state.turn_num / self.state.max_turns))
            exp_val = win_pct * (1/6) * (0 + min(x.coins, 10) + x.coins/2 + x.coins + min(x.stars, 1) * star_to_coins + min(x.stars, 2) * star_to_coins)
            exp_val -= (1-win_pct) * (1/6) * (0 + min(p.coins, 10) + p.coins/2 + p.coins + min(p.stars, 1) * star_to_coins + min(x.stars, 2) * star_to_coins)
            ev[x] = exp_val
        return ev

    def roll(self):
        return random.randint(1, 10)

    def buy_star(self, p):
        p.stars += 1
        p.coins -= 20

    def move_star(self):
        new_star = random.randint(MIN_STAR_DIST, MAX_STAR_DIST)
        for x in self.state.players:
            x.spaces_from_star = min(5, new_star-x.spaces_from_star)

    def bonus_stars(self):
        opts = [
            "minigames_won",
            "spaces_moved",
            "green",
            "red",
            # "shopping_star",
            # "orb_star",
        ]
        choices = random.choices(opts, k=3)
        for c in choices: 
            winners = self._get_bonus_star_winners(c)
            for p in winners:
                p.stars += 1

    def _get_bonus_star_winners(self, attr):
        m = max(self.state.players, key=lambda x: getattr(x, attr))
        return [p for p in self.state.players if getattr(p, attr) == m]

    def update_standings(self):
        # Sort by coins, then by stars to take advantage of stable sort
        self.state.standings = sorted(self.state.players, key=lambda x: x.coins, reverse=True)
        self.state.standings = sorted(self.state.standings, key=lambda x: x.stars, reverse=True)

    def print_results(self):
        for p in self.state.players: print(p)

    def get_winner(self):
        self.update_standings()
        return self.state.standings[0]._id
