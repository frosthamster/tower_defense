from model.Spell import Spell


class HealOverTime(Spell):
    def __init__(self, target, owner, power, **kwargs):
        super().__init__(target, owner, lambda t, _: t.change_hp(power, owner),
                         **kwargs)


class DamageOverTime(Spell):
    def __init__(self, target, owner, power, **kwargs):
        super().__init__(target, owner,
                         lambda t, _: t.change_hp(-power, owner),
                         is_buff=False,
                         **kwargs)


class Slow(Spell):
    def __init__(self, target, owner, power, **kwargs):
        self._subtracted_speed = target.velocity / power
        super().__init__(target, owner, self.slow,
                         on_remove_effect=self.speed_up,
                         is_buff=False, ticks_count=2, tick_duration=200,
                         **kwargs)

    def slow(self, target, owner):
        target.velocity -= self._subtracted_speed

    def speed_up(self, target, owner):
        target.velocity += 2 * self._subtracted_speed


class Dispell(Spell):
    def __init__(self, target, owner, **kwargs):
        super().__init__(target, owner, lambda t, _: t.dispell_all(), **kwargs)
