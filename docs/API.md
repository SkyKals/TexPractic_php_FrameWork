# API Documentation — Notifications (Variant #97)

REST API для управління сповіщеннями (notifications), реалізований **двічі** — на **Laravel** (порт 8000) та **Symfony** (порт 8001). Обидві реалізації мають однаковий набір ендпоінтів і спільну бізнес-логіку, працюють поверх **SQLite**.

Документація побудована на основі фактичного коду контролерів, моделі/entity та міграції.

---

## Модель даних

Таблиця `notifications`.

| Поле | Тип | Обмеження / за замовчуванням | Опис |
|------|-----|------------------------------|------|
| `id` | integer | auto-increment, PK | Унікальний ідентифікатор |
| `title` | string(255) | NOT NULL, обовʼязкове | Заголовок сповіщення |
| `message` | text | NOT NULL, обовʼязкове | Текст сповіщення |
| `type` | string(50) | default `info` | Одне з: `info`, `warning`, `error`, `success` |
| `is_read` | boolean | default `false` | Чи прочитане сповіщення |
| `created_at` | datetime | авто при створенні | Час створення |
| `updated_at` | datetime | авто при оновленні | Час останнього оновлення |

> **Примітка про формат дат.** Laravel (Eloquent) серіалізує дати у вигляді `2026-06-16T10:00:00.000000Z`. Symfony (Doctrine, формат ATOM) — у вигляді `2026-06-16T10:00:00+00:00`. Поле `is_read` в обох реалізаціях повертається як булеве значення JSON (`true`/`false`).

---

## Laravel API

**Base URL:** `http://localhost:8000/api`

Маршрути зареєстровані через `Route::apiResource('notifications', NotificationController::class)`.

### 1. GET `/api/notifications`
Отримати список усіх сповіщень.

**Відповідь 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "System Alert",
      "message": "Disk usage is above 90%",
      "type": "warning",
      "is_read": false,
      "created_at": "2026-06-16T10:00:00.000000Z",
      "updated_at": "2026-06-16T10:00:00.000000Z"
    }
  ],
  "count": 1
}
```

**Статус коди:** `200`.

---

### 2. GET `/api/notifications/{id}`
Отримати одне сповіщення за його id.

**Відповідь 200:**
```json
{
  "data": {
    "id": 1,
    "title": "System Alert",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:00:00.000000Z"
  }
}
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Статус коди:** `200`, `404`.

---

### 3. POST `/api/notifications`
Створити нове сповіщення.

**Тіло запиту:**
```json
{
  "title": "System Alert",
  "message": "Disk usage is above 90%",
  "type": "warning",
  "is_read": false
}
```

**Відповідь 201:**
```json
{
  "data": {
    "id": 1,
    "title": "System Alert",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:00:00.000000Z"
  },
  "message": "Notification created"
}
```

**Відповідь 422** (помилка валідації, стандартний формат Laravel):
```json
{
  "message": "The title field is required.",
  "errors": {
    "title": ["The title field is required."]
  }
}
```

**Статус коди:** `201`, `422`.

---

### 4. PATCH `/api/notifications/{id}`
Частково оновити сповіщення. Передаються тільки ті поля, які потрібно змінити.

**Тіло запиту:**
```json
{
  "title": "Updated title",
  "is_read": true
}
```

**Відповідь 200:**
```json
{
  "data": {
    "id": 1,
    "title": "Updated title",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": true,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:05:00.000000Z"
  },
  "message": "Notification updated"
}
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Статус коди:** `200`, `404`, `422`.

---

### 5. DELETE `/api/notifications/{id}`
Видалити сповіщення.

**Відповідь 200:**
```json
{ "message": "Notification deleted" }
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Статус коди:** `200`, `404`.

---

## Symfony API

**Base URL:** `http://localhost:8001/api`

Маршрути зареєстровані через атрибути `#[Route('/api/notifications')]` на контролері.

### 1. GET `/api/notifications`
Отримати список усіх сповіщень.

**Відповідь 200:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "System Alert",
      "message": "Disk usage is above 90%",
      "type": "warning",
      "is_read": false,
      "created_at": "2026-06-16T10:00:00+00:00",
      "updated_at": "2026-06-16T10:00:00+00:00"
    }
  ],
  "count": 1
}
```

**Статус коди:** `200`.

---

### 2. GET `/api/notifications/{id}`
Отримати одне сповіщення за id.

**Відповідь 200:**
```json
{
  "data": {
    "id": 1,
    "title": "System Alert",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00+00:00",
    "updated_at": "2026-06-16T10:00:00+00:00"
  }
}
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Статус коди:** `200`, `404`.

---

### 3. POST `/api/notifications`
Створити нове сповіщення. Тіло декодується з JSON.

**Тіло запиту:**
```json
{
  "title": "System Alert",
  "message": "Disk usage is above 90%",
  "type": "warning",
  "is_read": false
}
```

**Відповідь 201:**
```json
{
  "data": {
    "id": 1,
    "title": "System Alert",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00+00:00",
    "updated_at": "2026-06-16T10:00:00+00:00"
  },
  "message": "Notification created"
}
```

**Відповідь 422** (відсутні обовʼязкові поля):
```json
{
  "error": "Validation failed",
  "errors": {
    "title": "Title is required",
    "message": "Message is required"
  }
}
```

**Відповідь 422** (недопустиме значення `type`):
```json
{ "error": "Invalid type. Must be one of: info, warning, error, success" }
```

**Статус коди:** `201`, `422`.

---

### 4. PATCH `/api/notifications/{id}`
Частково оновити сповіщення. Оновлюються тільки передані поля.

**Тіло запиту:**
```json
{
  "title": "Updated title",
  "is_read": true
}
```

**Відповідь 200:**
```json
{
  "data": {
    "id": 1,
    "title": "Updated title",
    "message": "Disk usage is above 90%",
    "type": "warning",
    "is_read": true,
    "created_at": "2026-06-16T10:00:00+00:00",
    "updated_at": "2026-06-16T10:05:00+00:00"
  },
  "message": "Notification updated"
}
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Відповідь 422** (недопустиме значення `type`):
```json
{ "error": "Invalid type" }
```

**Статус коди:** `200`, `404`, `422`.

---

### 5. DELETE `/api/notifications/{id}`
Видалити сповіщення.

**Відповідь 200:**
```json
{ "message": "Deleted" }
```

**Відповідь 404:**
```json
{ "error": "Not found" }
```

**Статус коди:** `200`, `404`.

---

## Приклади curl (Laravel)

```bash
# 1. Список усіх сповіщень
curl -X GET http://localhost:8000/api/notifications \
  -H "Accept: application/json"

# 2. Одне сповіщення за id
curl -X GET http://localhost:8000/api/notifications/1 \
  -H "Accept: application/json"

# 3. Створити сповіщення
curl -X POST http://localhost:8000/api/notifications \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"title":"System Alert","message":"Disk usage is above 90%","type":"warning","is_read":false}'

# 4. Частково оновити сповіщення
curl -X PATCH http://localhost:8000/api/notifications/1 \
  -H "Content-Type: application/json" \
  -H "Accept: application/json" \
  -d '{"title":"Updated title","is_read":true}'

# 5. Видалити сповіщення
curl -X DELETE http://localhost:8000/api/notifications/1 \
  -H "Accept: application/json"
```

> Для Symfony використовуй ті самі команди, замінивши порт `8000` на `8001`.

---

## Валідація

| Поле | Правило | Laravel | Symfony |
|------|---------|---------|---------|
| `title` | обовʼязкове при створенні, рядок до 255 символів | `required\|string\|max:255` | перевірка на `empty()` |
| `message` | обовʼязкове при створенні, рядок | `required\|string` | перевірка на `empty()` |
| `type` | необовʼязкове, одне з `info`/`warning`/`error`/`success` | `sometimes\|string\|in:...` | `in_array()` проти whitelist |
| `is_read` | необовʼязкове, булеве | `sometimes\|boolean` | приведення `(bool)` |

**Поведінка при помилці:** обидві реалізації повертають статус **`422`**.
- **Laravel** — стандартний формат валідації: `{"message": "...", "errors": {...}}`.
- **Symfony** — для відсутніх обовʼязкових полів: `{"error": "Validation failed", "errors": {...}}`; для недопустимого `type`: `{"error": "Invalid type..."}`.

При оновленні (PATCH) усі поля необовʼязкові — застосовуються ті самі правила лише до переданих полів.

---

## Запуск

### Laravel
```bash
cd laravel
php artisan serve --port=8000
```

### Symfony
```bash
cd symfony
php -S localhost:8001 -t public
```
