<?php

use App\Http\Controllers\NotificationController;
use Illuminate\Support\Facades\Route;

Route::apiResource('notifications', NotificationController::class);
