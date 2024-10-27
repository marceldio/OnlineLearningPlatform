FROM python:3.12.3

# Обновляем pip до последней версии
RUN pip install --upgrade pip

# Устанавливаем Poetry через pip
RUN pip install poetry

# Устанавливаем рабочую директорию
WORKDIR /code

# Отключаем создание внешнего виртуального окружения
RUN poetry config virtualenvs.create false

# Копируем только файлы зависимостей
COPY pyproject.toml poetry.lock /code/

# Устанавливаем зависимости через Poetry
RUN poetry install

# Установка утилиты netcat
RUN apt-get update && apt-get install -y netcat-openbsd

# Копируем все остальные файлы
COPY . .

# Выполняем миграции и запускаем сервер
# CMD ["sh", "-c", "python manage.py migrate && exec python manage.py runserver 0.0.0.0:8000"]
CMD ["sh", "-c", "exec python manage.py runserver 0.0.0.0:8000"]
