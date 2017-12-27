from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.screenmanager import Screen


class ChangeLevelScreen(Screen):
    game_screen = ObjectProperty(None)
    stars_img = StringProperty('')
