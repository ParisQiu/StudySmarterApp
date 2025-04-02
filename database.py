# database.py
import psycopg
from psycopg import OperationalError
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def create_connection():
    """
    Create and return a new PostgreSQL database connection using credentials
    from environment variables.

    Returns:
        connection: psycopg connection object if successful; otherwise, None.
    """
    try:
        host = os.getenv("DB_HOST")
        db_name = os.getenv("DB_NAME")
        db_user = os.getenv("DB_USER")
        db_password = os.getenv("DB_PASSWORD")
        db_port = os.getenv("DB_PORT")

        if not all([host, db_name, db_user, db_password, db_port]):
            raise ValueError("Missing required database configuration in environment variables")

        conn = psycopg.connect(
            host=host,
            dbname=db_name,
            user=db_user,
            password=db_password,
            port=db_port
        )
        print("Database connection successful")
        return conn
    except OperationalError as e:
        print(f"OperationalError: {e}")
        return None
    except ValueError as e:
        print(f"ValueError: {e}")
        return None

def init_db():
    """
Initialize the database by creating tables defined in schema.sql.
The function checks if a known table (e.g., 'comments') exists. If it does,
it assumes that the database is already initialized.

Returns:
bool: True if tables are created or already exist; False if an error occurs.
    """
    conn = create_connection()
    if conn is None:
        print("Failed to initialize database: No connection")
        return False

    try:
        # Use a context manager so that commit/rollback and cleanup are handled automatically.
        with conn:
            with conn.cursor() as cursor:
                # Check if the 'comments' table exists
                cursor.execute(
                    "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'comments')"
                )
                exists = cursor.fetchone()
                if exists and exists[0]:
                    print("Database tables already exist, skipping creation")
                    return True

                # Read SQL commands from schema.sql
                with open('schema.sql', 'r') as f:
                    sql_commands = f.read()

                # Split and execute each non-empty SQL command
                commands = sql_commands.split(';')
                for command in commands:
                    command = command.strip()
                    if command:
                        cursor.execute(command)

                # Commit is automatically handled by the 'with conn:' block.
                print("Database tables created successfully")
                return True
    except Exception as e:
        # Even though the context manager handles rollback, we catch and log the exception.
        print(f"Error creating tables: {e}")
        return False
    finally:
        conn.close()

if __name__ == '__main__':
    if init_db():
        print("Database initialization test passed.")
    else:
        print("Database initialization test failed.")
        