import os

import sqlalchemy


def connect_tcp_socket() -> sqlalchemy.engine.base.Engine:
    db_host = os.environ["DATABASE_HOST"]
    db_user = os.environ["DATABASE_USER"]
    db_pass = os.environ["DATABASE_PASS"]
    db_name = os.environ["DATABASE_NAME"]
    # db_port = int(os.environ.get("DATABASE_PORT", 3306))
    db_port = int(os.environ["DATABASE_PORT"])

    engine = sqlalchemy.create_engine(
        sqlalchemy.engine.url.URL.create(
            drivername="mysql+pymysql",
            username=db_user,
            password=db_pass,
            host=db_host,
            port=db_port,
            database=db_name,
        ),
    )
    return engine


def seed_users(conn):
    print("🌱 Seeding users...")

    conn.execute(sqlalchemy.text("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL
        )
    """))

    conn.execute(sqlalchemy.text("""
        INSERT INTO users (name, email)
        VALUES
            ('Alice', 'alice@example.com'),
            ('Bob', 'bob@example.com'),
            ('Charlie', 'charlie@example.com')
        ON DUPLICATE KEY UPDATE name=VALUES(name), email=VALUES(email)
    """))

    print("✅ Seeded users!")


if __name__ == "__main__":
    print("🔌 Connecting to Cloud SQL...")

    try:
        engine = connect_tcp_socket()
        with engine.begin() as conn:  # ← begin() に変更すると自動で commit される
            print("✅ Connected!")

            seed_users(conn)

            result = conn.execute(sqlalchemy.text("SHOW TABLES"))
            tables = result.fetchall()

            if tables:
                print("📋 Tables in database:")
                for (table_name,) in tables:
                    print(f" - {table_name}")
            else:
                print("⚠️ No tables found in the database.")

    except Exception as e:
        print("❌ Connection failed or error occurred:")
        print(e)
