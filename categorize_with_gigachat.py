from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
from gigachat.exceptions import GigaChatException


def categorize_text_with_gigachat(credentials, text, category, model, max_tokens=100):
    try:
        prompt = f"Изложи информацию только о параметре '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие темы. Излагай информацию, по формату, так, как указывают в досье на пациента/преступника. Формат ответа должен выглядеть следующим образом: {category}: информация только о {category}."
        payload = Chat(
            model=model,
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content="Вы являетесь ассистентом, который должен строго следовать инструкциям.",
                ),
            ],
            max_tokens=max_tokens,
        )

        with GigaChat(credentials=credentials, verify_ssl_certs=False) as giga:
            payload.messages.append(Messages(role=MessagesRole.USER, content=prompt))
            response = giga.chat(payload)
            total_tokens_used = response.usage.total_tokens
            if total_tokens_used > max_tokens:
                return {
                    'error': f'Недостаточно токенов. Необходимо установить более высокое значение (текущее использование: {total_tokens_used}, лимит: {max_tokens}).'}, 0
            else:
                return response.choices[0].message.content, total_tokens_used

    except GigaChatException:
        return {'error': 'Неверный API-ключ'}, 0

    except UnicodeEncodeError:
        return {
            'error': f'Убедитесь, что API-ключ содержит только допустимые символы, проверьте их на соответствие UTF-8'
        }

    except Exception as e:
        return {'error': str(e)}, 0
