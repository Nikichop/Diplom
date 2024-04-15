def generate_sql_queries(request_text, results):
    sql_queries = [
        "CREATE TABLE IF NOT EXISTS request (id SERIAL PRIMARY KEY, request_text TEXT, date DATE, prompt_parameters TEXT);",
        "CREATE TABLE IF NOT EXISTS response (id SERIAL PRIMARY KEY, request_id INTEGER REFERENCES request (id), parameter_name TEXT, parameter_value TEXT);",
        f"INSERT INTO request (request_text, date, prompt_parameters) VALUES ('{request_text}', now(), '');"]

    for category, text in results.items():
        sql_queries.append(
            f"INSERT INTO response (request_id, parameter_name, parameter_value) SELECT id, '{category}', '{text}' FROM request WHERE request_text = '{request_text}';")

    return "\n".join(sql_queries)
