import uuid
import json
import psycopg2
from psycopg2 import OperationalError


def connect_to_database():
    try:
        connection = psycopg2.connect(
            database='postgres',
            user='postgres',
            password='postgres123',  # Don't forget to include your password
            host='localhost',
            port='5432'
        )
        connection.autocommit = True
        print("Connection successful!")
        return connection
    except OperationalError as e:
        print(f"Error: {e}")
        return None

myCursor = connect_to_database().cursor()

sql = "INSERT INTO script (name,address,id) VALUES (%s,%s,%s)"
jsonInsert = """insert into script select * from json_populate_record(NULL::script, %s)"""
deleteData = "DELETE FROM script WHERE name = 'chris'"
getData = "SELECT * FROM script"

data = ('chris', 'New Jersey',uuid.uuid4().hex)

#If you want to insert an array you can use [{jsonArrayData}]
jsonData = {"name": "Silvio Dante","address": "New Balance","id": uuid.uuid4().hex}

#converts data to JSON format
dumps = json.dumps(jsonData)

myCursor.execute(jsonInsert,(dumps,))

myCursor.execute(getData)
record = myCursor.fetchall()
json_dump = json.dumps(record)

print(json_dump)

myCursor.close()
