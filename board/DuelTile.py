import math
import random
from board.TileBase import TileType, TileBase
class DuelTile(TileBase):
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
    def __init__(self, _id):
        super(DuelTile, self).__init__(TileType.DUEL, _id)

    def apply(self, player, state, stats=None):
        stats.inc("num_duels")
        ev = self.calc_duel_ev(player, state)
        duel_target = max(ev, key=ev.get)

        if player != state.standings[0]:
            stats.inc("num_duels_by_not_first")
            if duel_target == state.standings[0]:
                stats.inc("duel_top_player")

        win_pct = player.skill / max((duel_target.skill + player.skill), 1)
        winner = duel_target
        loser = player
        if random.random() < win_pct:
            winner = player
            loser = duel_target

        opt = random.choice([1,2,3,4,5,6])
        # Win 10 coins
        if opt == 2:
            stats.inc("coins_from_duels", min(loser.coins, 10))
            winner.coins += min(loser.coins, 10)
            loser.coins -= min(loser.coins, 10)

        # Win half coins
        if opt == 3:
            stats.inc("coins_from_duels", loser.coins / 2)
            winner.coins += loser.coins / 2
            loser.coins /= 2

        # Win all coins
        if opt == 4:
            stats.inc("coins_from_duels", loser.coins)
            winner.coins += loser.coins
            loser.coins = 0

        # Win one star
        if opt == 5:
            stats.inc("stars_from_duels", min(loser.stars, 1))
            winner.stars += min(loser.stars, 1)
            loser.stars -= min(loser.stars, 1)

        # Win two stars
        if opt == 6:
            stats.inc("stars_from_duels", min(loser.stars, 2))
            winner.stars += min(loser.stars, 2)
            loser.stars -= min(loser.stars, 2)

        if random.random() < 0.5: state.minigame_assign[player] = 'red'
        else: state.minigame_assign[player] = 'blue'

    def calc_duel_ev(self, player, state):
        ev = {}
        for x in state.players:
            if x == player: continue
            win_pct = player.skill / max((x.skill + player.skill), 1)
            star_to_coins = 60 * math.exp(math.log(5) * (state.turn_num / state.max_turns))
            exp_val = win_pct * (1/6) * (0 + min(x.coins, 10) + x.coins/2 + x.coins + min(x.stars, 1) * star_to_coins + min(x.stars, 2) * star_to_coins)
            exp_val -= (1-win_pct) * (1/6) * (0 + min(player.coins, 10) + player.coins/2 + player.coins + min(player.stars, 1) * star_to_coins + min(x.stars, 2) * star_to_coins)
            ev[x] = exp_val
        return ev