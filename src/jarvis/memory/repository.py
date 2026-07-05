import sqlite3
from pathlib import Path


class ConversationRepository:
    """Handles all database operations for conversation history."""

    def __init__(self) -> None:
        # Project root/
        project_root = Path(__file__).resolve().parents[3]

        # Create data/ if it doesn't exist
        data_dir = project_root / "data"
        data_dir.mkdir(exist_ok=True)

        # data/jarvis.db
        self.database_path = data_dir / "jarvis.db"

        # Open a connection to the database
        self.connection = sqlite3.connect(self.database_path)

        # Return rows as dictionaries
        self.connection.row_factory = sqlite3.Row

        self._create_table()

    def _create_table(self) -> None:
        """Create the messages table if it does not already exist."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT NOT NULL,
                content TEXT NOT NULL
            )
            """
        )

        self.connection.commit()

    def save_message(
        self,
        role: str,
        content: str,
    ) -> None:
        """Save a message to the database."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            INSERT INTO messages(role, content)
            VALUES (?, ?)
            """,
            (role, content),
        )

        self.connection.commit()

    def load_messages(self) -> list[dict]:
        """Load all messages from the database."""

        cursor = self.connection.cursor()

        cursor.execute(
            """
            SELECT role, content
            FROM messages
            ORDER BY id
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "role": row["role"],
                "content": row["content"],
            }
            for row in rows
        ]

    def clear(self) -> None:
        """Delete all stored messages."""

        cursor = self.connection.cursor()

        cursor.execute("DELETE FROM messages")

        self.connection.commit()

    def close(self) -> None:
        """Close the database connection."""

        self.connection.close()