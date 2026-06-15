# frameworks — Notifications CRUD (Variant #97)

## Project Description

University practical work implementing a **Notifications CRUD REST API** in two PHP frameworks:
- **Laravel** (port 8000) — MVC with Eloquent ORM
- **Symfony** (port 8001) — Doctrine ORM with attributes routing

Both use **SQLite** as the database. No external DB required.

---

## Repository Structure

```
frameworks/
├── CLAUDE.md              # this file
├── README.md              # setup & usage guide
├── laravel/               # Laravel 11 application
│   ├── app/
│   │   ├── Http/Controllers/NotificationController.php
│   │   └── Models/Notification.php
│   ├── database/
│   │   ├── migrations/XXXX_create_notifications_table.php
│   │   └── database.sqlite
│   └── routes/api.php
├── symfony/               # Symfony 7 application
│   ├── src/
│   │   ├── Controller/NotificationController.php
│   │   └── Entity/Notification.php
│   └── var/data.db
└── postman/
    ├── laravel.json       # Postman collection for Laravel API
    └── symfony.json       # Postman collection for Symfony API
```

---

## Git Rules

### Branches

| Branch | Purpose |
|--------|---------|
| `main` | Production-ready, stable code only |
| `dev` | Integration branch, merges from feature branches |
| `feature/laravel-notifications` | Laravel CRUD implementation |
| `feature/symfony-notifications` | Symfony CRUD implementation |
| `feature/postman-collections` | Postman API collections |

### Workflow

```
feature/* → dev → main
```

All feature branches are merged into `dev` with `--no-ff`. Then `dev` is merged into `main` for release.

### Commit Format — Conventional Commits

```
<type>: <short description>

Types:
  feat     — new feature
  fix      — bug fix
  docs     — documentation only
  refactor — code refactoring
  test     — adding tests
  chore    — build/tooling changes
  merge    — branch merge
  release  — version release
```

Examples:
```
feat: add Notification CRUD for Laravel with SQLite
feat: add Notification CRUD for Symfony with SQLite
docs: add Postman collections for Laravel and Symfony APIs
merge: Laravel Notifications CRUD
release: Notifications CRUD complete
```

---

## Agents

### @dev
**Role:** Backend Developer
**Responsibilities:**
- Implement CRUD endpoints in Laravel and Symfony
- Write migrations and entities
- Ensure proper HTTP status codes and JSON responses
- Run artisan/console commands for DB setup

### @review
**Role:** Code Reviewer
**Responsibilities:**
- Review pull requests on `dev` and `main`
- Check code style, validation logic, error handling
- Verify API responses match specification
- Ensure no external DB dependencies (SQLite only)

### @git
**Role:** Git & CI/CD Manager
**Responsibilities:**
- Manage branch lifecycle (create, merge, delete)
- Enforce Conventional Commits format
- Handle merges with `--no-ff` to preserve history
- Push to remote, create tags for releases

### @docs
**Role:** Documentation Writer
**Responsibilities:**
- Maintain README.md and CLAUDE.md
- Create and update Postman collections
- Document all API endpoints with examples
- Write setup and run instructions

---

## API Endpoints

### Laravel (http://localhost:8000)

| Method | URL | Description | Status |
|--------|-----|-------------|--------|
| GET | `/api/notifications` | List all notifications | 200 |
| GET | `/api/notifications/{id}` | Get single notification | 200 / 404 |
| POST | `/api/notifications` | Create notification | 201 |
| PATCH | `/api/notifications/{id}` | Update notification | 200 / 404 |
| DELETE | `/api/notifications/{id}` | Delete notification | 200 / 404 |

### Symfony (http://localhost:8001)

| Method | URL | Description | Status |
|--------|-----|-------------|--------|
| GET | `/api/notifications` | List all notifications | 200 |
| GET | `/api/notifications/{id}` | Get single notification | 200 / 404 |
| POST | `/api/notifications` | Create notification | 201 |
| PATCH | `/api/notifications/{id}` | Update notification | 200 / 404 |
| DELETE | `/api/notifications/{id}` | Delete notification | 200 / 404 |

---

## Notification Model

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `id` | integer (auto) | — | Primary key |
| `title` | string (255) | — | Required |
| `message` | text | — | Required |
| `type` | string (50) | `'info'` | One of: info, warning, error, success |
| `is_read` | boolean | `false` | |
| `created_at` | datetime | now | Auto-set |
| `updated_at` | datetime | now | Auto-updated |

### JSON Example

```json
{
  "id": 1,
  "title": "System Alert",
  "message": "Disk usage is above 90%",
  "type": "warning",
  "is_read": false,
  "created_at": "2026-06-16T10:00:00.000000Z",
  "updated_at": "2026-06-16T10:00:00.000000Z"
}
```

---

## HTTP Status Codes

| Code | Meaning | When Used |
|------|---------|-----------|
| 200 | OK | Successful GET, PATCH, DELETE |
| 201 | Created | Successful POST |
| 404 | Not Found | Record does not exist |
| 422 | Unprocessable Entity | Validation failed |

---

## Running the Projects

### Laravel

```bash
cd laravel
php artisan migrate          # run migrations
php artisan serve            # starts at http://localhost:8000
```

### Symfony

```bash
cd symfony
php bin/console doctrine:database:create
php bin/console doctrine:migrations:migrate --no-interaction
symfony serve --port=8001    # or: php -S localhost:8001 -t public/
```

---

## Validation Rules

### POST /api/notifications
```
title:    required | string | max:255
message:  required | string
type:     optional | in:info,warning,error,success (default: info)
is_read:  optional | boolean (default: false)
```

### PATCH /api/notifications/{id}
All fields optional, same rules as POST.
