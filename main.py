from kivy.app import App
from kivy.lang import Builder
from botoes import *
import requests
import os
from functools import partial
from datetime import date
from kivy.uix.screenmanager import ScreenManager, Screen
from telas import *


class MainApp(App):
    def mudar_tela(self, id_tela):
        self.root.ids["screen_manager"].current = id_tela # type: ignore

    def build(self):
        return Builder.load_file("main.kv")

MainApp().run()
