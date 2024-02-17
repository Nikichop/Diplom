from gigachat import GigaChat
from gigachat.models import Chat, Messages, MessagesRole
import os


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
            update_interval=0.1,
        )

        with GigaChat(credentials=os.getenv('GIGACHAT_CREDENTIALS'), verify_ssl_certs=False) as giga:
            payload.messages.append(Messages(role=MessagesRole.USER, content=prompt))
            response = giga.chat(payload)
            return response.choices[0].message.content

    except Exception as e:
        return {'error': str(e)}
