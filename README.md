# Notifications CRUD — Variant #97

University practical work implementing a Notifications CRUD REST API in two PHP frameworks: **Laravel** and **Symfony**, both using **SQLite**.

---

## Installation & Running

### Laravel (port 8000)

```bash
cd laravel

# 1. Install dependencies (already done if vendor/ exists)
composer install

# 2. Copy environment file
cp .env.example .env
php artisan key:generate

# 3. Run migrations (SQLite database is auto-created)
php artisan migrate

# 4. Start the development server
php artisan serve
# → http://localhost:8000
```

### Symfony (port 8001)

```bash
cd symfony

# 1. Install dependencies (already done if vendor/ exists)
composer install --ignore-platform-req=ext-iconv

# 2. Run migrations (creates var/data.db automatically)
php bin/console doctrine:migrations:migrate --no-interaction

# 3. Start the development server
php -S localhost:8001 -t public/
# → http://localhost:8001
```

---

## API Endpoints

### Laravel — http://localhost:8000

| Method | URL | Description | Success Status |
|--------|-----|-------------|----------------|
| GET | `/api/notifications` | List all notifications | 200 |
| GET | `/api/notifications/{id}` | Get single notification | 200 |
| POST | `/api/notifications` | Create notification | 201 |
| PATCH | `/api/notifications/{id}` | Update notification | 200 |
| DELETE | `/api/notifications/{id}` | Delete notification | 200 |

### Symfony — http://localhost:8001

| Method | URL | Description | Success Status |
|--------|-----|-------------|----------------|
| GET | `/api/notifications` | List all notifications | 200 |
| GET | `/api/notifications/{id}` | Get single notification | 200 |
| POST | `/api/notifications` | Create notification | 201 |
| PATCH | `/api/notifications/{id}` | Update notification | 200 |
| DELETE | `/api/notifications/{id}` | Delete notification | 200 |

---

## Example Requests

### Create (POST)
```json
{
  "title": "System Alert",
  "message": "Disk usage is above 90%",
  "type": "warning",
  "is_read": false
}
```

### Update (PATCH)
```json
{
  "title": "Updated Title",
  "is_read": true
}
```

### Response format (GET list)
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

---

## Notification Model

| Field | Type | Default | Allowed Values |
|-------|------|---------|----------------|
| `id` | integer | auto | — |
| `title` | string (255) | required | — |
| `message` | text | required | — |
| `type` | string | `info` | info, warning, error, success |
| `is_read` | boolean | `false` | true, false |
| `created_at` | datetime | auto | — |
| `updated_at` | datetime | auto | — |

---

## HTTP Status Codes

| Code | Meaning |
|------|---------|
| 200 | OK — request succeeded |
| 201 | Created — new record created |
| 404 | Not Found — record does not exist |
| 422 | Unprocessable Entity — validation failed |

---

## Postman Collections

Import the collection files into Postman:

1. Open Postman → **Import**
2. Select file:
   - `postman/laravel.json` — for Laravel API (port 8000)
   - `postman/symfony.json` — for Symfony API (port 8001)
3. Run requests from the imported collection

---

## Project Structure

```
frameworks/
├── laravel/            # Laravel 11 application
├── symfony/            # Symfony 7 application
├── postman/
│   ├── laravel.json    # Postman collection (Laravel)
│   └── symfony.json    # Postman collection (Symfony)
├── CLAUDE.md           # Developer documentation
└── README.md           # This file
```
