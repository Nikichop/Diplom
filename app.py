from flask import Flask, request, render_template, jsonify
import time
from caregorize_with_chatgpt import categorize_text_with_chatgpt
from categorize_with_gigachat import categorize_text_with_gigachat
from database_connect import insert_into_database

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    categories = request.form['category'].split(',')
    api_choice = request.form['apiChoice']
    response_format = request.form.get('responseFormat', 'text')  # Добавленный параметр для выбора формата ответа

    results = {}

    start_time = time.time()
    for category in categories:
        category = category.strip()
        if api_choice == 'chatgpt':
            result = categorize_text_with_chatgpt(text, category)
        elif api_choice == 'gigachat':
            result = categorize_text_with_gigachat(text, category)

        if 'error' in result:
            results[category] = f'Ошибка: {result["error"]}'
        else:
            results[category] = result

    end_time = time.time()

    if results:
        print(f'Общее время выполнения: {end_time - start_time} секунд')
        if response_format == 'json':
            return jsonify({
                "information": [
                    {"category": key, "text": value}
                    for key, value in results.items()
                ]
            })
        elif response_format == 'sql':
            db_params = {
                'host': request.form['dbHost'],
                'port': request.form['dbPort'],
                'dbname': request.form['dbName'],
                'user': request.form['dbUser'],
                'password': request.form['dbPassword'],
            }
            data_to_insert = [
                {"category": key, "text": value}
                for key, value in results.items()
            ]
            insert_into_database(**db_params, data=data_to_insert)
            # Сохраняем информацию об успешном сохранении в базе данных вместе с результатами
            return jsonify({
                'success': 'Данные успешно сохранены в базе данных',
                'results': results
            })

        else:
            return jsonify(results)
    else:
        return jsonify({'error': 'Нет данных для обработки'}), 500


if __name__ == '__main__':
    app.run(debug=True)
