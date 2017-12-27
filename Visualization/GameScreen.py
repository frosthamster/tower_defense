import pickle
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import Screen

from Visualization.TowersMenu import TowersMenu
from Visualization.UpgradeMenu import UpgradeMenu
from model.GameObject import GameObject
from model.Tower import Tower
from model.Towers import Mage, Archers


class GameScreen(Screen):
    game_view = ObjectProperty(None)
    towers_menu_layout = ObjectProperty(None)
    results = ObjectProperty(None)

    def __init__(self, **kw):
        super().__init__(**kw)
        self.game_view.game.game_end += self._on_game_end
        self.game_view.game.level_changed += self._on_level_changed
        self.game_view.game.level_end_with_result += self._handle_level_result
        self._towers_menu = TowersMenu()
        self._towers_menu.mage_button.bt.bind(
            on_press=lambda _: self._mage_bt_pressed())
        self._towers_menu.archers_button.bt.bind(
            on_press=lambda _: self._archers_bt_pressed())
        self._towers_menu.close_button.bind(
            on_press=lambda _: self._close_towers_menu_bt_pressed())
        self._selected_tower_location = None
        self._selected_tower = None
        self._upgrade_menu = None

    def _close_towers_menu_bt_pressed(self):
        if self._towers_menu is not None:
            self.towers_menu_layout.remove_widget(self._towers_menu)
        self._selected_tower_location = None

    def _close_tower_upgrade_bt_pressed(self):
        if self._upgrade_menu is not None:
            self.towers_menu_layout.remove_widget(self._upgrade_menu)
        self._selected_tower = None

    def _handle_level_result(self, level_number, result):
        self.results.add_level_result(level_number, result)
        with open('results', 'wb') as f:
            pickle.dump(self.results, f)
        self.manager.get_screen('change_level').stars_img = \
            f'res/{result}stars.png'

    def _on_level_changed(self):
        self.game_view.stop_game()
        self.manager.current = 'change_level'
        self._close_tower_upgrade_bt_pressed()
        self._close_towers_menu_bt_pressed()

    def _build_tower(self, tower_cls):
        if self.game_view.game.try_build_tower(tower_cls,
                                               self._selected_tower_location):
            self._close_towers_menu_bt_pressed()

    def _mage_bt_pressed(self):
        self._build_tower(Mage)

    def _archers_bt_pressed(self):
        self._build_tower(Archers)

    def _upgrade_pressed(self, cost):
        if self.game_view.game.current_level.gold >= cost:
            self.game_view.game.current_level.gold -= cost
            self._selected_tower.upgrade()
            self._close_tower_upgrade_bt_pressed()

    def on_touch_down(self, touch):
        ret = super().on_touch_down(touch)

        pos = touch.pos
        locations = self.game_view.game.current_level.towers_locations
        for tower_location in locations:
            if (tower_location - pos).length() < 30:
                if self._selected_tower is not None:
                    self._close_tower_upgrade_bt_pressed()
                if self._selected_tower_location is None:
                    self.towers_menu_layout.add_widget(self._towers_menu)
                self._selected_tower_location = tower_location
                return True

        for tower in (obj
                      for obj in GameObject.objects
                      if isinstance(obj, Tower)
                      if obj.upgrade_info is not None
                      if (obj.location - pos).length() < 30):
            if self._selected_tower_location is not None:
                self._close_towers_menu_bt_pressed()

            self._close_tower_upgrade_bt_pressed()
            cost, img, description = tower.upgrade_info
            self._upgrade_menu = UpgradeMenu(img=img, cost=str(cost),
                                             description=description)
            self._upgrade_menu.close_button.bind(
                on_press=lambda _: self._close_tower_upgrade_bt_pressed())
            self._upgrade_menu.upgrade_bt.bt.bind(
                on_press=lambda _: self._upgrade_pressed(cost))
            self.towers_menu_layout.add_widget(self._upgrade_menu)
            self._selected_tower = tower
            return True

        return ret

    def _on_game_end(self, is_win):
        self.game_view.stop_game()
        if is_win:
            self.game_view.stop_game()
            self.manager.current = 'win'
        else:
            self.game_view.stop_game()
            self.manager.current = 'lose'
