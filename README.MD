### Тестовое задание для Python разработчика для компании Hammer     Systems
##### Задание
Реализовать простую реферальную систему. Минимальный интерфейс для тестирования.
##### Проект развернут в прод среде.
##### API документация доступна по:
В Swagger

```
https://hammerstesttask.zapto.org/api/schema/swagger-ui/
```
В Redoc
```
https://hammerstesttask.zapto.org/api/schema/redoc/
```
##### Стек технологий
<div>
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/python/python-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/django/django-plain.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/djangorest/djangorest-line-wordmark.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg" width="50" height="50">
<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postman/postman-original-wordmark.svg" width="50" height="50">
</div>

###### Что сделано в проекте:
- Авторизация по номеру телефона. (api/registration/) Возвращается случайный 4 значный код. Если номера нет в БД, он сохраняется, если есть, обновляется 4 значный код. 
- Написаны кастоный UserManager и модель пользователя. 
- При первой авторизации (api/login/), единожды присваивается реферальный код пользователя. 
- При PATCH запросе к энпойнту (api/profile/{tepephone_number}) можно добавить реферальную ссылку пригласившего пользователя.
- Подключена PostgreSQL. 
- Сформировна конфигурация docker compose для локального развертывания.
- Сформирована коллекция запросов Postman


##### Чтобы запустить проект на локальной машине:
###### Клонировать репозиторий и перейти в него в командной строке:

```
git@github.com:dmitry-svechkar/hammers_systems_test_task_referral_api.git
```
###### Перейти в директорию:
```
cd ref_system/infra/
```
###### Создать в директории ref_system файл .env c указанием переменных.
###### при DEBUG = True, sqlite3

```
SECRET_KEY=any_secret_key_of_django_project
DEBUG=False

#db В прод-среде подключена sqllite3:

POSTGRES_USER=username
POSTGRES_PASSWORD=pass
POSTGRES_DB=name_db
DB_HOST=db
DB_PORT=5432

CSRF_TRUSTED_ORIGINS =http://domain:port

CORS_ORIGIN_WHITELIST =http://domain:port
```
###### Поднять контейнеры
```
docker-compose up
```

###### Выполнить миграции, собрать и копировать статистику:
```
docker exec backend python manage.py migrate
docker exec backend python manage.py collectstatic
docker exec backend cp -r /collected_static/. static/
```
###### Создать суперпользователя:
```
docker exec backend python manage.py сreatesuperuser
```
 
###### Примеры запросов.
Энпойнт api/registration/
```
{
    "telephone_number": "89999999999"
}
```
Вернет
```
{
    "Confirmation_code": "1234"
}
```
Энпойнт api/login/
```
{
    "telephone_number": "89999999999",
    "Confirmation_code": "1234"
}
```
Вернет
```
{
    "token": "django_token"
}
```
Эндпойнт api/profile/{telephone_number}
Необходимо указать заголовок запроса: Authorization : Token <token>
GET вернет ответ следующего формата
```
{
  "reg_data": "2024-04-22",
  "telephone_number": "string",
  "user_referal_code": "string",
  "all_referals": "string"
}
```
PATCH api/profile/{telephone_number} запрос добавит код приглашения в профиль пользователя. Доступно только добавление в свой профиль.
```
{
  "invitation_code": "string"
}
```

