from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout


class TowerButton(BoxLayout):
    image = StringProperty('')
    bt = ObjectProperty(None)
    bt_text = StringProperty('')
    description = StringProperty('')
