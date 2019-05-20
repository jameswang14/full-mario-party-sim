import random
from board.TileBase import TileType, TileBase

BOWSER_MINIGAME_PCT = 0.5
BOWSER_TAKE_STAR_PCT = 0.1 
BOWSER_MIN_COIN_TAKE = 5
BOWSER_MAX_COIN_TAKE = 50


class BowserTile(TileBase):
    def __init__(self, _id):
        super(BowserTile, self).__init__(TileType.BOWSER, _id)

    def apply(self, player, state, stats=None):
        stats.inc("num_bowsers")

        # Bowser straight up takes stuff from you
        if random.random() < (1-BOWSER_MINIGAME_PCT):
            if random.random() < BOWSER_TAKE_STAR_PCT:
                player.stars -= 1 
                player.stars = max(player.stars, 0)
            else:                    
                player.coins -= random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)
                player.coins = max(player.coins, 0)

        # Bowser mini-game: These are interesting since they're survival games rather than battles. 
        # In my experience, these mini-games vary in widely in difficulty but are generally not that 
        # easy to win. The single-player games do seem to be easier than the multiplayer ones, 
        # but for a multiplayer game only one player has to win to avoid all penalties for everyone. 
        else:
            # Single-player: apply a slight bonus since single-player games tend to be pretty easy
            if random.random() < 0.5: 
                # Failed - apply penalty
                if random.random() < 1-(player.skill / 100 + 0.05):
                    if random.random() < BOWSER_TAKE_STAR_PCT:
                        player.stars -= 1
                        player.start = max(player.stars, 0)
                    else:
                        player.coins -= random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)
                        player.coins = max(player.coins, 0)
            # Multi-player: only one player has to pass
            else:
                game_pass = False
                for x in state.players:
                    if random.random() < player.skill / 100:
                        game_pass = True
                        break
                if not game_pass:
                    if random.random() < BOWSER_TAKE_STAR_PCT:
                        for x in state.players: 
                            x.stars -= 1
                            x.stars = max(x.stars, 0)
                    else:
                        t = random.randint(BOWSER_MIN_COIN_TAKE, BOWSER_MAX_COIN_TAKE)
                        for x in state.players: 
                            x.coins -= t
                            x.coins = max(x.coins, 0)

        state.minigame_assign[player] = 'red'