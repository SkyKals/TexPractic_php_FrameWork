<?php

use App\Http\Controllers\TestController;
use Illuminate\Support\Facades\Route;

Route::apiResource('notifications', TestController::class);
