import mysql.connector

try:
    # Connect to MySQL server
    connection = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='1234',
        port='3306'
    )
    
    # Create cursor
    cursor = connection.cursor()
    
    # Create database
    cursor.execute("CREATE DATABASE IF NOT EXISTS movsurf;")
    
    print("Database created successfully!")
    
except mysql.connector.Error as err:
    print(f"Error: {err}")
finally:
    if 'connection' in locals():
        connection.close()
