import psycopg2
from psycopg2.extras import execute_values
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def load_data(df):
    try:
        connection = psycopg2.connect(
            dbname="postgres",
            user="your_username",       # Default user: postgres
            password="your_password",   # Default password: postgres
            host="localhost",
            port="5432"
        )
        connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = connection.cursor()

        database_name = "apartment_db"
        cursor.execute(f"SELECT 1 FROM pg_database WHERE datname = '{database_name}';")
        exists = cursor.fetchone()

        if not exists:
            cursor.execute(f"CREATE DATABASE {database_name};")

        cursor.close()
        connection.close()

        connection = psycopg2.connect(
            dbname=database_name,
            user="your_username",       # Default user: postgres
            password="your_password",   # Default password: postgres
            host="localhost",
            port="5432"
        )
        cursor = connection.cursor()
        table_name = "chung_cu"

        cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}');")
        exists = cursor.fetchone()[0]
        if not exists:
            create_table_query = f'''
                CREATE TABLE {table_name} (
                    "ID" CHAR(10) PRIMARY KEY,
                    "Giá(tỷ)" FLOAT,
                    "Diện tích(m2)" FLOAT,
                    "Giá/m2" FLOAT,
                    "Phòng ngủ" INT,
                    "Phòng tắm" INT,
                    "Địa chỉ" TEXT
                );
            '''
            cursor.execute(create_table_query)
        cursor.execute(f"TRUNCATE TABLE {table_name};")

        values = [tuple(row) for row in df.to_numpy()]
        insert_query = f'INSERT INTO {table_name} ("ID", "Giá(tỷ)", "Diện tích(m2)", "Giá/m2", "Phòng ngủ", "Phòng tắm", "Địa chỉ") VALUES %s'
        execute_values(cursor, insert_query, values)

        connection.commit()
        cursor.close()
        connection.close()
    except Exception as e:
        print("Error loading data:", e)