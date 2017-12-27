from kivy.vector import Vector

from model.Enemies import Orc, Bandit, Shaman
from model.Level import Level
from model.WavesManager import WavesManager, WavePart


class LevelGenerator:
    @staticmethod
    def levels():
        path = [Vector(320, 600), Vector(320, 420), Vector(290, 360),
                Vector(211, 338), Vector(170, 293), Vector(168, 244),
                Vector(212, 180), Vector(318, 170), Vector(385, 178),
                Vector(477, 162), Vector(588, 237), Vector(710, 255)]
        towers = [Vector(465, 222), Vector(178, 392), Vector(254, 295),
                  Vector(241, 417), Vector(248, 234), Vector(323, 234),
                  Vector(387, 138), Vector(586, 161)]
        waves = [WavePart([Orc] * 3 + [Shaman] * 2, Vector(310, 630), path),
                 WavePart([Bandit] * 15, Vector(310, 630), path,
                          unit_interval=15),
                 WavePart([Orc, Orc, Shaman] * 4, Vector(310, 630), path)]
        yield Level(100, towers, WavesManager(waves), 'res/maps/level1.png')

        path = [Vector(700, 390), Vector(527, 392), Vector(493, 491),
                Vector(438, 517), Vector(377, 488), Vector(346, 393),
                Vector(221, 380), Vector(166, 319), Vector(202, 272),
                Vector(267, 266), Vector(389, 288), Vector(452, 256),
                Vector(426, 176), Vector(321, 147), Vector(308, -10)]
        towers = [Vector(438, 458), Vector(437, 396), Vector(299, 442),
                  Vector(247, 330), Vector(305, 218), Vector(379, 232),
                  Vector(390, 122)]
        waves = [WavePart([Orc] * 3 + [Shaman] * 2, Vector(710, 390), path),
                 WavePart([Bandit] * 15, Vector(710, 390), path,
                          unit_interval=15),
                 WavePart([Orc, Orc, Shaman] * 4, Vector(710, 390), path)]
        yield Level(200, towers, WavesManager(waves), 'res/maps/level2.png')

        path1 = [Vector(309, 148), Vector(472, 155), Vector(577, 186),
                 Vector(625, 281), Vector(592, 383), Vector(461, 490),
                 Vector(397, 514), Vector(402, 624)]
        path2 = [Vector(309, 148), Vector(144, 281), Vector(110, 370),
                 Vector(150, 452), Vector(244, 503),
                 Vector(397, 514), Vector(402, 624)]

        towers = [Vector(400, 470), Vector(318, 470), Vector(243, 448),
                  Vector(199, 406), Vector(192, 346), Vector(213, 305),
                  Vector(92, 251), Vector(511, 382), Vector(547, 322),
                  Vector(551, 263), Vector(495, 215),
                  Vector(414, 206), Vector(325, 211), Vector(474, 110),
                  Vector(586, 128)]
        waves = [WavePart([Orc] * 3 + [Shaman] * 2, Vector(300, -20), path1),
                 WavePart([Bandit] * 15, Vector(300, -20), path2,
                          unit_interval=15),
                 WavePart([Orc, Orc, Shaman] * 4, Vector(300, -20), path1)]
        yield Level(200, towers, WavesManager(waves), 'res/maps/level3.png')
