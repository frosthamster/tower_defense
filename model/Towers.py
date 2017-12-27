from kivy.vector import Vector

from model.DamageType import DamageType
from model.Spells import Slow
from model.Tower import Tower


class Mage(Tower):
    cost = 50

    def __init__(self, location):
        super().__init__(location)
        self.sprite_path = 'res/towers/mage.png'
        self._damage = 100
        self._attack_cooldown = 150
        self._damage_type = DamageType.MAGICAL
        self.missile_graphics_offset = Vector(0, 60)
        self._spells_builders.append(lambda t: Slow(t, self, 2))

    def _get_upgrades(self):
        yield 60, 'res/towers/mage2.png', 'Increase\ndamage and speed'
        self.sprite_path = 'res/towers/mage2.png'
        self._damage += 45
        self._attack_cooldown -= 50


class Archers(Tower):
    cost = 40

    def __init__(self, location):
        super().__init__(location)
        self.sprite_path = 'res/towers/archers.png'
        self._damage = 5
        self._max_targets_to_attack = 2
        self._attack_cooldown = 10

    def _get_upgrades(self):
        yield 50, 'res/towers/archers2.png', 'Add additional\nmissile'
        self.sprite_path = 'res/towers/archers2.png'
        self._max_targets_to_attack += 1
