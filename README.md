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

## AI Agents

The project ships with four **Claude Code subagents** in `.claude/agents/`. Each is a specialized assistant with a focused role and a restricted toolset:

| Agent | Role | Responsibility |
|-------|------|----------------|
| `dev` | PHP Developer | Writes and edits PHP code (controllers, models, entities, migrations, routes) for Laravel and Symfony following PSR-12, JSON-only APIs, SQLite, and input validation. |
| `reviewer` | Code Reviewer | Checks that all five CRUD endpoints exist, HTTP status codes are correct (200/201/404/422), input is validated, and Laravel/Symfony stay in parity. Reports only, never edits. |
| `git-manager` | Git Engineer | Manages branches, commits and merges: branches from `dev`, Conventional Commits, merges only with `--no-ff`, never pushes directly to `main`. |
| `docs-writer` | Technical Writer | Creates and maintains API documentation and Postman collections strictly from the real code. |

---

## Documentation

| Document | Description |
|----------|-------------|
| [`docs/API.md`](docs/API.md) | Full API reference for both frameworks — endpoints, request/response examples, status codes, curl examples, validation rules. |
| [`docs/PROMPTS.md`](docs/PROMPTS.md) | Chronological log of the AI prompts used to build the project. |
| [`CLAUDE.md`](CLAUDE.md) | Developer/agent guide — repository structure, git rules, model and endpoint reference. |

---

## Project Structure

```
frameworks/
├── .claude/
│   └── agents/         # Claude Code subagents
│       ├── dev.md
│       ├── reviewer.md
│       ├── git-manager.md
│       └── docs-writer.md
├── docs/
│   ├── API.md          # Full API documentation
│   └── PROMPTS.md      # AI prompt log
├── laravel/            # Laravel application
├── symfony/            # Symfony application
├── postman/
│   ├── laravel.json    # Postman collection (Laravel)
│   └── symfony.json    # Postman collection (Symfony)
├── CLAUDE.md           # Developer documentation
└── README.md           # This file
```
