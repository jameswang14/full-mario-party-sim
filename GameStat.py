class GameStat(object):
    def __init__(self):
        self.num_games = 0
        self._stats = {}

    def inc(self, key, amt=1):
        if key not in self._stats:
            self._stats[key] = 0
        self._stats[key] += amt
    def dec(self, key, amt):
        if key not in self._stats:
            self._stats[key] = 0
        self._stats[key] -= amt

    def print_stats(self):
        for k,v in self._stats.items():
            print("{}: {}".format(k, v))
    def print_stats_avg(self):
        for k,v in self._stats.items():
            print("{}: {}".format(k, v/self.num_games))


