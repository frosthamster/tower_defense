from abc import ABCMeta
from itertools import islice

from kivy.vector import Vector

from Event import Event
from model.DamageType import DamageType
from model.Direction import Direction


class GameObject(metaclass=ABCMeta):
    objects = set()
    cost = 10

    def __init__(self, location, damage_type=DamageType.PHYSICAL,
                 graphics_offset=Vector(0, 0)):
        self._location = location
        self._max_velocity = 0
        self._velocity = 0
        self._friendly = False

        self._range = 1
        self._damage = 1
        self._attack_cooldown = 30
        self._current_attack_cooldown = 0
        self._max_targets_to_attack = 1

        self._max_hp = 100
        self._hp = self._max_hp

        self._spells = set()

        self._direction = Direction.RIGHT
        self.sprite_path = ''
        self.graphics_offset = graphics_offset
        self._damage_type = damage_type

        self._resists = {DamageType.PHYSICAL: 1,
                         DamageType.MAGICAL: 0.7}

        self.on_death = Event()
        self.on_remove = Event()

    @property
    def damage_type(self):
        return self._damage_type

    @property
    def hp(self):
        return self._hp

    @property
    def max_hp(self):
        return self._max_hp

    @property
    def direction(self):
        return self._direction

    @property
    def friendly(self):
        return self._friendly

    @property
    def damage(self):
        return self._damage

    @damage.setter
    def damage(self, value):
        if value < 0:
            raise ValueError
        self._damage = value

    @property
    def spells(self):
        return self._spells

    @property
    def location(self):
        return self._location

    @property
    def velocity(self):
        return self._velocity

    @velocity.setter
    def velocity(self, value):
        if value < 0:
            value = 0
        if value > self._max_velocity:
            value = self._max_velocity
        self._velocity = value

    def _try_attack(self):
        if self._current_attack_cooldown > 0:
            self._current_attack_cooldown -= 1
        else:
            targets = self._get_targets_to_attack()
            if targets is not None:
                for target in islice(targets, self._max_targets_to_attack):
                    self._do_attack(target)
                    self._current_attack_cooldown = self._attack_cooldown

    def _do_attack(self, target):
        target.change_hp(-self._damage, self)

    def _get_targets_to_attack(self):
        pass

    def tick(self):
        self._try_attack()
        for spell in set(self._spells):
            spell.tick()

    def cast_spell(self, spell):
        if spell.target != self:
            raise ValueError
        self._spells.add(spell)

    def dispell(self, spell):
        if spell in self._spells:
            self._spells.remove(spell)

    def dispell_all(self):
        for spell in filter(lambda e: not e.is_buff, set(self._spells)):
            self._spells.remove(spell)

    def change_hp(self, delta, sender):
        if delta < 0:
            delta = delta * self._resists[sender.damage_type]
        self._hp += delta
        if self._hp > self._max_hp:
            self._hp = self._max_hp

        if self._hp <= 0:
            self.on_death.fire(sender)
            self._remove()

    def _remove(self):
        if self in GameObject.objects:
            GameObject.objects.remove(self)
            self.on_remove.fire(self._friendly)

    def objects_in_range(self):
        for obj in list(GameObject.objects):
            if obj == self:
                continue
            distance = (self._location - obj.location).length()
            if distance <= self._range:
                yield obj

    def __str__(self):
        return f'{self.__class__}:{self._location}'
