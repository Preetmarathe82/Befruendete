import sqlite3

DATABASE_NAME = "befreundete.db"


def get_connection():
    return sqlite3.connect(DATABASE_NAME)


def create_tables():
    connection = get_connection()

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS mistakes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                mistake TEXT NOT NULL,
                correction TEXT NOT NULL,
                topic TEXT NOT NULL,
                count INTEGER NOT NULL DEFAULT 1,
                reviewed INTEGER NOT NULL DEFAULT 0
            )
        """)

        connection.commit()

    finally:
        connection.close()

def check_tables():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type = 'table'
        """)

        tables = cursor.fetchall()

        print("Tables:", tables)


    finally:
        connection.close()

def save_mistake(mistake, correction, topic):
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, count
            FROM mistakes
            WHERE mistake = ?
              AND correction = ?
              AND topic = ?
        """, (mistake, correction, topic))

        existing_mistake = cursor.fetchone()

        if existing_mistake:
            mistake_id, count = existing_mistake

            connection.execute("""
                UPDATE mistakes
                SET count = ?, reviewed = 0
                WHERE id = ?
            """, (count + 1, mistake_id))

        else:
            connection.execute("""
                INSERT INTO mistakes (mistake, correction, topic)
                VALUES (?, ?, ?)
            """, (mistake, correction, topic))

        connection.commit()

    finally:
        connection.close()

def get_mistakes():
    connection = get_connection()

    try:
        cursor = connection.execute("""
            SELECT id, mistake, correction, topic, count, reviewed
            FROM mistakes
            ORDER BY id
        """)

        return cursor.fetchall()

    finally:
        connection.close()


if __name__ == "__main__":
    create_tables()