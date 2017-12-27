from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.screenmanager import Screen


class EndGameScreen(Screen):
    message_image = StringProperty('')
    background = StringProperty('res/end_game_background.jpg')
    game_screen = ObjectProperty(None)
