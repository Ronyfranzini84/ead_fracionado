from kivy.app import App
from kivy.uix.screenmanager import Screen


def _formatar_mensagem(texto, cor):
    return f"[color={cor}]{texto}[/color]"


class BasePage(Screen):
    def mostrar_mensagem(self, widget_id, texto, cor="#00CFDB"):
        widget = self.ids.get(widget_id)
        if widget is None:
            return

        widget.markup = True
        widget.text = _formatar_mensagem(texto, cor)

    def mudar_tela(self, nome_tela):
        app = App.get_running_app()
        if app is not None:
            app.mudar_tela(nome_tela)


class LoginPage(BasePage):
    def fazer_login(self):
        email = self.ids.email_input.text.strip()
        senha = self.ids.senha_input.text.strip()

        if not email or not senha:
            self.mostrar_mensagem("mensagem_login", "Preencha e-mail e senha.", "#FF6B6B")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            self.mostrar_mensagem("mensagem_login", "Digite um e-mail valido.", "#FF6B6B")
            return

        self.ids.email_input.text = email.lower()
        self.mostrar_mensagem("mensagem_login", "Campos validados. Abrindo painel.", "#52FF8F")
        self.mudar_tela("homepage")


class CriarLoginPage(BasePage):
    def criar_conta(self):
        email = self.ids.email_input.text.strip().lower()
        senha = self.ids.senha_input.text.strip()
        confirmar_senha = self.ids.confirmar_senha_input.text.strip()

        if not email or not senha or not confirmar_senha:
            self.mostrar_mensagem("mensagem_criar_conta", "Preencha todos os campos.", "#FF6B6B")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            self.mostrar_mensagem("mensagem_criar_conta", "Digite um e-mail valido.", "#FF6B6B")
            return

        if len(senha) < 6:
            self.mostrar_mensagem("mensagem_criar_conta", "Use ao menos 6 caracteres na senha.", "#FF6B6B")
            return

        if senha != confirmar_senha:
            self.mostrar_mensagem("mensagem_criar_conta", "As senhas precisam ser iguais.", "#FF6B6B")
            return

        login_page = self.manager.get_screen("loginpage") if self.manager else None
        if login_page is not None:
            login_page.ids.email_input.text = email
            login_page.ids.senha_input.text = ""
            login_page.mostrar_mensagem("mensagem_login", "Conta preparada. Faca o login.", "#52FF8F")

        self.ids.email_input.text = ""
        self.ids.senha_input.text = ""
        self.ids.confirmar_senha_input.text = ""
        self.mostrar_mensagem("mensagem_criar_conta", "Cadastro local validado com sucesso.", "#52FF8F")
        self.mudar_tela("loginpage")


class HomePage(BasePage):
    pass


class BoxPage(BasePage):
    pass