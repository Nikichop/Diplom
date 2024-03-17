import openai


def categorize_text_with_chatgpt(text, category, temperature=0):
    try:
        prompt = f"Изложи информацию только о параметре '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие темы. Излагай информацию, по формату, так, как указывают в досье на пациента/преступника. Формат ответа должен выглядеть следующим образом: {category}: информация только о {category}"
        response = openai.chat.completions.create(
            messages=[
                {"role": "system", "content": "Вы являетесь ассистентом, который должен строго следовать инструкциям."},
                {"role": "user", "content": prompt},
            ],
            model="gpt-3.5-turbo",
            temperature=temperature,
        )

        categorized_text = response.choices[0].message.content
        return categorized_text

    except Exception as e:
        return {'error': str(e)}
