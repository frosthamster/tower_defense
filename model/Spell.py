class Spell:
    def __init__(self, target, owner, effect, ticks_count=1,
                 tick_duration=100, is_buff=True, is_permanent=False,
                 on_remove_effect=None):
        self._owner = owner
        self._is_buff = is_buff
        self._target = target
        self._effect = effect
        self._is_permanent = is_permanent
        self._ticks_count = ticks_count
        self._tick_duration = tick_duration
        self._current_tick_count = 0
        self._on_remove_effect = on_remove_effect

    def tick(self):
        if self._current_tick_count > 0:
            self._current_tick_count -= 1
        else:
            self._effect(self._target, self._owner)
            self._current_tick_count = self._tick_duration
            if not self._is_permanent:
                self._ticks_count -= 1
                if self._ticks_count <= 0:
                    self._target.dispell(self)
                    if self._on_remove_effect is not None:
                        self._on_remove_effect(self._target, self._owner)

    @property
    def target(self):
        return self._target

    @property
    def is_buff(self):
        return self._is_buff