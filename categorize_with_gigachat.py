from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os


def categorize_text_with_gigachat(text, category, temperature=0):
    try:
        prompt = f"Изложи информацию только о параметре '{category}' в следующем тексте, исключая все остальные темы: '{text}'. Сосредоточься исключительно на '{category}', игнорируя другие темы. Излагай информацию, по формату, так, как указывают в досье на пациента/преступника. Формат ответа должен выглядеть следующим образом: {category}: информация только о {category}"
        payload = Chat(
            messages=[
                Messages(
                    role=MessagesRole.SYSTEM,
                    content="Вы являетесь ассистентом, который должен строго следовать инструкциям.",
                ),
            ],
            temperature=temperature,
        )

        with GigaChat(credentials=os.getenv('GIGACHAT_CREDENTIALS'), verify_ssl_certs=False) as giga:
            payload.messages.append(Messages(role=MessagesRole.USER, content=prompt))
            response = giga.chat(payload)
            return response.choices[0].message.content

    except Exception as e:
        return {'error': str(e)}
