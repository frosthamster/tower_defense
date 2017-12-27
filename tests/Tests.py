import unittest

from kivy.vector import Vector

from model.Enemies import Orc
from model.Game import Game
from model.GameObject import GameObject
from model.Level import Level
from model.Missile import Missile
from model.MovableGameObject import MovableGameObject
from model.Tower import Tower
from model.Towers import Mage
from model.WavesManager import WavePart, WavesManager


class Tests(unittest.TestCase):
    def tearDown(self):
        GameObject.objects.clear()

    def _find(self, cls):
        return list(filter(lambda o: isinstance(o, cls), GameObject.objects))

    def test_objs_in_range(self):
        o0 = GameObject(Vector(0, 0))
        o0._range = 2

        o1 = GameObject(Vector(0, 1))
        o2 = GameObject(Vector(0, 2))
        GameObject.objects.add(o0)
        GameObject.objects.add(o1)
        GameObject.objects.add(o2)

        self.assertSetEqual({o1, o2}, set(o0.objects_in_range()))
        o0._range = 1
        self.assertSetEqual({o1}, set(o0.objects_in_range()))
        o0._range = 0
        self.assertSetEqual(set(), set(o0.objects_in_range()))

    def test_attack(self):
        obj2 = GameObject(Vector(1, 1))
        obj2._hp = 10

        obj = GameObject(Vector(0, 0))
        obj._get_targets_to_attack = lambda: (obj2,)
        obj._damage = 5
        obj._attack_cooldown = 1
        GameObject.objects.add(obj)
        obj.tick()
        self.assertEqual(5, obj2._hp)
        obj2.on_death += lambda s: self.assertEqual(obj, s)
        obj.tick()
        obj.tick()
        self.assertTrue(obj2 not in GameObject.objects)

    def test_movement(self):
        obj = MovableGameObject(Vector(0, 0), [Vector(0.5, 0), Vector(0.5, 1)])
        obj._velocity = 1
        obj.tick()
        self.assertListEqual(Vector(0.5, 0), obj.location)
        obj.tick()
        self.assertEqual(Vector(0.5, 1), obj.location)
        obj.tick()
        self.assertTrue(obj not in GameObject.objects)

    def test_tower(self):
        tow = Tower(Vector(0, 0))
        GameObject.objects.add(tow)
        tow._range = 2
        orc = Orc(Vector(0, 1), [Vector(0, 0)])
        GameObject.objects.add(orc)
        tow.tick()
        miss = self._find(Missile)
        self.assertTrue(len(miss) == 1)
        self.assertTrue(miss[0]._effects[0].target == orc)

    def test_build_tower(self):
        game = Game()
        game.current_level._gold = 100
        Mage.cost = 60
        loc = game.current_level.towers_locations[0]
        loc2 = game.current_level.towers_locations[1]
        game.try_build_tower(Mage, loc)
        tows = self._find(Mage)
        self.assertEqual(1, len(tows))
        self.assertListEqual(loc, tows[0].location)
        self.assertEqual(40, game.current_level.gold)
        game.try_build_tower(Mage, loc2)
        tows = self._find(Mage)
        self.assertEqual(1, len(tows))

    def test_wawes(self):
        Orc._velocity = 1
        path = [Vector(1, 0), Vector(2, 0)]
        towers = [Vector(0, 0)]
        waves = [WavePart([Orc] * 2, Vector(0, 0), path)]
        level = Level(100, towers, WavesManager(waves, preparation_duration=0,
                                                unit_interval=2), '')
        game = Game(levels=iter((level,)))
        game.current_level.tick()
        orcs = self._find(Orc)
        self.assertEqual(1, len(orcs))

        game.current_level.tick()
        orcs = self._find(Orc)
        self.assertEqual(1, len(orcs))

        game.current_level.tick()
        orcs = self._find(Orc)
        self.assertEqual(1, len(orcs))


if __name__ == '__main__':
    unittest.main()
