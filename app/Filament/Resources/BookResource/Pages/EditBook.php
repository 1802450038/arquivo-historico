<?php

namespace App\Filament\Resources\BookResource\Pages;

use App\Filament\Resources\BookResource;
use App\Models\Book;
use Filament\Actions;
use Filament\Resources\Pages\EditRecord;
use Barryvdh\DomPDF\Facade\Pdf;
use Illuminate\Support\Facades\Storage;
use Filament\Notifications\Notification;

class EditBook extends EditRecord
{
    protected static string $resource = BookResource::class;

    protected function getHeaderActions(): array
    {
        return [
            Actions\DeleteAction::make(),
        ];
    }

     protected function getFormActions(): array
    {
        return [
            // Botão padrão de Salvar Alterações
            $this->getSaveFormAction(),

            // NOSSO BOTÃO PERSONALIZADO
            Actions\Action::make('generate_pdf')
                ->label('Gerar PDF')
                ->icon('heroicon-o-arrow-down-tray') // Ícone de download
                ->color('success')                    // Cor verde
                ->action(function (Book $record) {
                    Notification::make()
                        ->title('Gerando PDF, por favor aguarde...')
                        ->info()
                        ->send();

                    $images = $record->getMedia('images')->reverse();
                    if ($images->isEmpty()) {
                        Notification::make()
                            ->title('Nenhuma imagem encontrada')
                            ->warning()
                            ->send();
                        return;
                    }

                    Storage::disk('public')->makeDirectory('pdfs');
                    $fileName = \Illuminate\Support\Str::slug($record->title) . '.pdf';
                    $filePath = 'pdfs/' . $fileName;

                    $pdf = Pdf::loadView('pdf.book', [
                        'book' => $record,
                        'images' => $images
                    ]);

                    Storage::disk('public')->put($filePath, $pdf->output());

                    $record->update([
                        'book_pdf_file' => $filePath
                    ]);

                    $this->refreshFormData(['book_pdf_file']);
                })
                ->successNotificationTitle('PDF gerado e salvo com sucesso!'),
            
            // Botão padrão de Cancelar
            $this->getCancelFormAction(),
        ];
    }

}
