from flask import Flask, request, render_template, jsonify
import openai
from gigachat import GigaChat
import os

app = Flask(__name__)


def categorize_text_with_chatgpt(text, category):
    try:
        prompt = f"Изложи информацию о категории '{category}' в следующем тексте: '{text}'. Сфокусируйся на выбранной категории и старайся исключать другие"
        response = openai.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
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
        prompt = f"Изложи информацию о категории '{category}' в следующем тексте: '{text}'. Сфокусируйся на выбранной категории и старайся исключать другие"
        with GigaChat(credentials=os.getenv('GIGACHAT_CREDENTIALS'), verify_ssl_certs=False) as giga:
            response = giga.chat(prompt)
            return response.choices[0].message.content

    except Exception as e:
        return {'error': str(e)}


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/process', methods=['POST'])
def process():
    text = request.form['text']
    category = request.form['category']
    api_choice = request.form['apiChoice']

    if api_choice == 'chatgpt':
        result = categorize_text_with_chatgpt(text, category)
    elif api_choice == 'gigachat':
        result = categorize_text_with_gigachat(text, category)

    if 'error' in result:
        return jsonify(result), 500
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
