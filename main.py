#!/usr/bin/python

import sys
import os

from Visualization.LevelPickerScreen import LevelPickerScreen

if sys.version_info[:2] < (3, 6):
    print('This code need Python 3.6 or higher')
    sys.exit(10)

from kivy.config import Config

Config.set('graphics', 'resizable', False)

from Visualization.ChangeLevelScreen import ChangeLevelScreen
from Visualization.LooseGameScreen import LooseGameScreen
from model.Results import Results
import pickle
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition

from Visualization.EndGameScreen import EndGameScreen
from Visualization.GameScreen import GameScreen
from Visualization.MainScreen import MainScreen


class TowerDefenceApp(App):
    def build(self):
        self._results = Results()
        self._load_results()

        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(MainScreen(name='main'))
        game_screen = GameScreen(name='game', results=self._results)
        sm.add_widget(
            LevelPickerScreen(name='pick_lvl', game_screen=game_screen,
                              results=self._results))
        sm.add_widget(LooseGameScreen(name='lose', game_screen=game_screen))
        sm.add_widget(
            ChangeLevelScreen(name='change_level', game_screen=game_screen))
        sm.add_widget(game_screen)
        sm.add_widget(EndGameScreen(name='win', message_image='res/win.png',
                                    game_screen=game_screen))
        return sm

    def _load_results(self):
        if os.path.isfile('results'):
            with open('results', 'rb') as f:
                self._results = pickle.load(f)


if __name__ == '__main__':
    TowerDefenceApp().run()
