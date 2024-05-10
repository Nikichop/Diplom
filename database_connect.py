import psycopg2
from psycopg2 import sql


def connect_to_db(host, port, dbname, user, password):
    conn = psycopg2.connect(
        host=host,
        port=port,
        dbname=dbname,
        user=user,
        password=password
    )
    return conn


def save_data(conn, request_text, results, max_tokens, api_choice, model_choice):
    with conn.cursor() as cursor:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS request (
                id SERIAL PRIMARY KEY,
                request_text TEXT,
                date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                prompt_parameters TEXT
            );
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS response (
                id SERIAL PRIMARY KEY,
                request_id INTEGER REFERENCES request (id),
                parameter_name TEXT,
                parameter_value TEXT
            );
        """)
        cursor.execute(sql.SQL("""
            INSERT INTO request (request_text, date, prompt_parameters)
            VALUES (%s, NOW(), %s)
            RETURNING id;
        """), (request_text.replace('\n', ' '),
               f'max_tokens: {max_tokens}, api_choice: {api_choice}, model_choice: {model_choice}'))
        request_id = cursor.fetchone()[0]
        for category, text in results.items():
            cursor.execute(sql.SQL("""
                INSERT INTO response (request_id, parameter_name, parameter_value)
                VALUES (%s, %s, %s);
            """), (request_id, category, text.replace('\n', ' ')))
        conn.commit()


def close_connection(conn):
    conn.close()
