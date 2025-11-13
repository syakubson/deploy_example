# Qwen3 Text Generation Service

FastAPI сервис для генерации текста с использованием модели Qwen3-0.6B. Включает Gradio веб-интерфейс и автоматический деплой через GitLab CI/CD.

## Структура проекта

```
.
├── src/                    # Основной код приложения
│   ├── app.py             # FastAPI приложение с Gradio UI
│   └── download_model.py  # Скрипт загрузки модели с S3
├── scripts/                # Вспомогательные скрипты
│   └── entrypoint.sh      # Docker entrypoint
├── docs/                   # Документация
│   └── DEPLOYMENT.md      # Руководство по деплою
├── examples/               # Примеры использования
│   ├── example_client.py  # Пример клиента для API
│   └── qwen_test.ipynb    # Тестовый notebook
├── Dockerfile              # Docker образ
├── docker-compose.yml      # Docker Compose конфигурация
├── .gitlab-ci.yml          # GitLab CI/CD pipeline
├── requirements.txt        # Python зависимости
└── README.md               # Документация
```

## Особенности

- **FastAPI REST API** - `/generate` и `/health` endpoints
- **Gradio Web UI** - простой интерфейс для взаимодействия с моделью
- **Автоматический деплой** - GitLab CI/CD pipeline с build и deploy stages
- **Docker контейнеризация** - легкий деплой на любой сервер
- **S3 интеграция** - автоматическая загрузка модели при старте контейнера

## Быстрый старт

### Локальный запуск

```bash
# Установка зависимостей
pip install -r requirements.txt

# Запуск сервиса (требуется локальная модель в папке Qwen3-0.6B)
./run_local.sh

# Или вручную:
export MODEL_PATH=./Qwen3-0.6B
export PYTHONPATH=.
uvicorn src.app:app --host 0.0.0.0 --port 8000
```

Откройте браузер: `http://localhost:8000`

### Docker запуск

```bash
docker build -t qwen3-service .
docker run -d -p 8000:8000 \
  -e S3_ENDPOINT="your-s3-endpoint" \
  -e S3_ACCESS_KEY="your-key" \
  -e S3_SECRET_KEY="your-secret" \
  -e S3_BUCKET="your-bucket" \
  -e S3_MODEL_PATH="models/Qwen3-0.6B.tar.gz" \
  qwen3-service
```

### Использование API клиента

```bash
# Запустите пример клиента
python examples/example_client.py
```

## Деплой

Подробные инструкции по настройке GitLab CI/CD и деплою на сервер смотрите в [DEPLOYMENT.md](docs/DEPLOYMENT.md).

## API Endpoints

- `GET /` - Gradio веб-интерфейс
- `POST /generate` - генерация текста (возвращает thinking и content)
- `GET /health` - проверка статуса сервиса
- `GET /docs` - автоматическая документация API

## Технологии

- **Python 3.11**
- **FastAPI** - веб-фреймворк
- **Gradio** - веб-интерфейс
- **Transformers** - работа с моделью Qwen3
- **PyTorch** - ML фреймворк
- **Boto3** - работа с S3
- **Docker** - контейнеризация
- **GitLab CI/CD** - автоматический деплой
