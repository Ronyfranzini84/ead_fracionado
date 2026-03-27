from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.behaviors import ButtonBehavior


__all__ = ["ImageButton", "LabelButton"]

class ImageButton(ButtonBehavior, Image):
    pass

class LabelButton(ButtonBehavior, Label):
    pass
