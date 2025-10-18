# mistral_tools.py
import os
import logging
from mistralai import Mistral

API_KEY = os.getenv("MISTRAL_API_KEY")
MODEL = "mistral-small-latest"
# Читаем чек‑лист из файла checklist.txt
CHECKLIST_PATH = os.path.join(os.path.dirname(__file__), "checklist.txt")
with open(CHECKLIST_PATH, encoding="utf-8") as f:
    CHECKLIST = f.read()

def call_mistral(raw_text: str) -> str:
    prompt = f"""
У меня есть чек‑лист для оценки качества телефонного звонка в автосалоне и транскрибированный текст разговора.

1) 📞 **Структурированный диалог**  
Преобразуй транскрипт в понятный диалог между Менеджером и Клиентом.  
— Каждую реплику отмечай как `Менеджер:` или `Клиент:`.

2) ✅ **Таблица соответствия чек‑листу**  
Обязательно выведи после диалога **Markdown‑таблицу** со следующими колонками и примером:

| №  | Пункт чек‑листа                                            | Выполнено? | Комментарий                   |
|----|------------------------------------------------------------|:----------:|-------------------------------|
| 1  | Представление менеджера и приветствие                      | ✅/❌      | краткий комментарий           |
| 2  | …                                                          | …          | …                             |

**Чек‑лист:**
{CHECKLIST}

**Транскрипт:**
{raw_text}

— Не пропускай ни один из двух шагов: сначала весь диалог, потом заголовок таблицы и саму Markdown‑таблицу.
"""
    with Mistral(api_key=API_KEY) as client:
        logging.debug("Отправляем запрос в Mistral…")
        resp = client.chat.complete(
            model=MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            stream=False
        )
    return resp.choices[0].message.content.strip()
