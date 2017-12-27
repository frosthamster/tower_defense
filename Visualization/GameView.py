from kivy.core.window import Window
from kivy.graphics.context_instructions import Image, Color
from kivy.graphics.gl_instructions import ClearColor
from kivy.graphics.vertex_instructions import Rectangle
from kivy.properties import Clock, StringProperty, ObjectProperty
from kivy.uix.widget import Widget
from kivy.utils import rgba
from kivy.vector import Vector

from model.Game import Game
from model.GameObject import GameObject
from model.MovableGameObject import MovableGameObject
from model.Tower import Tower


class GameView(Widget):
    gold = StringProperty('Gold:\n')
    hp = StringProperty('Hp:\n')
    start_stop_icon = StringProperty()
    change_speed_icon = StringProperty('res/x1_speed.png')
    wave = StringProperty('Wave:\n')

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._game = Game()
        self._current_speed_is_slow = True
        self._update_background_size()
        self._game.level_changed += self._update_background_size
        self._running = False
        self._game_timer_event = Clock.schedule_interval(
            lambda dt: self._make_iteration(dt),
            1.0 / self._game.iters_per_second)

    def change_running(self):
        if self._running:
            self.stop_game()
        else:
            self.start_game()

    @property
    def running(self):
        return self._running

    def change_speed(self):
        if self._current_speed_is_slow:
            self.change_speed_icon = 'res/x2_speed.png'
            self._game.iters_per_second += 30
        else:
            self.change_speed_icon = 'res/x1_speed.png'
            self._game.iters_per_second -= 30
        self._game_timer_event.timeout = 1 / self._game.iters_per_second
        self._current_speed_is_slow = not self._current_speed_is_slow

    def start_game(self):
        self._running = True
        self.start_stop_icon = 'res/stop_game.png'

    def stop_game(self):
        self._running = False
        self.start_stop_icon = 'res/play_game.png'

    @property
    def game(self):
        return self._game

    def _make_iteration(self, dt):
        if self._running:
            self._game.make_game_iteration()
        self.update(dt)

    def _update_background_size(self):
        background = Image(self._game.current_level.map_path)
        Window.size = (background.width, background.height)

    @staticmethod
    def _set_color(r, g, b):
        Color(r / 255, g / 255, b / 255)

    @staticmethod
    def _set_hp_bar_color(hp_percent):
        if hp_percent > 0.5:
            GameView._set_color(101, 230, 66)
        elif hp_percent > 0.25:
            GameView._set_color(244, 229, 66)
        else:
            GameView._set_color(219, 40, 24)

    def update(self, dt):
        self.gold = f'Gold: {self._game.current_level.gold}\n'
        self.hp = f'Hp: {self._game.current_level.hp}\n'
        self.wave = f'Wave: {self.game.current_level.current_wave}\n'

        with self.canvas:
            self.canvas.clear()
            Rectangle(pos=(0, 0), size=Window.size,
                      source=self._game.current_level.map_path)

            for obj in sorted(GameObject.objects, key=lambda o: -o.location.y):
                pos = obj.location
                img = Image(obj.sprite_path)
                offset = Vector(obj.direction * -img.width / 2,
                                -img.height / 2)

                offset += obj.graphics_offset
                size = (obj.direction * img.width, img.height)
                Rectangle(texture=img.texture, pos=pos + offset, size=size)

                if not obj.friendly:
                    hp_percent = obj.hp / obj.max_hp
                    offset_percent = (1 - hp_percent) / 2

                    hp_bar_size = (size[0] * hp_percent, 3)
                    hp_bar_pos = pos + (size[0] * offset_percent, -5)
                    self._set_hp_bar_color(hp_percent)
                    Rectangle(pos=hp_bar_pos + offset, size=hp_bar_size)
                    Color(1, 1, 1)
