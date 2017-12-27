from model.MovableGameObject import MovableGameObject


class Missile(MovableGameObject):
    def __init__(self, location, spells, **kwargs):
        super().__init__(location, (spells[0].target,), **kwargs)

        target = spells[0].target
        for spell in spells:
            if target != spell.target:
                raise ValueError

        self._effects = spells
        self._friendly = True
        self._range = 5
        self._velocity = 10
        self._max_velocity = 10
        self.sprite_path = 'res/missile.png'

    def _get_targets_to_attack(self):
        if self._effects[0].target in self.objects_in_range():
            yield self._effects[0].target

    def _do_attack(self, target):
        for spell in self._effects:
            target.cast_spell(spell)

    @property
    def curr_destination(self):
        return self._effects[0].target.location

    @property
    def destination(self):
        return self._effects[0].target.location

    def tick(self):
        super().tick()
        if self._current_attack_cooldown > 0:
            self._remove()
            self.on_end.fire(self)
