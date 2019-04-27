import psycopg2
from psycopg2 import Error

try:
    connection = psycopg2.connect(user="xtkmmxdm",
                                  password="5R5Gx8ky14x6jQbRJ0ppKdNtuIVO4Mci",
                                  host="manny.db.elephantsql.com",
                                  port="5432",
                                  database="xtkmmxdm")
    cursor = connection.cursor()

    create_table_query = '''
    CREATE TABLE mobile
          (ID INT PRIMARY KEY     NOT NULL,
          MODEL           TEXT    NOT NULL,
          PRICE         REAL); 
          '''

    drop_table_query = '''
    DROP TABLE mobile CASCADE; 
          '''

    cursor.execute(drop_table_query)
    connection.commit()
    print("Execution successful")
except (Exception, psycopg2.DatabaseError) as error:
    print("Error while creating PostgreSQL table", error)
finally:
    if (connection):
        cursor.close()
        connection.close()
        print("PostgreSQL connection is closed")
