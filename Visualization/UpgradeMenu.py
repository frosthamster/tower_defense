from kivy.properties import ObjectProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout


class UpgradeMenu(BoxLayout):
    upgrade_bt = ObjectProperty(None)
    close_button = ObjectProperty(None)
    img = StringProperty()
    description = StringProperty()
    cost = StringProperty()
