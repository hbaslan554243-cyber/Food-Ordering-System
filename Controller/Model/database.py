import mysql.connector
from mysql.connector import Error

class Database:
    """Handles database connection"""

    @staticmethod
    def get_connection():
        """Create and return database connection"""
        try:
            print("🔄 Attempting database connection...")
            connection = mysql.connector.connect(
                host='localhost',
                database='database_eatogo',
                user='root',
                password='',
                autocommit=False,
                use_pure=True
            )
            if connection.is_connected():
                print("✅ Database connection successful")
                return connection
        except Error as e:
            print(f"❌ Database Error: {e}")
            import traceback
            traceback.print_exc()
            return None
        except Exception as e:
            print(f"❌ Unexpected Error: {e}")
            import traceback
            traceback.print_exc()
            return None