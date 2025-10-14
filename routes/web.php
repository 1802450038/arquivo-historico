<?php

use App\Http\Controllers\Controller;
use App\Http\Controllers\PostController;
use Illuminate\Support\Facades\Route;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider and all of them will
| be assigned to the "web" middleware group. Make something great!
|
*/

Route::get('/', [PostController::class, 'index'])->name('index');

Route::get('/book{id}', [PostController::class, 'show'])->name('show');



// <img src="{{asset("assets/logo.png")}}" class="h-12 w-auto" alt="logo">