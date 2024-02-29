import psycopg2


def insert_into_database(host, port, dbname, user, password, data):
    conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    for index, item in enumerate(data, start=1):
        cursor.execute(
            "INSERT INTO categories_info (category_name, category_info) VALUES (%s, %s)",
            (item['category'], item['text'])
        )
    conn.commit()
    cursor.close()
    conn.close()
