import sys
import sqlite3
from pathlib import Path


Product = tuple[int, str, int]


class BikeManager:
    def __init__(self, db_path: str | Path | None = None) -> None:
        if db_path is not None:
            self.db_path = Path(db_path)
        elif getattr(sys, "frozen", False):
            self.db_path = Path(sys.executable).resolve().with_name("MyProduct.db")
        else:
            self.db_path = Path(__file__).with_name("MyProduct.db")
        self.connection = sqlite3.connect(self.db_path)
        try:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS MyProduct (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    price INTEGER NOT NULL CHECK (price >= 0)
                )
                """
            )
            self.connection.commit()
        except sqlite3.Error:
            self.connection.close()
            raise

    def insert_product(self, name: str, price: int) -> None:
        try:
            self.connection.execute(
                "INSERT INTO MyProduct (name, price) VALUES (?, ?)",
                (name, price),
            )
            self.connection.commit()
        except sqlite3.Error:
            self.connection.rollback()
            raise

    def update_product(self, product_id: int, name: str, price: int) -> int:
        try:
            cursor = self.connection.execute(
                "UPDATE MyProduct SET name = ?, price = ? WHERE id = ?",
                (name, price, product_id),
            )
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error:
            self.connection.rollback()
            raise

    def delete_product(self, product_id: int) -> int:
        try:
            cursor = self.connection.execute(
                "DELETE FROM MyProduct WHERE id = ?", (product_id,)
            )
            self.connection.commit()
            return cursor.rowcount
        except sqlite3.Error:
            self.connection.rollback()
            raise

    def select_products(self, name_filter: str = "") -> list[Product]:
        if name_filter:
            cursor = self.connection.execute(
                """
                SELECT id, name, price
                FROM MyProduct
                WHERE name LIKE ?
                ORDER BY id
                """,
                (f"%{name_filter}%",),
            )
        else:
            cursor = self.connection.execute(
                "SELECT id, name, price FROM MyProduct ORDER BY id"
            )
        return cursor.fetchall()

    def close(self) -> None:
        self.connection.close()
