<?php

namespace App\Http\Controllers;

use App\Models\Notification;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;

class NotificationController extends Controller
{
    public function index(): JsonResponse
    {
        $notifications = Notification::all();

        return response()->json([
            'data' => $notifications,
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

        return response()->json([
            'data'    => $notification,
            'message' => 'Notification updated',
        ], 200);
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
}
