import mysql.connector
from mysql.connector import Error

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host="interchange.proxy.rlwy.net",
            port=34610,
            user="root",
            password="YgCpmrXuBowXTSsFYTbNBXojTJcviRQb",
            database="railway"
        )
        return connection
    except Error as e:
        print(f"Error connecting to MySQL: {e}")
        return None
