import uuid
import json
import pandas
import openpyxl
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
jsonInsert = """insert into script select * from json_populate_recordset(NULL::script, %s)"""
deleteData = "DELETE FROM script WHERE name = 'chris'"
getData = "SELECT * FROM script"
updateData = """UPDATE script SET eyecolor = 'blue' WHERE id = 'f0aace9c53c4401182f3e7bf44ba9d04'"""

excel = pandas.read_excel("dataBase_ids.xlsx")

i = 0
while i < len(excel):
    ids = excel['ids'].iloc[i]
    i+= 1
    columnValue = [{'name':'isCustomerOnAlex','value':'Yes'}]
    valuesList = list(columnValue)
    updateDataWithId = '''UPDATE script SET characteristic = jsonb_set(data, %s) WHERE id = %s'''
    jsonArray = [{"name":"isCustomerOnAlex","value":"Yes"}]
    print(ids)
    myCursor.execute(updateDataWithId,(valuesList,ids))

data = ('chris', 'New Jersey',uuid.uuid4().hex)

#If you want to insert an array you can use [{jsonArrayData}]
jsonData = [{"name": "Tom Hanks", "address": "New York", "id": uuid.uuid4().hex,"age":75},
            {"name": "Keanue Reeves", "address": "New York", "id": uuid.uuid4().hex,"age":48},
            {"name": "Brad Pitt", "address": "New York", "id": uuid.uuid4().hex,"age":51}]

#converts data to JSON format
dumps = json.dumps(jsonData)

# myCursor.execute(jsonInsert,(dumps,))


myCursor.execute(getData)
record = myCursor.fetchall()
json_dump = json.dumps(record)

print(json_dump)

myCursor.close()
