from kivy.uix.button import Button

from Event import Event
from model.GameObject import GameObject
from model.LevelGenerator import LevelGenerator
from copy import deepcopy


class Game:
    def __init__(self, levels=LevelGenerator.levels(), iters_per_second=30,
                 current_level_index=0):
        self._iters_per_second = iters_per_second
        self._levels = list(levels)
        self._current_level_index = current_level_index
        self._current_level = None
        self.refresh_level()
        self.level_changed = Event()
        self.game_end = Event()
        self.level_end_with_result = Event()

    def try_build_tower(self, tower_cls, location):
        if not location:
            raise ValueError
        if self.current_level.gold >= tower_cls.cost:
            if location in self.current_level.towers_locations:
                self.current_level.towers_locations.remove(location)
                GameObject.objects.add(tower_cls(location))
                self.current_level.gold -= tower_cls.cost
            else:
                raise ValueError
            return True
        return False

    def get_level_passing_success(self):
        hp_remainder = self.current_level.hp / self.current_level.max_hp
        result = int(hp_remainder // 0.33)
        return result if result != 0 else 1

    @property
    def current_level(self):
        return self._current_level

    def _on_level_end(self, is_win):
        GameObject.objects.clear()
        if is_win:
            self.level_end_with_result.fire(self._current_level_index,
                                            self.get_level_passing_success())
            self._current_level_index += 1
            if self._current_level_index < len(self._levels):
                self.refresh_level()
            else:
                self.game_end.fire(is_win=True)
                self._current_level_index = 0
                return

            self.level_changed.fire()
        else:
            self.game_end.fire(is_win=False)

    @property
    def iters_per_second(self):
        return self._iters_per_second

    @iters_per_second.setter
    def iters_per_second(self, value):
        if value < 20:
            raise ValueError
        self._iters_per_second = value

    def set_level(self, number):
        if number < len(self._levels):
            self._current_level_index = number
            self.refresh_level()
        else:
            raise ValueError

    def refresh_level(self):
        GameObject.objects.clear()
        level = deepcopy(self._levels[self._current_level_index])
        level.on_end_level += self._on_level_end
        self._current_level = level

    def make_game_iteration(self):
        self._current_level.tick()
