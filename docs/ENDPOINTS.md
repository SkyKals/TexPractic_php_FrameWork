# Endpoints — практична документація для фронтенду

Цей документ описує всі операції API сповіщень (notifications) для розробника, який пише фронтенд і **не бачив код бекенду**. Для кожної операції наведено метод, URL, заголовки, тіло запиту, приклади реальних відповідей (успіх і помилки) та готовий приклад виклику через `fetch`.

## Базові URL

| Фреймворк | Base URL |
|-----------|----------|
| Laravel | `http://localhost:8000/api` |
| Symfony | `http://localhost:8001/api` |

**Обидва API ідентичні за контрактом** — однакові шляхи, методи, тіла запитів, структура відповідей і статус коди. Можна розробляти проти будь-якого з них; для перемикання достатньо змінити порт (`8000` ↔ `8001`).

> **Єдина технічна відмінність** — формат дат у полях `created_at` / `updated_at`:
> - Laravel: `"2026-06-16T10:00:00.000000Z"`
> - Symfony: `"2026-06-16T10:00:00+00:00"`
>
> Обидва формати є валідним ISO 8601 і коректно парсяться через `new Date(value)` у JavaScript.

Усі запити з тілом надсилаються із заголовком `Content-Type: application/json`. Відповіді завжди у форматі JSON.

---

## Поля моделі

| Поле | Тип | Обовʼязкове при створенні | Опис |
|------|-----|---------------------------|------|
| `title` | string (до 255) | **так** | Заголовок сповіщення |
| `message` | string | **так** | Текст сповіщення |
| `type` | string | ні (за замовчуванням `info`) | Одне з: `info`, `warning`, `error`, `success` |
| `is_read` | boolean | ні (за замовчуванням `false`) | Чи прочитане сповіщення |

Поля `id`, `created_at`, `updated_at` генеруються сервером автоматично — їх не треба передавати.

При **створенні (POST)** обовʼязкові `title` і `message`. При **оновленні (PATCH)** усі поля необовʼязкові — передавай лише ті, які змінюєш.

---

## 1. Отримати список сповіщень

Повертає всі сповіщення та їх кількість.

- **Метод і URL:** `GET /api/notifications`
- **Заголовки:** не обовʼязкові
- **Тіло запиту:** не потрібне

**Успішна відповідь — `200 OK`:**
```json
{
  "data": [
    {
      "id": 1,
      "title": "Test",
      "message": "Hello world",
      "type": "info",
      "is_read": false,
      "created_at": "2026-06-16T10:00:00.000000Z",
      "updated_at": "2026-06-16T10:00:00.000000Z"
    }
  ],
  "count": 1
}
```
Якщо записів немає — `data` буде порожнім масивом, а `count` дорівнюватиме `0`.

**Приклад fetch:**
```javascript
const res = await fetch("http://localhost:8000/api/notifications");
const json = await res.json();
console.log(json.count, json.data);
```

---

## 2. Отримати одне сповіщення

Повертає одне сповіщення за його `id`.

- **Метод і URL:** `GET /api/notifications/{id}`
- **Заголовки:** не обовʼязкові
- **Тіло запиту:** не потрібне

**Успішна відповідь — `200 OK`:**
```json
{
  "data": {
    "id": 1,
    "title": "Test",
    "message": "Hello world",
    "type": "info",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:00:00.000000Z"
  }
}
```

**Помилка — `404 Not Found`** (сповіщення з таким id не існує):
```json
{ "error": "Not found" }
```

**Приклад fetch:**
```javascript
const id = 1;
const res = await fetch(`http://localhost:8000/api/notifications/${id}`);
if (res.status === 404) {
  console.warn("Сповіщення не знайдено");
} else {
  const { data } = await res.json();
  console.log(data);
}
```

---

## 3. Створити сповіщення

Створює нове сповіщення.

- **Метод і URL:** `POST /api/notifications`
- **Заголовки:** `Content-Type: application/json`
- **Тіло запиту:**
```json
{
  "title": "Test",
  "message": "Hello world",
  "type": "info",
  "is_read": false
}
```

**Успішна відповідь — `201 Created`:**
```json
{
  "data": {
    "id": 1,
    "title": "Test",
    "message": "Hello world",
    "type": "info",
    "is_read": false,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:00:00.000000Z"
  },
  "message": "Notification created"
}
```

**Помилка валідації — `422 Unprocessable Entity`** (відсутні обовʼязкові поля):

Laravel:
```json
{
  "message": "The title field is required. (and 1 more error)",
  "errors": {
    "title": ["The title field is required."],
    "message": ["The message field is required."]
  }
}
```

Symfony:
```json
{
  "error": "Validation failed",
  "errors": {
    "title": "Title is required",
    "message": "Message is required"
  }
}
```

> Обидва повертають статус `422`. Перевіряй саме код статусу — він однаковий; формат тіла помилки трохи відрізняється між фреймворками. Для недопустимого `type` також повертається `422`.

**Приклад fetch:**
```javascript
const res = await fetch("http://localhost:8000/api/notifications", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    title: "Test",
    message: "Hello world",
    type: "info",
    is_read: false
  })
});

if (res.status === 422) {
  const err = await res.json();
  console.error("Помилка валідації", err);
} else {
  const { data } = await res.json();
  console.log("Створено", data.id);
}
```

---

## 4. Оновити сповіщення

Частково оновлює сповіщення. Передавай лише поля, які треба змінити.

- **Метод і URL:** `PATCH /api/notifications/{id}`
- **Заголовки:** `Content-Type: application/json`
- **Тіло запиту:**
```json
{
  "title": "Updated",
  "is_read": true
}
```

**Успішна відповідь — `200 OK`:**
```json
{
  "data": {
    "id": 1,
    "title": "Updated",
    "message": "Hello world",
    "type": "info",
    "is_read": true,
    "created_at": "2026-06-16T10:00:00.000000Z",
    "updated_at": "2026-06-16T10:05:00.000000Z"
  },
  "message": "Notification updated"
}
```

**Помилка — `404 Not Found`:**
```json
{ "error": "Not found" }
```

**Приклад fetch:**
```javascript
const id = 1;
const res = await fetch(`http://localhost:8000/api/notifications/${id}`, {
  method: "PATCH",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ title: "Updated", is_read: true })
});
const json = await res.json();
console.log(json.message, json.data);
```

---

## 5. Видалити сповіщення

Видаляє сповіщення за `id`.

- **Метод і URL:** `DELETE /api/notifications/{id}`
- **Заголовки:** не обовʼязкові
- **Тіло запиту:** не потрібне

**Успішна відповідь — `200 OK`:**
```json
{ "message": "Notification deleted" }
```

**Помилка — `404 Not Found`:**
```json
{ "error": "Not found" }
```

**Приклад fetch:**
```javascript
const id = 1;
const res = await fetch(`http://localhost:8000/api/notifications/${id}`, {
  method: "DELETE"
});
if (res.status === 404) {
  console.warn("Нічого видаляти — не знайдено");
} else {
  const json = await res.json();
  console.log(json.message);
}
```

---

## Зведення статус кодів

| Код | Коли виникає |
|-----|--------------|
| `200` | Успішні GET, PATCH, DELETE |
| `201` | Успішне створення (POST) |
| `404` | Сповіщення з вказаним `id` не існує |
| `422` | Не пройшла валідація (немає `title`/`message` або недопустимий `type`) |
