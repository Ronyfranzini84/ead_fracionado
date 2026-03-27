import hashlib
import os
import secrets
import sqlite3
from contextlib import closing
from pathlib import Path


class SQLiteAuthService:
    def __init__(self):
        db_path = os.getenv("SQLITE_DB_PATH", "").strip()
        if db_path:
            self._db_path = Path(db_path)
        else:
            self._db_path = Path(__file__).resolve().parent / "usuarios.db"

        self._inicializar_banco()

    def _inicializar_banco(self):
        with closing(sqlite3.connect(self._db_path)) as conn, closing(conn.cursor()) as cursor:
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    email      TEXT PRIMARY KEY,
                    senha_hash TEXT NOT NULL,
                    senha_salt TEXT NOT NULL,
                    criado_em  TEXT NOT NULL DEFAULT (datetime('now'))
                )
                """
            )
            conn.commit()

    def _hash_password(self, senha, salt):
        return hashlib.sha256(f"{salt}:{senha}".encode("utf-8")).hexdigest()

    def _nova_senha_hash(self, senha):
        salt = secrets.token_hex(16)
        return self._hash_password(senha, salt), salt

    def autenticar(self, email, senha):
        try:
            with closing(sqlite3.connect(self._db_path)) as conn, closing(conn.cursor()) as cursor:
                cursor.execute(
                    "SELECT senha_hash, senha_salt FROM users WHERE email = ? LIMIT 1",
                    (email,),
                )
                row = cursor.fetchone()

            if row is None:
                return False, "Usuario nao encontrado."

            senha_hash, senha_salt = row
            if self._hash_password(senha, senha_salt) != senha_hash:
                return False, "Senha incorreta."

            return True, "Login realizado com sucesso."
        except Exception as exc:
            return False, f"Falha ao autenticar: {exc}"

    def criar_conta(self, email, senha):
        try:
            with closing(sqlite3.connect(self._db_path)) as conn, closing(conn.cursor()) as cursor:
                cursor.execute(
                    "SELECT 1 FROM users WHERE email = ? LIMIT 1",
                    (email,),
                )
                if cursor.fetchone() is not None:
                    return False, "Ja existe conta com este e-mail."

                senha_hash, senha_salt = self._nova_senha_hash(senha)
                cursor.execute(
                    "INSERT INTO users (email, senha_hash, senha_salt) VALUES (?, ?, ?)",
                    (email, senha_hash, senha_salt),
                )
                conn.commit()

            return True, "Conta criada com sucesso."
        except Exception as exc:
            return False, f"Falha ao criar conta: {exc}"
