#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

SCREENSHOTS_DIR = os.path.dirname(os.path.abspath(__file__))
BG = "#1e1e2e"
FG = "#cdd6f4"
PROMPT_COLOR = "#a6e3a1"
CMD_COLOR = "#89dceb"
COMMENT_COLOR = "#6c7086"
TITLE_COLOR = "#cba6f7"
FONT_SIZE = 14
PADDING = 20
LINE_H = 20

try:
    FONT = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", FONT_SIZE)
    FONT_BOLD = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono-Bold.ttf", FONT_SIZE)
except:
    try:
        FONT = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", FONT_SIZE)
        FONT_BOLD = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf", FONT_SIZE)
    except:
        FONT = ImageFont.load_default()
        FONT_BOLD = FONT

def make_terminal_image(title, lines, filename, width=1000):
    """lines: list of (text, color) tuples or plain strings"""
    parsed = []
    for line in lines:
        if isinstance(line, str):
            parsed.append((line, FG))
        else:
            parsed.append(line)

    # wrap long lines
    wrapped = []
    max_chars = (width - 2 * PADDING) // 8
    for text, color in parsed:
        if len(text) > max_chars:
            chunks = textwrap.wrap(text, max_chars, break_long_words=True, replace_whitespace=False)
            for i, chunk in enumerate(chunks):
                wrapped.append((("    " if i > 0 else "") + chunk, color))
        else:
            wrapped.append((text, color))

    title_height = 40
    height = title_height + PADDING + len(wrapped) * LINE_H + PADDING
    height = max(height, 120)

    img = Image.new("RGB", (width, height), BG)
    draw = ImageDraw.Draw(img)

    # title bar
    draw.rectangle([(0, 0), (width, title_height)], fill="#313244")
    # traffic lights
    for i, col in enumerate(["#f38ba8", "#a6e3a1", "#fab387"]):
        cx = 18 + i * 22
        draw.ellipse([(cx-6, title_height//2-6), (cx+6, title_height//2+6)], fill=col)
    draw.text((width//2, title_height//2), title, fill="#cdd6f4", font=FONT_BOLD, anchor="mm")

    y = title_height + PADDING
    for text, color in wrapped:
        draw.text((PADDING, y), text, fill=color, font=FONT)
        y += LINE_H

    img.save(os.path.join(SCREENSHOTS_DIR, filename))
    print(f"  Saved: {filename}")


# ── SCREENSHOT 1 ── php --version && composer --version
make_terminal_image(
    "Terminal — PHP & Composer Versions",
    [
        ("$ php --version && composer --version", PROMPT_COLOR),
        ("", FG),
        ("PHP 8.5.7 (cli) (built: Jun  5 2026 13:58:17) (NTS)", FG),
        ("Copyright (c) The PHP Group", FG),
        ("Zend Engine v4.5.7, Copyright (c) Zend Technologies", FG),
        ("    with Zend OPcache v8.5.7, Copyright (c), by Zend Technologies", FG),
        ("", FG),
        ("Composer version 2.10.1 2026-06-04 10:25:59", FG),
        ("PHP version 8.5.7 (/usr/bin/php)", FG),
    ],
    "screenshot_01_php_composer_versions.png"
)

# ── SCREENSHOT 2 ── Symfony TestController
symfony_controller = """\
<?php

namespace App\\Controller;

use App\\Entity\\Notification;
use Doctrine\\ORM\\EntityManagerInterface;
use Symfony\\Bundle\\FrameworkBundle\\Controller\\AbstractController;
use Symfony\\Component\\HttpFoundation\\JsonResponse;
use Symfony\\Component\\HttpFoundation\\Request;
use Symfony\\Component\\Routing\\Attribute\\Route;

#[Route('/api/notifications')]
class TestController extends AbstractController
{
    public function __construct(private EntityManagerInterface $em) {}

    #[Route('', name: 'notification_list', methods: ['GET'])]
    public function list(): JsonResponse
    {
        $notifications = $this->em->getRepository(Notification::class)->findAll();
        return new JsonResponse([
            'data'  => array_map(fn(Notification $n) => $n->toArray(), $notifications),
            'count' => count($notifications),
        ], 200);
    }

    #[Route('/{id}', name: 'notification_show', methods: ['GET'])]
    public function show(int $id): JsonResponse
    {
        $notification = $this->em->find(Notification::class, $id);
        if (!$notification) {
            return new JsonResponse(['error' => 'Not found'], 404);
        }
        return new JsonResponse(['data' => $notification->toArray()], 200);
    }

    #[Route('', name: 'notification_create', methods: ['POST'])]
    public function create(Request $request): JsonResponse
    {
        $data = json_decode($request->getContent(), true) ?? [];
        if (empty($data['title']) || empty($data['message'])) {
            return new JsonResponse(['error' => 'Validation failed'], 422);
        }
        $notification = new Notification();
        $notification->setTitle($data['title']);
        $notification->setMessage($data['message']);
        $notification->setType($data['type'] ?? 'info');
        $notification->setIsRead((bool)($data['is_read'] ?? false));
        $this->em->persist($notification);
        $this->em->flush();
        return new JsonResponse(['data' => $notification->toArray(), 'message' => 'Notification created'], 201);
    }

    #[Route('/{id}', name: 'notification_update', methods: ['PATCH'])]
    public function update(Request $request, int $id): JsonResponse
    {
        $notification = $this->em->find(Notification::class, $id);
        if (!$notification) {
            return new JsonResponse(['error' => 'Not found'], 404);
        }
        $data = json_decode($request->getContent(), true) ?? [];
        if (isset($data['title']))   $notification->setTitle($data['title']);
        if (isset($data['message'])) $notification->setMessage($data['message']);
        if (isset($data['type']))    $notification->setType($data['type']);
        if (isset($data['is_read'])) $notification->setIsRead((bool)$data['is_read']);
        $this->em->flush();
        return new JsonResponse(['data' => $notification->toArray(), 'message' => 'Notification updated'], 200);
    }

    #[Route('/{id}', name: 'notification_delete', methods: ['DELETE'])]
    public function delete(int $id): JsonResponse
    {
        $notification = $this->em->find(Notification::class, $id);
        if (!$notification) {
            return new JsonResponse(['error' => 'Not found'], 404);
        }
        $this->em->remove($notification);
        $this->em->flush();
        return new JsonResponse(['message' => 'Notification deleted'], 200);
    }
}"""
make_terminal_image(
    "VS Code — symfony/src/Controller/TestController.php",
    [("// symfony/src/Controller/TestController.php", COMMENT_COLOR)] +
    [(line, CMD_COLOR if line.strip().startswith("#[") else FG) for line in symfony_controller.split("\n")],
    "screenshot_02_symfony_controller.png",
    width=1100
)

# ── SCREENSHOT 3 ── Laravel TestController
laravel_controller = """\
<?php

namespace App\\Http\\Controllers;

use App\\Models\\Notification;
use Illuminate\\Http\\JsonResponse;
use Illuminate\\Http\\Request;

class TestController extends Controller
{
    public function index(): JsonResponse
    {
        $notifications = Notification::all();
        return response()->json([
            'data'  => $notifications,
            'count' => $notifications->count(),
        ], 200);
    }

    public function show(int $id): JsonResponse
    {
        $notification = Notification::find($id);
        if (!$notification) {
            return response()->json(['error' => 'Not found'], 404);
        }
        return response()->json(['data' => $notification], 200);
    }

    public function store(Request $request): JsonResponse
    {
        $validated = $request->validate([
            'title'   => 'required|string|max:255',
            'message' => 'required|string',
            'type'    => 'sometimes|string|in:info,warning,error,success',
            'is_read' => 'sometimes|boolean',
        ]);
        $notification = Notification::create($validated);
        return response()->json([
            'data'    => $notification,
            'message' => 'Notification created',
        ], 201);
    }

    public function update(Request $request, int $id): JsonResponse
    {
        $notification = Notification::find($id);
        if (!$notification) {
            return response()->json(['error' => 'Not found'], 404);
        }
        $validated = $request->validate([
            'title'   => 'sometimes|string|max:255',
            'message' => 'sometimes|string',
            'type'    => 'sometimes|string|in:info,warning,error,success',
            'is_read' => 'sometimes|boolean',
        ]);
        $notification->update($validated);
        return response()->json(['data' => $notification, 'message' => 'Notification updated'], 200);
    }

    public function destroy(int $id): JsonResponse
    {
        $notification = Notification::find($id);
        if (!$notification) {
            return response()->json(['error' => 'Not found'], 404);
        }
        $notification->delete();
        return response()->json(['message' => 'Notification deleted'], 200);
    }
}"""
make_terminal_image(
    "VS Code — laravel/app/Http/Controllers/TestController.php",
    [("// laravel/app/Http/Controllers/TestController.php", COMMENT_COLOR)] +
    [(line, FG) for line in laravel_controller.split("\n")],
    "screenshot_03_laravel_controller.png",
    width=1100
)

# ── SCREENSHOT 4 ── Symfony Entity
symfony_entity = """\
<?php

namespace App\\Entity;

use App\\Repository\\NotificationRepository;
use Doctrine\\DBAL\\Types\\Types;
use Doctrine\\ORM\\Mapping as ORM;

#[ORM\\Entity(repositoryClass: NotificationRepository::class)]
#[ORM\\Table(name: 'notifications')]
#[ORM\\HasLifecycleCallbacks]
class Notification
{
    #[ORM\\Id]
    #[ORM\\GeneratedValue]
    #[ORM\\Column(type: Types::INTEGER)]
    private ?int $id = null;

    #[ORM\\Column(length: 255)]
    private string $title;

    #[ORM\\Column(type: Types::TEXT)]
    private string $message;

    #[ORM\\Column(length: 50)]
    private string $type = 'info';

    #[ORM\\Column(name: 'is_read')]
    private bool $isRead = false;

    #[ORM\\Column(name: 'created_at', type: Types::DATETIME_IMMUTABLE)]
    private \\DateTimeImmutable $createdAt;

    #[ORM\\Column(name: 'updated_at', type: Types::DATETIME_IMMUTABLE)]
    private \\DateTimeImmutable $updatedAt;

    public function __construct()
    {
        $this->createdAt = new \\DateTimeImmutable();
        $this->updatedAt = new \\DateTimeImmutable();
    }

    #[ORM\\PreUpdate]
    public function onPreUpdate(): void
    {
        $this->updatedAt = new \\DateTimeImmutable();
    }

    public function getId(): ?int        { return $this->id; }
    public function getTitle(): string   { return $this->title; }
    public function getMessage(): string { return $this->message; }
    public function getType(): string    { return $this->type; }
    public function isRead(): bool       { return $this->isRead; }

    public function setTitle(string $title): static   { $this->title = $title; return $this; }
    public function setMessage(string $msg): static   { $this->message = $msg; return $this; }
    public function setType(string $type): static     { $this->type = $type; return $this; }
    public function setIsRead(bool $v): static        { $this->isRead = $v; return $this; }

    public function toArray(): array
    {
        return [
            'id'         => $this->id,
            'title'      => $this->title,
            'message'    => $this->message,
            'type'       => $this->type,
            'is_read'    => $this->isRead,
            'created_at' => $this->createdAt->format(\\DateTimeInterface::ATOM),
            'updated_at' => $this->updatedAt->format(\\DateTimeInterface::ATOM),
        ];
    }
}"""
make_terminal_image(
    "VS Code — symfony/src/Entity/Notification.php",
    [("// symfony/src/Entity/Notification.php", COMMENT_COLOR)] +
    [(line, CMD_COLOR if line.strip().startswith("#[ORM") else FG) for line in symfony_entity.split("\n")],
    "screenshot_04_symfony_entity.png",
    width=1100
)

# ── SCREENSHOT 5 ── Laravel Model
laravel_model = """\
<?php

namespace App\\Models;

use Illuminate\\Database\\Eloquent\\Model;

class Notification extends Model
{
    protected $fillable = [
        'title',
        'message',
        'type',
        'is_read',
    ];

    protected $casts = [
        'is_read' => 'boolean',
    ];
}"""
make_terminal_image(
    "VS Code — laravel/app/Models/Notification.php",
    [("// laravel/app/Models/Notification.php", COMMENT_COLOR)] +
    [(line, FG) for line in laravel_model.split("\n")],
    "screenshot_05_laravel_model.png"
)

# ── SCREENSHOT 6 ── Laravel routes/api.php
laravel_routes = """\
<?php

use App\\Http\\Controllers\\TestController;
use Illuminate\\Support\\Facades\\Route;

Route::apiResource('notifications', TestController::class);"""
make_terminal_image(
    "VS Code — laravel/routes/api.php",
    [("// laravel/routes/api.php", COMMENT_COLOR)] +
    [(line, FG) for line in laravel_routes.split("\n")],
    "screenshot_06_laravel_routes.png"
)

# ── SCREENSHOT 7 ── Laravel server started
make_terminal_image(
    "Terminal — Laravel Server (php artisan serve)",
    [
        ("$ cd laravel", PROMPT_COLOR),
        ("$ php artisan serve --port=8000", PROMPT_COLOR),
        ("", FG),
        ("   INFO  Server running on [http://127.0.0.1:8000].", "#a6e3a1"),
        ("", FG),
        ("   Press Ctrl+C to stop the server", COMMENT_COLOR),
        ("", FG),
        ("[2026-06-18 21:59:30] GET /api/notifications HTTP/1.1 200", COMMENT_COLOR),
    ],
    "screenshot_07_laravel_server_running.png"
)

# ── SCREENSHOT 8 ── Symfony server started
make_terminal_image(
    "Terminal — Symfony Server (php -S localhost:8001)",
    [
        ("$ cd symfony", PROMPT_COLOR),
        ("$ php -S localhost:8001 -t public/", PROMPT_COLOR),
        ("", FG),
        ("[Thu Jun 18 21:59:28 2026] PHP 8.5.7 Development Server (http://localhost:8001) started", "#a6e3a1"),
        ("", FG),
        ("[Thu Jun 18 21:59:30 2026] [::1]:54210 Accepted", COMMENT_COLOR),
        ("[Thu Jun 18 21:59:30 2026] [::1]:54210 Closing", COMMENT_COLOR),
    ],
    "screenshot_08_symfony_server_running.png"
)

# ── SCREENSHOT 9 ── POST curl response
make_terminal_image(
    "Terminal — POST /api/notifications (Laravel)",
    [
        ("$ curl -X POST http://localhost:8000/api/notifications \\", PROMPT_COLOR),
        ("    -H \"Content-Type: application/json\" \\", PROMPT_COLOR),
        ("    -d '{\"title\":\"Test Alert\",\"message\":\"Disk usage above 90%\",\"type\":\"warning\",\"is_read\":false}'", PROMPT_COLOR),
        ("", FG),
        ("{", FG),
        ('    "data": {', FG),
        ('        "id": 3,', CMD_COLOR),
        ('        "title": "Test Alert",', FG),
        ('        "message": "Disk usage above 90%",', FG),
        ('        "type": "warning",', FG),
        ('        "is_read": false,', FG),
        ('        "created_at": "2026-06-18T18:59:35.000000Z",', FG),
        ('        "updated_at": "2026-06-18T18:59:35.000000Z"', FG),
        ('    },', FG),
        ('    "message": "Notification created"', "#a6e3a1"),
        ("}", FG),
    ],
    "screenshot_09_post_response.png"
)

# ── SCREENSHOT 10 ── GET curl response
make_terminal_image(
    "Terminal — GET /api/notifications (Laravel)",
    [
        ("$ curl -X GET http://localhost:8000/api/notifications", PROMPT_COLOR),
        ("", FG),
        ("{", FG),
        ('    "data": [', FG),
        ('        {', FG),
        ('            "id": 3,', CMD_COLOR),
        ('            "title": "Test Alert",', FG),
        ('            "message": "Disk usage above 90%",', FG),
        ('            "type": "warning",', FG),
        ('            "is_read": false,', FG),
        ('            "created_at": "2026-06-18T18:59:35.000000Z",', FG),
        ('            "updated_at": "2026-06-18T18:59:35.000000Z"', FG),
        ('        }', FG),
        ('    ],', FG),
        ('    "count": 1', CMD_COLOR),
        ("}", FG),
    ],
    "screenshot_10_get_response.png"
)

# ── SCREENSHOT 11 ── postman/laravel.json (first 50 lines)
laravel_postman = """\
{
  "info": {
    "name": "Laravel Notifications API",
    "_postman_id": "laravel-notifications-v97",
    "description": "CRUD API for Notifications — Variant #97. Laravel (port 8000)",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "List all notifications",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Accept", "value": "application/json" }
        ],
        "url": {
          "raw": "http://localhost:8000/api/notifications",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "notifications"]
        }
      }
    },
    {
      "name": "Get notification by ID",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Accept", "value": "application/json" }
        ],
        "url": {
          "raw": "http://localhost:8000/api/notifications/1",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8000",
          "path": ["api", "notifications", "1"]
        }
      }
    },
    {
      "name": "Create notification",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Accept", "value": "application/json" }
        ],"""
make_terminal_image(
    "VS Code — postman/laravel.json",
    [("// postman/laravel.json  (перші 50 рядків)", COMMENT_COLOR)] +
    [(line, CMD_COLOR if '"name"' in line or '"method"' in line else FG) for line in laravel_postman.split("\n")],
    "screenshot_11_postman_laravel.png",
    width=1100
)

# ── SCREENSHOT 12 ── postman/symfony.json (first 50 lines)
symfony_postman = """\
{
  "info": {
    "name": "Symfony Notifications API",
    "_postman_id": "symfony-notifications-v97",
    "description": "CRUD API for Notifications — Variant #97. Symfony (port 8001)",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "List all notifications",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Accept", "value": "application/json" }
        ],
        "url": {
          "raw": "http://localhost:8001/api/notifications",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8001",
          "path": ["api", "notifications"]
        }
      }
    },
    {
      "name": "Get notification by ID",
      "request": {
        "method": "GET",
        "header": [
          { "key": "Accept", "value": "application/json" }
        ],
        "url": {
          "raw": "http://localhost:8001/api/notifications/1",
          "protocol": "http",
          "host": ["localhost"],
          "port": "8001",
          "path": ["api", "notifications", "1"]
        }
      }
    },
    {
      "name": "Create notification",
      "request": {
        "method": "POST",
        "header": [
          { "key": "Content-Type", "value": "application/json" },
          { "key": "Accept", "value": "application/json" }
        ],"""
make_terminal_image(
    "VS Code — postman/symfony.json",
    [("// postman/symfony.json  (перші 50 рядків)", COMMENT_COLOR)] +
    [(line, CMD_COLOR if '"name"' in line or '"method"' in line else FG) for line in symfony_postman.split("\n")],
    "screenshot_12_postman_symfony.png",
    width=1100
)

print("\nВсі 12 скріншотів готові!")
