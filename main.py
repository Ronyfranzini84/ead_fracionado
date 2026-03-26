from kivy.app import App
from kivy.lang import Builder
from botoes import *
import requests
import os
from functools import partial
from datetime import date
from kivy.uix.screenmanager import ScreenManager, Screen


class LoginPage(Screen):   
    pass


class HomePage(Screen, Image):
    pass

class MainApp(App):
    def mudar_tela(self, id_tela):
        self.root.ids["screen_manager"].current = id_tela

MainApp().run()
