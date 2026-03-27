from pathlib import Path

from kivy.app import App
from kivy.lang import Builder

from botoes import ImageButton
from telas import BoxPage, CriarLoginPage, HomePage, LoginPage


class MainApp(App):
    title = "Conferencia EAD Fracionado"

    def load_kv(self, filename=None):
        return None

    def mudar_tela(self, id_tela):
        screen_manager = self.root.ids.get("screen_manager")  # type: ignore[union-attr]
        if screen_manager is None or id_tela not in screen_manager.screen_names:
            return

        screen_manager.current = id_tela

    def build(self):
        base_dir = Path(__file__).resolve().parent
        return Builder.load_file(str(base_dir / "main.kv"))


if __name__ == "__main__":
    MainApp().run()
