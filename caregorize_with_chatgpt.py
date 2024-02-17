import openai


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
