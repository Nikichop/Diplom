def generate_sql_queries(request_text, results, max_tokens, api_choice, model_choice):
    sql_queries = [
        "CREATE TABLE IF NOT EXISTS request (id SERIAL PRIMARY KEY, request_text TEXT, date DATE, prompt_parameters TEXT);",
        "CREATE TABLE IF NOT EXISTS response (id SERIAL PRIMARY KEY, request_id INTEGER REFERENCES request (id), parameter_name TEXT, parameter_value TEXT);",
        "DO $$",
        "DECLARE",
        "    request_id integer;",
        "BEGIN",
        f"    INSERT INTO request (request_text, date, prompt_parameters) VALUES ('{request_text}', now(), 'max_tokens: {max_tokens}, api_choice: {api_choice}, model_choice: {model_choice}') RETURNING id INTO request_id;",
    ]

    for category, text in results.items():
        sql_queries.append(
            f"    INSERT INTO response (request_id, parameter_name, parameter_value) VALUES (request_id, '{category}', '{text}');")

    sql_queries.append("END $$;")

    return "\n".join(sql_queries)
