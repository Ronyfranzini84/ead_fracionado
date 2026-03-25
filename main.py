from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder

class HomePage(Screen):
    pass

class AjustesPage(Screen):
    pass

GUI = Builder.load_file("main.kv")
class MainApp(App):
    def build(self):
        return GUI
    
    def mudar_tela(self, id_tela):
        print(id_tela)
        gerenciadir_telas = self.root.ids["screen_manager"]
        gerenciadir_telas.current = id_tela
    
MainApp().run()
