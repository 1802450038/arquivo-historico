<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Model;
use Spatie\MediaLibrary\HasMedia;
use Spatie\MediaLibrary\InteractsWithMedia;

class Book extends Model implements HasMedia
{
    use HasFactory, InteractsWithMedia;

    protected $fillable = [
        'title',
    ];

    // Opcional, mas recomendado: definir uma "coleção" para as imagens
    public function registerMediaCollections(): void
    {
        $this->addMediaCollection('images');
    }

    public function post()
    {
        return $this->hasOne(Post::class);
    }
}