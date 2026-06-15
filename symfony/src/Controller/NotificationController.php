<?php

namespace App\Controller;

use App\Entity\Notification;
use Doctrine\ORM\EntityManagerInterface;
use Symfony\Bundle\FrameworkBundle\Controller\AbstractController;
use Symfony\Component\HttpFoundation\JsonResponse;
use Symfony\Component\HttpFoundation\Request;
use Symfony\Component\Routing\Attribute\Route;

#[Route('/api/notifications')]
class NotificationController extends AbstractController
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
            return new JsonResponse([
                'error'  => 'Validation failed',
                'errors' => [
                    'title'   => empty($data['title']) ? 'Title is required' : null,
                    'message' => empty($data['message']) ? 'Message is required' : null,
                ],
            ], 422);
        }

        $validTypes = ['info', 'warning', 'error', 'success'];
        $type = $data['type'] ?? 'info';
        if (!in_array($type, $validTypes, true)) {
            return new JsonResponse(['error' => 'Invalid type. Must be one of: ' . implode(', ', $validTypes)], 422);
        }

        $notification = new Notification();
        $notification->setTitle($data['title']);
        $notification->setMessage($data['message']);
        $notification->setType($type);
        $notification->setIsRead((bool)($data['is_read'] ?? false));

        $this->em->persist($notification);
        $this->em->flush();

        return new JsonResponse([
            'data'    => $notification->toArray(),
            'message' => 'Notification created',
        ], 201);
    }

    #[Route('/{id}', name: 'notification_update', methods: ['PATCH'])]
    public function update(Request $request, int $id): JsonResponse
    {
        $notification = $this->em->find(Notification::class, $id);

        if (!$notification) {
            return new JsonResponse(['error' => 'Not found'], 404);
        }

        $data = json_decode($request->getContent(), true) ?? [];

        if (isset($data['title'])) {
            $notification->setTitle($data['title']);
        }
        if (isset($data['message'])) {
            $notification->setMessage($data['message']);
        }
        if (isset($data['type'])) {
            $validTypes = ['info', 'warning', 'error', 'success'];
            if (!in_array($data['type'], $validTypes, true)) {
                return new JsonResponse(['error' => 'Invalid type'], 422);
            }
            $notification->setType($data['type']);
        }
        if (isset($data['is_read'])) {
            $notification->setIsRead((bool)$data['is_read']);
        }

        $this->em->flush();

        return new JsonResponse([
            'data'    => $notification->toArray(),
            'message' => 'Notification updated',
        ], 200);
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

        return new JsonResponse(['message' => 'Deleted'], 200);
    }
}
