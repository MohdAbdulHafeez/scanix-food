from database.database import (
    check_database_connection,
)

if __name__ == "__main__":
    status = check_database_connection()
    print(f"Database Status: {status}")