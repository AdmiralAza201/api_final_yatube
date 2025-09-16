# Yatube API — итоговый сервис

REST API для социальной сети Yatube. Сервис позволяет публиковать записи, оставлять комментарии, подписываться на авторов и просматривать сообщества. Под капотом — JWT-аутентификация, права доступа и пагинация. Для проверки готова коллекция запросов Postman.

## Что умеет API
- Публикации: текстовый контент, автор, необязательная принадлежность к группе, дата публикации и поддержка изображений.
- Комментарии к постам: создание, редактирование и удаление в рамках конкретной записи.
- Сообщества (группы): список и детальная карточка (через API доступны только операции чтения).
- Подписки: выдача собственного списка подписок и оформление новой подписки; поиск по подпискам через `?search=<username>`.
- Аутентификация: работа с токенами JWT (создание, обновление, проверка).
- Пагинация: параметры `limit` и `offset` для выборки постов.

## Зависимости и требования
- Python 3.9+
- Django 3.2
- Всё необходимое перечислено в `requirements.txt`

## Быстрый старт
```bash
git clone https://github.com/ONS-1111/api_final_yatube
cd api_final_yatube-master

# Виртуальное окружение
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# База и запуск
cd yatube_api
python manage.py migrate
python manage.py runserver
```

## Карта API (v1)
- `POST /api/v1/jwt/create/` — получить пару токенов (`access`/`refresh`).
- `POST /api/v1/jwt/refresh/` — выпустить новый `access` по `refresh`.
- `POST /api/v1/jwt/verify/` — проверить валидность токена.
- `GET/POST /api/v1/posts/` — список постов / создание поста.
- `GET/PUT/PATCH/DELETE /api/v1/posts/{id}/` — получить/изменить/удалить пост.
- `GET/POST /api/v1/posts/{post_id}/comments/` — список/создание комментариев к посту.
- `GET/PUT/PATCH/DELETE /api/v1/posts/{post_id}/comments/{id}/` — операции с конкретным комментарием.
- `GET /api/v1/groups/` и `GET /api/v1/groups/{id}/` — список и детальная карточка сообщества.
- `GET/POST /api/v1/follow/` — подписки текущего пользователя; поиск по `?search=<username>`.

## Доступы и правила
- Неавторизованные пользователи работают в режиме «только чтение» (исключение — `/follow/`: доступно только авторизованным).
- Автор записи/комментария может изменять и удалять только свой контент.
- Создание групп через API не предусмотрено — добавляйте их в админке.

## JWT-аутентификация
- Получение токенов: `POST /api/v1/jwt/create/` с полями `username` и `password`.
- Передавайте `Authorization: Bearer <access_token>` для защищённых запросов.
- Обновление и верификация: `POST /api/v1/jwt/refresh/` и `POST /api/v1/jwt/verify/`.

## Postman-коллекция
- Импортируйте `postman_collection/API_for_yatube.postman_collection.json` в Postman.
- Для быстрого наполнения базы воспользуйтесь скриптом ниже, затем выполните запросы из коллекции.

## Скрипт инициализации тестовых данных
```bash
cd postman_collection
chmod +x set_up_data.sh
./set_up_data.sh
```
Будут созданы пользователи и группа:
- суперпользователь: `root / 5eCretPaSsw0rD`
- обычный пользователь: `regular_user / iWannaBeAdmin`
- второй пользователь: `second_user / 5eCretPaSsw0rD`
- группа: `TestGroup`

## Пример запроса: создание поста
```http
POST /api/v1/posts/
Authorization: Bearer <access>
Content-Type: application/json

{ "text": "Привет!", "group": 1 }
```

Примечание: для списка постов можно передать `?limit=<N>&offset=<K>`.

## Технологический стек
- Django 3.2, Django REST Framework, SimpleJWT

## Контакты
- Оспищев Никита Сергеевич
- Email: Kanalohca@gmail.com
