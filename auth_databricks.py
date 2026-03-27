import hashlib
import os
import secrets
from contextlib import closing

try:
    from databricks import sql  # type: ignore[import-not-found]
except ImportError:
    sql = None


class DatabricksAuthService:
    def __init__(self):
        self.server_hostname = os.getenv("DATABRICKS_SERVER_HOSTNAME", "").strip()
        self.http_path = os.getenv("DATABRICKS_HTTP_PATH", "").strip()
        self.access_token = os.getenv("DATABRICKS_TOKEN", "").strip()
        self.catalog = os.getenv("DATABRICKS_CATALOG", "").strip()
        self.schema = os.getenv("DATABRICKS_SCHEMA", "").strip()
        self.users_table = os.getenv("DATABRICKS_USERS_TABLE", "users").strip() or "users"

    @property
    def configurado(self):
        return bool(self.server_hostname and self.http_path and self.access_token and sql is not None)

    def _qualified_table(self):
        parts = [part for part in [self.catalog, self.schema, self.users_table] if part]
        return ".".join(parts)

    def _hash_password(self, senha, salt):
        digest = hashlib.sha256(f"{salt}:{senha}".encode("utf-8")).hexdigest()
        return digest

    def _nova_senha_hash(self, senha):
        salt = secrets.token_hex(16)
        return self._hash_password(senha, salt), salt

    def _connect(self):
        if sql is None:
            raise RuntimeError("Pacote databricks-sql-connector nao instalado.")

        return sql.connect(
            server_hostname=self.server_hostname,
            http_path=self.http_path,
            access_token=self.access_token,
        )

    def autenticar(self, email, senha):
        if not self.configurado:
            return False, "Databricks nao configurado. Defina as variaveis de ambiente."

        try:
            with closing(self._connect()) as conn, closing(conn.cursor()) as cursor:
                table = self._qualified_table()
                cursor.execute(
                    f"SELECT senha_hash, senha_salt FROM {table} WHERE email = ? LIMIT 1",
                    [email],
                )
                row = cursor.fetchone()

            if row is None:
                return False, "Usuario nao encontrado."

            senha_hash, senha_salt = row
            senha_digitada_hash = self._hash_password(senha, senha_salt)
            if senha_digitada_hash != senha_hash:
                return False, "Senha incorreta."

            return True, "Login realizado com sucesso."
        except Exception as exc:
            return False, f"Falha ao autenticar no Databricks: {exc}"

    def criar_conta(self, email, senha):
        if not self.configurado:
            return False, "Databricks nao configurado. Defina as variaveis de ambiente."

        try:
            with closing(self._connect()) as conn, closing(conn.cursor()) as cursor:
                table = self._qualified_table()
                cursor.execute(
                    f"SELECT 1 FROM {table} WHERE email = ? LIMIT 1",
                    [email],
                )
                if cursor.fetchone() is not None:
                    return False, "Ja existe conta com este e-mail."

                senha_hash, senha_salt = self._nova_senha_hash(senha)
                cursor.execute(
                    f"INSERT INTO {table} (email, senha_hash, senha_salt, criado_em) VALUES (?, ?, ?, current_timestamp())",
                    [email, senha_hash, senha_salt],
                )
                conn.commit()

            return True, "Conta criada com sucesso."
        except Exception as exc:
            return False, f"Falha ao criar conta no Databricks: {exc}"


auth_service = DatabricksAuthService()
