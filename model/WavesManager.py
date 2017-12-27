from Event import Event


class WavePart:
    def __init__(self, enemies_cls, start, path, next_wave_interval=None,
                 unit_interval=None):
        self.enemies_cls = enemies_cls
        self.path = path
        self.start = start
        self.next_wave_interval = next_wave_interval
        self.unit_interval = unit_interval


class WavesManager:
    def __init__(self, waves, unit_interval=30, wave_interval=650,
                 preparation_duration=100):
        self._iteration = -1
        self._enemy_on_time = {}
        self._wave_interval = wave_interval
        self._count = len(waves)
        self.on_waves_end = Event()
        self._enemies_count = 0
        self._waves_borders = set()
        self._current_wave = 0
        self._waves_count = len(waves)

        index = preparation_duration
        for part in waves:
            self._unit_interval = unit_interval
            if part.unit_interval is not None:
                self._unit_interval = part.unit_interval
            enemies_count = len(part.enemies_cls)
            self._enemies_count += enemies_count
            self._waves_borders.add(index)
            for i, enemy_cls in enumerate(part.enemies_cls):
                self._enemy_on_time[index + i * self._unit_interval] = \
                    enemy_cls(part.start, part.path)
            if part.next_wave_interval:
                index += part.next_wave_interval
            else:
                index += self._wave_interval
            index += 1 + enemies_count * self._unit_interval
            index += preparation_duration

    @property
    def count(self):
        return self._count

    @property
    def waves_count(self):
        return self._waves_count

    @property
    def current_wave(self):
        return self._current_wave

    def get_enemy(self):
        self._iteration += 1
        if self._iteration in self._waves_borders:
            self._current_wave += 1

        if self._enemies_count <= 0:
            self.on_waves_end.fire()

        if self._iteration in self._enemy_on_time:
            self._enemies_count -= 1
            return self._enemy_on_time[self._iteration]
