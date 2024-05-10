import openai


def categorize_text_with_chatgpt(api_key, text, category, model, max_tokens=100):
    openai.api_key = api_key
    try:
        prompt = f"Изложи информацию только о параметре '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие темы. Излагай информацию по формату так, как указывают в досье на пациента/преступника. Формат ответа должен выглядеть следующим образом: {category}: информация только о {category}."
        response = openai.chat.completions.create(
            messages=[
                {"role": "system", "content": "Вы являетесь ассистентом, который должен строго следовать инструкциям."},
                {"role": "user", "content": prompt},
            ],
            model=model,
            max_tokens=max_tokens,
        )

        categorized_text = response.choices[0].message.content
        total_tokens_used = response.usage.total_tokens
        if total_tokens_used > max_tokens:
            return {
                'error': f'Недостаточно токенов. Необходимо установить более высокое значение (текущее использование: {total_tokens_used}, лимит: {max_tokens}).'}, 0
        else:
            return categorized_text, total_tokens_used


    except UnicodeEncodeError:
        return {
            'error': f'Убедитесь, что API-ключ содержит только допустимые символы, проверьте их на соответствие UTF-8'
        }

    except Exception as e:
        if e.response.status_code == 403:
            return {'error': 'Регион не поддерживается API ChatGPT. Попробуйте воспользоваться VPN'}, 0
        elif e.response.status_code == 401:
            return {'error': 'Неверный API-ключ.'}, 0
        else:
            return {'error': str(e)}, 0
