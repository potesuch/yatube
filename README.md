# Yatube

## Описание

Это Django приложение представляет собой платформу для блогов, где пользователи могут создавать и управлять постами, комментировать их, подписываться на других пользователей и просматривать посты по группам и тегам. Также предоставляется API для интеграции с внешними системами и создания мобильных приложений.

# Установка

1. Клонируйте репозиторий:

    ```sh

    git clone https://github.com/potesuch/yatube.git
    cd yatube
    ```

2. Создайте виртуальное окружение и активируйте его:

    ```sh

    python -m venv venv
    source venv/bin/activate  # Для Windows используйте `venv\Scripts\activate`
    ```

3. Установите зависимости:

    ```sh

    pip install -r requirements.txt
    ```

4. Примените миграции:

    ```sh

    python manage.py migrate
    ```

5. Запустите сервер разработки:

    ```sh

    python manage.py runserver
    ```
