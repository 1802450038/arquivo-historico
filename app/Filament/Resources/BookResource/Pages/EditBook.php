<?php

namespace App\Filament\Resources\BookResource\Pages;

use App\Filament\Resources\BookResource;
use Filament\Actions;
use Filament\Resources\Pages\EditRecord;

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
                    $images = $record->getMedia('images')->reverse();

                    $pdf = Pdf::loadView('pdf.book', [
                        'book' => $record,
                        'images' => $images
                    ]);
                    
                    $fileName = $record->title . '.pdf';

                    return response()->streamDownload(
                        fn() => print($pdf->output()),
                        $fileName
                    );
                }),
            
            // Botão padrão de Cancelar
            $this->getCancelFormAction(),
        ];
    }

}
