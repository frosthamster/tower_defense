from Event import Event
from model.GameObject import GameObject


class Level:
    def __init__(self, start_gold, towers_locations, waves_manager, map_path,
                 start_hp=50):
        self._gold = start_gold
        self._hp = start_hp
        self._max_hp = start_hp
        self.map_path = map_path
        self._towers_location = towers_locations
        self._waves_manager = waves_manager
        self._waves_manager.on_waves_end += self._on_last_wave_coming
        self.on_end_level = Event()
        self._last_wave_is_coming = False

    @property
    def towers_locations(self):
        return self._towers_location

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def current_wave(self):
        wm = self._waves_manager
        return f'{wm.current_wave}/{wm.waves_count}'

    @property
    def gold(self):
        return self._gold

    @gold.setter
    def gold(self, value):
        if value < 0:
            raise ValueError
        self._gold = value

    def _on_last_wave_coming(self):
        self._last_wave_is_coming = True

    def _on_enemy_end_path(self, enemy):
        self._hp -= enemy.damage
        if self._hp <= 0:
            self.on_end_level.fire(is_win=False)

    def _on_enemy_death(self, enemy):
        self._gold += enemy.cost
        self.gold_kv = str(self._gold)

    def tick(self):
        if not self._last_wave_is_coming:
            enemy = self._waves_manager.get_enemy()
            if enemy:
                GameObject.objects.add(enemy)
                enemy.on_end += lambda: self._on_enemy_end_path(enemy)
                enemy.on_death += lambda s: self._on_enemy_death(enemy)
        else:
            enemies = filter(lambda o: not o.friendly, GameObject.objects)
            if sum(1 for _ in enemies) == 0:
                self.on_end_level.fire(is_win=True)

        for obj in list(GameObject.objects):
            obj.tick()
