
Приложение для отслеживания полезных привычек с автоматическими уведомлениями в Telegram и системой CI/CD.

## 🚀 Быстрый запуск (Локально)

### Подготовка окружения
Убедитесь, что у вас установлены **Docker** и **Docker Compose**.

Создайте файл `.env` в корне проекта и заполните его:

SECRET_KEY=your_secret_key
DEBUG=True

POSTGRES_DB=healthy_habits
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_HOST=db
POSTGRES_PORT=5432

CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

2. Запуск проекта
Соберите и запустите контейнеры:
docker-compose up -d --build


Приложение будет доступно по адресу: http://localhost:8000/

🛠 Настройка CI/CD (GitHub Actions)
Проект настроен на автоматическое тестирование, проверку линтером и деплой на сервер Yandex Cloud.
1. Настройка сервера (Yandex Cloud)
Зайдите на сервер по SSH и выполните подготовку:
# Установка Docker
curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh
sudo apt-get install -y docker-compose-plugin

# Настройка прав доступа (критично для GitHub Actions)
sudo usermod -aG docker $USER
sudo chmod 666 /var/run/docker.sock

2. Добавление GitHub Secrets
Перейдите в репозиторий: Settings > Secrets and variables > Actions и добавьте:
Секрет	Описание
HOST	Публичный IP вашей ВМ (например, 89.169.xxx.xxx)
USER	Имя пользователя (например, test)
SSH_KEY	Содержимое вашего приватного ключа id_rsa


🏗 Архитектура деплоя
При каждом git push в ветку main происходят следующие действия:
Linter: Проверка кода через flake8 (исключая миграции).
Tests: Запуск тестов Django внутри GitHub Actions с использованием временной базы PostgreSQL.
При каждом git push в ветку main происходят следующие действия:
Linter: Проверка кода через flake8 (исключая миграции).
Tests: Запуск тестов Django внутри GitHub Actions с использованием временной базы PostgreSQL.
Build Check: Проверка сборки Docker-образов.
Deploy:
Автоматическое подключение к серверу через SSH.
Обновление кода через git pull.
Пересборка контейнеров (docker-compose up --build).
Автоматический запуск миграций БД внутри контейнера.
📋 Основные команды
Просмотр логов: docker-compose logs -f
Выполнение миграций: docker-compose exec backend python manage.py migrate
Создание суперпользователя: docker-compose exec backend python manage.py createsuperuser