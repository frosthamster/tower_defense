from kivy.vector import Vector

from model.DamageType import DamageType
from model.GameObject import GameObject
from model.Missile import Missile
from model.MovableGameObject import MovableGameObject
from model.Spells import HealOverTime, DamageOverTime, Dispell


class Orc(MovableGameObject):
    def __init__(self, location, road, **kwargs):
        super().__init__(location, road, **kwargs)
        self._velocity = 1
        self._max_velocity = 1
        self._damage = 20
        self.sprite_path = 'res/enemies/orc.png'


class Bandit(MovableGameObject):
    cost = 5

    def __init__(self, location, road, **kwargs):
        super().__init__(location, road, **kwargs)
        self._velocity = 2.1
        self._max_velocity = 2.1
        self._damage = 10
        self._hp = 25
        self._max_hp = 20
        self._resists = {DamageType.PHYSICAL: 1,
                         DamageType.MAGICAL: 1}
        self.sprite_path = 'res/enemies/bandit.png'


class Shaman(MovableGameObject):
    cost = 30

    def __init__(self, location, road, **kwargs):
        super().__init__(location, road, **kwargs)
        self._velocity = 1
        self._max_velocity = 1
        self._damage = 20
        self._hp = 60
        self._max_hp = 60
        self._range = 100
        self._attack_cooldown = 650
        self._resists = {DamageType.PHYSICAL: 1,
                         DamageType.MAGICAL: 0.5}
        self.sprite_path = 'res/enemies/shaman.png'

    def _get_targets_to_attack(self):
        yield from filter(lambda e: not e.friendly and e.hp / e.max_hp < 0.5,
                          self.objects_in_range())

    def _do_attack(self, target):
        spell = HealOverTime(target, self, target.max_hp / 10, ticks_count=10,
                             tick_duration=5)
        GameObject.objects.add(
            Missile(self._location + Vector(0, 1), [spell]))
