import psycopg2


def insert_into_database(host, port, dbname, user, password, request_text, prompt_parameters, data):
    conn_string = f"host={host} port={port} dbname={dbname} user={user} password={password}"
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    # Вставка в таблицу request и получение id
    cursor.execute(
        "INSERT INTO request (request_text, date, prompt_parameters) VALUES (%s, now(), %s) RETURNING id",
        (request_text, prompt_parameters)
    )
    request_id = cursor.fetchone()[0]
    # Вставка в таблицу response
    for item in data:
        cursor.execute(
            "INSERT INTO response (request_id, parameter_name, parameter_value) VALUES (%s, %s, %s)",
            (request_id, item['category'], item['text'])
        )
    conn.commit()
    cursor.close()
    conn.close()
