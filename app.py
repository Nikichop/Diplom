from flask import Flask, request, render_template, jsonify
import openai
from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os

app = Flask(__name__)


def categorize_text_with_chatgpt(text, category):
    try:
        prompt = f"Изложи информацию только о категории '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие аспекты."
        response = openai.chat.completions.create(
            messages=[
                {"role": "system", "content": "Вы являетесь ассистентом, который должен строго следовать инструкциям."},
                {"role": "user", "content": prompt},
            ],
            model="gpt-3.5-turbo",
            temperature=0.8,
        )

        categorized_text = response.choices[0].message.content
        return categorized_text

    except Exception as e:
        return {'error': str(e)}


def categorize_text_with_gigachat(text, category):
    try:
        prompt = f"Изложи информацию только о категории '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие аспекты."
        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content="Вы являетесь ассистентом, который должен строго следовать инструкциям.",
                ),
            ],
            temperature=0.8,
        )

        with GigaChat(credentials=os.getenv('GIGACHAT_CREDENTIALS'), verify_ssl_certs=False) as giga:
            payload.messages.append(Messages(role=MessagesRole.USER, content=prompt))
            response = giga.chat(payload)
            return response.choices[0].message.content

    except Exception as e:
        return {'error': str(e)}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    categories = request.form['category'].split(',')
    api_choice = request.form['apiChoice']

    results = {}

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

    if results:
        return jsonify(results)
    else:
        return jsonify({'error': 'Нет данных для обработки'}), 500


if __name__ == '__main__':
    app.run(debug=True)
