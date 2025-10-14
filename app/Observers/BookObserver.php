<?php

namespace App\Observers;

use App\Models\Book;
use Barryvdh\DomPDF\Facade\Pdf;
use Illuminate\Support\Facades\Storage;

class BookObserver
{
    /**
     * Handle the Book "saved" event.
     */
    public function saved(Book $book): void
    {
        // Garante que o diretório de destino exista
        Storage::disk('public')->makeDirectory('books_pdf');

        // Pega as imagens associadas ao livro, na ordem correta
        $images = $book->getMedia('images');

        // Se não houver imagens, não faz nada
        if ($images->isEmpty()) {
            return;
        }

        // Define o nome e o caminho do arquivo PDF
        $pdfFileName = 'book_' . $book->id . '_' . time() . '.pdf';
        $pdfPath = 'books_pdf/' . $pdfFileName;

        // Carrega a view e gera o PDF
        $pdf = Pdf::loadView('pdf.book', ['book' => $book, 'images' => $images]);

        // Salva o PDF no disco 'public'
        Storage::disk('public')->put($pdfPath, $pdf->output());

        // Atualiza o campo no modelo Book sem disparar o evento 'saved' novamente
        Book::where('id', $book->id)->update([
            'book_pdf_file' => $pdfPath
        ]);
    }

    /**
     * Handle the Book "created" event.
     */
    public function created(Book $book): void
    {
        //
    }

    /**
     * Handle the Book "updated" event.
     */
    public function updated(Book $book): void
    {
        //
    }

    /**
     * Handle the Book "deleted" event.
     */
    public function deleted(Book $book): void
    {
        //
    }

    /**
     * Handle the Book "restored" event.
     */
    public function restored(Book $book): void
    {
        //
    }

    /**
     * Handle the Book "force deleted" event.
     */
    public function forceDeleted(Book $book): void
    {
        //
    }
}