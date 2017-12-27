from model.LevelGenerator import LevelGenerator


class Results:
    def __init__(self):
        levels = LevelGenerator.levels()
        self._results = [(level.map_path, 0) for level in levels]

    @property
    def results(self):
        return self._results

    def add_level_result(self, level_number, result):
        if level_number < 0 or level_number >= len(self._results):
            raise ValueError
        if result < 0 or result > 3:
            raise ValueError

        map_path, old_result = self._results[level_number]
        if result > old_result:
            self._results[level_number] = (map_path, result)

    @property
    def last_completed_level_index(self):
        for i in range(len(self._results)):
            mp, res = self._results[i]
            if res == 0:
                return i - 1
        return len(self._results) - 1
