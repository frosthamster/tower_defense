from itertools import islice

from kivy.vector import Vector

from model.GameObject import GameObject
from model.Missile import Missile
from model.Spells import DamageOverTime


class Tower(GameObject):
    def __init__(self, location):
        super().__init__(location)
        self._friendly = True
        self._range = 100
        self._attack_cooldown = 10
        self.graphics_offset = Vector(0, 20)
        self.missile_graphics_offset = Vector(0, 1)
        self._upgrade_cost, self._image, self._description = None, None, None
        self._upgrades = self._get_upgrades()
        self._spells_builders = [
            lambda t: DamageOverTime(t, self, self._damage)]
        self.upgrade()

    def upgrade(self):
        try:
            self._upgrade_cost, self._image, self._description = next(
                self._upgrades)
        except StopIteration:
            self._upgrade_cost = None

    @property
    def upgrade_info(self):
        if self._upgrade_cost is None:
            return None
        return self._upgrade_cost, self._image, self._description

    def _get_upgrades(self):
        yield from ()

    def _get_targets_to_attack(self):
        yield from filter(lambda e: not e.friendly, self.objects_in_range())

    def _do_attack(self, target):
        spells = [builder(target) for builder in self._spells_builders]
        GameObject.objects.add(
            Missile(self._location + self.missile_graphics_offset, spells))
