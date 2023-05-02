from typing import Self

import psycopg2

from app.config import DefaultSettings


settings = DefaultSettings()


class DBManager:
    _instance = None

    def __init__(self) -> None:
        self.connection = psycopg2.connect(**settings.database_settings)

    def __new__(cls) -> Self:
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance

    def execute(self, query: str, *args) -> list[tuple]:
        with self.connection:
            with self.connection.cursor() as curs:
                curs.execute(query, args)
                return curs.fetchall()

    def commit(self) -> None:
        self.connection.commit()

    def rollback(self) -> None:
        self.connection.rollback()

    def close(self):
        self.connection.close()
