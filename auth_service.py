from auth_databricks import DatabricksAuthService
from auth_sqlite import SQLiteAuthService

_databricks = DatabricksAuthService()
_sqlite = SQLiteAuthService()


def _backend():
    """Usa Databricks se estiver configurado; caso contrario usa SQLite local."""
    if _databricks.configurado:
        return _databricks
    return _sqlite


class AuthService:
    @property
    def usando_databricks(self):
        return _databricks.configurado

    def autenticar(self, email, senha):
        return _backend().autenticar(email, senha)

    def criar_conta(self, email, senha):
        return _backend().criar_conta(email, senha)


auth_service = AuthService()
