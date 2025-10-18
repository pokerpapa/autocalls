# AutoCalls — Flask-сервис: транскрипция звонков (Vosk) + анализ (Mistral) + отчёт DOCX

Загружаем MP3 → конвертируем в WAV → **Vosk** делает ASR → **Mistral** анализирует по чек-листу → собираем **.docx** отчёт и раскладываем по менеджерам. Есть веб-форма загрузки и страница истории отчётов.

## ✨ Возможности
- 📤 Веб-форма: выбор менеджера + мультизагрузка до 10 MP3
- 🎙 MP3 → WAV (FFmpeg/pydub), ASR через **Vosk**
- 🤖 Анализ текста через **Mistral** (таблица соответствия чек-листу + структурированный диалог)
- 📝 Генерация **DOCX** (python-docx)
- 📁 Автоматическая раскладка отчётов по менеджерам, страница **История**
- 🧩 Чек-лист берётся из `checklist.txt`

## 🗂 Архитектура
```text
project/
├─ app.py                 # Flask-приложение и роуты
├─ mistral_tools.py       # обращение к Mistral + чек-лист
├─ vostools.py            # MP3→WAV и Vosk ASR
├─ templates/
│  ├─ upload.html         # форма загрузки
│  └─ jobs.html           # история отчётов
├─ static/                # статические ресурсы (логотип и т.п.)
├─ instance/
│  ├─ uploads/            # входящие MP3 (runtime)
│  └─ results/            # готовые .docx по менеджерам (runtime)
├─ models/
│  └─ README.md           # как скачать Vosk-модель (сама модель в .gitignore)
├─ checklist.txt
├─ .env                   # ключи и пути (в .gitignore)
└─ requirements.txt
⚙️ Установка
Системные требования
Python 3.10+

FFmpeg в PATH (Windows: добавьте путь к ffmpeg.exe)

Vosk модель RU (например vosk-model-small-ru-0.22) — распакуйте и укажите путь в .env

Ключ Mistral API (для анализа)

Шаги
bash
Copy code
git clone https://github.com/<username>/<repo>.git
cd <repo>

python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
Создайте .env:

env
Copy code
# Flask/Vosk
VOSK_MODEL=C:\path\to\vosk-model-small-ru-0.22
# или /home/user/vosk-model-small-ru-0.22

# Mistral
MISTRAL_API_KEY=sk-xxxxxxxxxxxxxxxx

# (опционально) Flask INSTANCE_PATH берётся автоматически из app.instance_path
Где взять Vosk модель: https://alphacephei.com/vosk/models
Скачайте vosk-model-small-ru-0.22, распакуйте и пропишите путь в VOSK_MODEL.

▶️ Запуск
bash
Copy code
python app.py
# откройте http://127.0.0.1:8000
🧭 UI/Endpoints
GET / — форма загрузки (выбор менеджера, MP3)

POST /api/process — принимает (manager, audio) → генерирует .docx → JSON с download_url

GET /results/<manager>/<filename> — скачивание отчёта

GET /jobs — история по менеджерам

🔒 Замечания по эксплуатации
Не коммитьте .env, instance/uploads/, instance/results/, каталоги моделей

Большие файлы/модели держите вне репозитория; при деплое — поставляйте отдельно

FFmpeg обязателен для конвертации MP3→WAV

🧪 Быстрая проверка
Положите Vosk-модель, задайте VOSK_MODEL в .env

Запустите python app.py

Загрузите 1–2 MP3 → получите ссылку на DOCX

Откройте /jobs — появится история по менеджерам

