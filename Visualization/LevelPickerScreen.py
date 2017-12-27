from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen

from Visualization.ImageButton import ImageButton


class LevelPickerScreen(Screen):
    game_screen = ObjectProperty(None)
    results = ObjectProperty(None)
    right_bt_layout = ObjectProperty(None)
    left_bt_layout = ObjectProperty(None)
    play_bt_layout = ObjectProperty(None)
    result_img = StringProperty('res/empty.png')
    map_img = StringProperty()

    def __init__(self, **kw):
        super().__init__(**kw)

        self._play_bt = ImageButton(size_hint=(0.2, 0.1),
                                    source='res/play.png',
                                    on_press=self._play)
        self._right_bt = ImageButton(size_hint=(0.1, 0.1),
                                     source='res/right_bt.png',
                                     on_press=self._on_right_pressed)
        self._left_bt = ImageButton(size_hint=(0.1, 0.1),
                                    source='res/left_bt.png',
                                    on_press=self._on_left_pressed)
        self.left_bt_layout.add_widget(self._left_bt)
        self.right_bt_layout.add_widget(self._right_bt)
        # self.play_bt_layout.add_widget(self._play_bt)

        self._buttons = ((self._play_bt, self.play_bt_layout),
                             (self._left_bt, self.left_bt_layout),
                             (self._right_bt, self.right_bt_layout))

        self._current_level = 0
        self.update()

    @property
    def _res(self):
        return self.results.results

    def update(self):
        map_path, res = self._res[self._current_level]
        last_completed_level = self.results.last_completed_level_index

        for button, layout in self._buttons:
            if button not in layout.children:
                layout.add_widget(button)

        self.map_img = f'res/maps/level{self._current_level+1}.png'
        if self._current_level > last_completed_level + 1:
            self.map_img = f'res/maps/level{self._current_level+1}_gs.png'
            self.play_bt_layout.remove_widget(self._play_bt)

        if last_completed_level >= self._current_level:
            self.result_img = f'res/{res}stars.png'
        else:
            self.result_img = 'res/empty.png'

        if self._current_level == 0:
            self.left_bt_layout.remove_widget(self._left_bt)
        if self._current_level == len(self._res) - 1:
            self.right_bt_layout.remove_widget(self._right_bt)

    def _on_right_pressed(self, s):
        self._current_level += 1
        self.update()

    def _on_left_pressed(self, s):
        self._current_level -= 1
        self.update()

    def _play(self, s):
        self.manager.current = 'game'
        self.manager.get_screen('game').game_view.game.set_level(
            self._current_level)
        self.manager.get_screen('game').game_view.start_game()
