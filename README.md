# PlantCare — учёт полива растений

**Тема:** Учёт полива растений (вариант 10).  
**Технологии:** FastAPI, SQLAlchemy 2.0, SQLite, Alembic, HTML, CSS, JavaScript.

## Назначение
Приложение позволяет зарегистрированному пользователю вести список домашних растений, фиксировать полив, просматривать историю ухода и находить растения, которым требуется полив.

## Запуск в Windows
1. Установить Python 3.11 или новее.
2. Открыть терминал в папке проекта.
3. Создать виртуальное окружение:
   ```powershell
   python -m venv venv
   venv\Scripts\activate
   ```
4. Установить зависимости:
   ```powershell
   pip install -r requirements.txt
   ```
5. Создать таблицы миграцией:
   ```powershell
   alembic upgrade head
   ```
6. Запустить сервер:
   ```powershell
   uvicorn app.main:app --reload
   ```
7. Открыть http://127.0.0.1:8000

Swagger: http://127.0.0.1:8000/docs

## Структура базы данных
- `users` — пользователи приложения.
- `plants` — растения. `owner_id` ссылается на `users.id`.
- `waterings` — записи о поливе. `plant_id` ссылается на `plants.id`.

Связи: User 1:N Plant; Plant 1:N Watering.

## Основные эндпоинты
| Метод | URL | Назначение |
|---|---|---|
| POST | /api/auth/register | Регистрация |
| POST | /api/auth/login | Вход |
| POST | /api/auth/logout | Выход |
| GET | /api/auth/me | Текущий пользователь |
| GET | /api/plants | Список, поиск `q`, фильтр `needs_water` |
| GET | /api/plants/{id} | Получение растения |
| POST | /api/plants | Создание растения |
| PATCH | /api/plants/{id} | Изменение растения |
| DELETE | /api/plants/{id} | Удаление растения |
| GET | /api/plants/{id}/waterings | История поливов |
| POST | /api/plants/{id}/waterings | Добавление полива |
| DELETE | /api/plants/{id}/waterings/{watering_id} | Удаление записи о поливе |
| GET | /api/stats | Краткая статистика |

## Безопасность
Пароли хранятся в виде хеша PBKDF2-HMAC-SHA256 с индивидуальной случайной солью. Идентификатор пользователя хранится в подписанной сессии. Все операции с растениями проверяют владельца; чужие записи возвращают 404. В API не передаётся `password_hash`.

## Примечание
Перед развёртыванием в публичной сети необходимо задать собственный секретный ключ через переменную окружения `PLANTCARE_SECRET` и включить HTTPS.
