# Журнал промптів — AI-розробка проекту

Цей документ хронологічно фіксує процес розробки проекту **Notifications CRUD (Варіант #97)** із застосуванням AI-асистента (Claude Code) як інструмента розробки. Для кожного етапу наведено мету та реальний промпт, який використовувався для отримання результату.

---

## Етап 1. Ініціалізація і встановлення фреймворків

**Мета:** підготувати робочу директорію з двома незалежними проектами — Laravel і Symfony — та спільним git-репозиторієм для практичної роботи.

```text
Створи робочу директорію frameworks для практичної роботи (тема #97 Notifications).
Усередині встанови два проекти:
- laravel/ — свіжий Laravel-проект, налаштований на SQLite (DB_CONNECTION=sqlite,
  файл database/database.sqlite)
- symfony/ — свіжий Symfony-проект (skeleton)
Ініціалізуй git-репозиторій у корені frameworks/. Стек: PHP 8.5, Composer 2.10.
Не використовуй жодних зовнішніх баз даних — тільки SQLite.
```

---

## Етап 2. Laravel Notifications CRUD

**Мета:** реалізувати повний CRUD для сутності Notification у Laravel — міграція, модель, контролер, маршрути.

```text
Реалізуй у laravel/ повний CRUD для Notifications:

1. Міграція таблиці notifications з полями: id (bigIncrements), title (string 255,
   not null), message (text, not null), type (string 50, default 'info'),
   is_read (boolean, default false), timestamps.
2. Модель App\Models\Notification з $fillable (title, message, type, is_read)
   і кастом is_read => boolean.
3. Контролер NotificationController з методами index, show, store, update, destroy.
   - index повертає {"data": [...], "count": N}, статус 200
   - show повертає {"data": {...}} або 404 {"error": "Not found"}
   - store валідує title required|max:255, message required, type in:info,warning,
     error,success, is_read boolean; повертає 201 з message "Notification created"
   - update знаходить або 404, валідує optional-поля, повертає 200
   - destroy знаходить або 404, видаляє, повертає 200 {"message": "Notification deleted"}
4. Зареєструй apiResource у routes/api.php і підключи api-маршрути в bootstrap/app.php.

Дотримуйся PSR-12. Усі відповіді — валідний JSON. Запусти міграцію і перевір
route:list, що всі 5 маршрутів на місці.
```

---

## Етап 3. Symfony Notifications CRUD

**Мета:** реалізувати аналогічний CRUD у Symfony засобами Doctrine ORM, із тією самою структурою відповідей.

```text
Реалізуй у symfony/ повний CRUD для Notifications на Doctrine ORM (SQLite,
DATABASE_URL="sqlite:///%kernel.project_dir%/var/data.db"):

1. Встанови orm-pack, maker-bundle (dev) і validator
   (додавай --ignore-platform-req=ext-iconv до composer-команд).
2. Entity App\Entity\Notification з полями id, title (255), message (text),
   type (string 50, default 'info'), isRead (bool, default false),
   createdAt і updatedAt (datetime_immutable). Додай геттери/сеттери, ORM-атрибути,
   lifecycle-callback для updatedAt і метод toArray() для серіалізації
   (is_read, created_at, updated_at у вихідному JSON).
3. NotificationRepository.
4. Згенеруй і застосуй міграцію.
5. Контролер NotificationController з атрибутами #[Route('/api/notifications')]:
   list, show, create, update, delete. JSON-відповіді мають збігатися за структурою
   з Laravel: {"data": ..., "count": N}, повідомлення "Notification created"/
   "Notification updated", 404 {"error": "Not found"}, 422 при невалідних даних.

Перевір через debug:router, що всі 5 маршрутів зареєстровані.
```

---

## Етап 4. Postman колекції

**Мета:** створити колекції Postman для ручного тестування обох API.

```text
Створи папку postman/ з двома колекціями Postman Collection v2.1:
- laravel.json — запити до http://localhost:8000/api/notifications
- symfony.json — ті самі запити до http://localhost:8001/api/notifications

У кожній колекції 5 запитів: GET список, GET за id, POST (тіло
{"title":"Test","message":"Hello","type":"info","is_read":false}),
PATCH (тіло {"title":"Updated","is_read":true}), DELETE.
info.schema має дорівнювати
"https://schema.getpostman.com/json/collection/v2.1.0/collection.json".
```

---

## Етап 5. Субагенти Claude Code

**Мета:** додати систему спеціалізованих субагентів для структурованого AI-процесу розробки.

```text
Створи директорію .claude/agents і чотири субагенти Claude Code (markdown-файли
з YAML front-matter: name, description, tools — далі системний промпт):

- dev.md — PHP-розробник (Read, Write, Edit, Bash): PSR-12, валідний JSON,
  тільки SQLite, Eloquent для Laravel і Doctrine для Symfony, валідація вводу,
  не чіпає vendor/, читає сусідні файли заради стилю.
- reviewer.md — код-рев'ювер (Read, Grep, Bash): чекліст із 5 ендпоінтів,
  HTTP-коди 200/201/404/422, валідація, паритет Laravel і Symfony; тільки звітує.
- git-manager.md — git-інженер (Bash, Read): гілки тільки від dev,
  Conventional Commits, merge лише з --no-ff, ніколи не пушить напряму в main.
- docs-writer.md — технічний письменник (Read, Write, Bash): документація лише
  на основі реального коду, підтримує Postman-колекції.
```

---

## Етап 6. Технічна документація API

**Мета:** скласти повну документацію API, що точно відповідає реалізованому коду.

```text
Спершу прочитай реальні контролери, модель/entity та міграцію Laravel і Symfony.
На основі прочитаного створи docs/API.md:
- опис проекту і таблиця моделі даних (id, title, message, type, is_read,
  created_at, updated_at)
- розділ Laravel API (base http://localhost:8000/api) — для кожного з 5 ендпоінтів
  метод, URL, призначення, тіло запиту, приклад реальної відповіді, статус коди
- розділ Symfony API (base http://localhost:8001/api) аналогічно
- готові curl-приклади для всіх 5 операцій
- розділ валідації (обовʼязкові title і message, правила type/is_read, 422)
- розділ запуску обох серверів
Документація має відповідати фактичному коду, а не вигаданому.
```

---

## Етап 7. Журнал промптів

**Мета:** задокументувати весь процес AI-розробки для прозорості й відтворюваності.

```text
Створи docs/PROMPTS.md — хронологічний журнал промптів, що використовувались
для розробки проекту. Для кожного етапу (ініціалізація, Laravel CRUD,
Symfony CRUD, Postman, субагенти, документація API, цей журнал) вкажи заголовок,
коротку мету і реалістичний текст промпта, який справді міг би згенерувати
відповідний результат.
```

---

## Етап 8. Тестування і відповідність ТЗ

**Мета:** привести контролери у відповідність до технічного завдання (TestController) і перевірити всі endpoints.

```text
Перейменуй контролери на TestController у Laravel і Symfony, зберігаючи логіку CRUD.
Протестуй усі пʼять операцій через curl на портах 8000 і 8001, переконайся, що
статуси 200, 201, 404, 422 коректні і структура відповідей у двох фреймворках
збігається. Виправ будь-які помилки.
```

---

## Етап 9. Документація для фронтенду

**Мета:** створити практичну документацію API для споживачів.

```text
Створи docs/ENDPOINTS.md з описом кожної операції для фронтенд-розробника: метод,
URL, заголовки, тіло запиту, приклади успішних і помилкових відповідей і готові
приклади fetch на JavaScript для кожного endpoint.
```
