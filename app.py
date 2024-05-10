import os
from flask import Flask, request, render_template, jsonify
import time
from categorize_with_chatgpt import categorize_text_with_chatgpt
from categorize_with_gigachat import categorize_text_with_gigachat
from database_connect import save_data, close_connection, connect_to_db
from generate_sql_queries import generate_sql_queries
from dotenv import load_dotenv

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

load_dotenv('config.env')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    categories = request.form['category'].split(',')
    categories = [category.strip() for category in categories if category.strip()]

    api_choice = request.form['apiChoice']
    response_format = request.form.get('responseFormat', 'text')
    max_tokens = int(request.form.get('max_tokens', 0))
    model_choice = request.form.get('modelChoice')
    api_key = request.form.get('apiKey')

    results = {}

    start_time = time.time()
    for category in categories:
        category = category.strip()
        if api_choice == 'chatgpt':
            result, total_tokens_used = categorize_text_with_chatgpt(api_key, text, category, model_choice, max_tokens)
        elif api_choice == 'gigachat':
            result, total_tokens_used = categorize_text_with_gigachat(api_key, text, category, model_choice, max_tokens)

        if 'error' in result:
            results[category] = f'Ошибка: {result["error"]}'
        else:
            pattern = category + ": "
            cleaned_text = result.replace(pattern, '')
            results[category] = cleaned_text

    end_time = time.time()
    print(f'Общее время выполнения: {end_time - start_time} секунд')

    if results:
        conn = connect_to_db(os.getenv('DB_HOST'), os.getenv('DB_PORT'), os.getenv('DB_NAME'), os.getenv('DB_USER'),
                             os.getenv('DB_PASSWORD'))
        save_data(conn, text, results, total_tokens_used, api_choice, model_choice)
        close_connection(conn)
        if response_format == 'json':
            return jsonify({
                "request_text": text,
                "prompt_parameters": f'total_tokens_used: {total_tokens_used}, api_choice: {api_choice}, model_choice: {model_choice}',
                "information": [
                    {"category": key, "text": value}
                    for key, value in results.items()
                ]
            })
        elif response_format == 'sql':
            sql_queries = generate_sql_queries(text, results, total_tokens_used, api_choice, model_choice)
            return jsonify({
                'sql_queries': sql_queries
            })
        elif response_format == 'text':
            initial_data = text
            output_data = "\n\n"
            for category, data in results.items():
                output_data += f"\n{category}:\n{data}\n\n"
            return jsonify({'\nВходные данные \n': initial_data, '\n\nВыходные данные': output_data})
    else:
        return jsonify({'error': 'Возникла непредвиденная ошибка'}), 500


if __name__ == '__main__':
    app.run(debug=True)
