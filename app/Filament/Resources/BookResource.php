<?php

namespace App\Filament\Resources;

use App\Filament\Resources\BookResource\Pages;
use App\Filament\Resources\BookResource\RelationManagers;
use App\Models\Book;
use Filament\Forms;
use Filament\Forms\Components\SpatieMediaLibraryFileUpload as ComponentsSpatieMediaLibraryFileUpload;
use Filament\Forms\Form;
use Filament\Resources\Resource;
use Filament\Tables;
use Filament\Tables\Table;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;
// CORRETO
use Filament\SpatieMediaLibrary\Forms\Components\SpatieMediaLibraryFileUpload;
use Filament\Forms\Components\TextInput; // Importar
use Filament\Infolists\Components\SpatieMediaLibraryImageEntry;

class BookResource extends Resource
{
    protected static ?string $model = Book::class;

    protected static ?string $navigationIcon = 'heroicon-o-rectangle-stack';

public static function form(Form $form): Form
{
    return $form
        ->schema([
            TextInput::make('title')
                ->required()
                ->maxLength(255)
                ->columnSpanFull(),

            ComponentsSpatieMediaLibraryFileUpload::make('images')
                ->collection('images') // Mesmo nome da coleção definida no Model
                ->multiple()          // Permitir múltiplos uploads
                ->reorderable()         // ✨ HABILITAR A REORDENAÇÃO! ✨
                ->image()               // Garantir que apenas imagens sejam aceitas
                ->imageEditor()         // (Opcional) Adicionar um editor básico
                ->columnSpanFull(),
        ]);
}

  public static function table(Table $table): Table
{
    return $table
        ->columns([
            Tables\Columns\TextColumn::make('title')->searchable(),
            Tables\Columns\TextColumn::make('created_at')->dateTime()->sortable(),
        ])
        ->filters([
            //
        ])
        ->actions([
            Tables\Actions\EditAction::make(),
            
            // ↓ AÇÃO PERSONALIZADA PARA GERAR O PDF ↓
            Tables\Actions\Action::make('generate_pdf')
                ->label('Gerar PDF')
                ->icon('heroicon-o-document-arrow-down')
                ->action(function (Book $record) {
                    // 1. Pega todas as mídias da coleção 'images'
                    // A biblioteca já as retorna na ordem correta!
                    $images = $record->getMedia('images');

                    // 2. Carrega uma view Blade com os dados
                    $pdf = Pdf::loadView('pdf.book', [
                        'book' => $record,
                        'images' => $images
                    ]);
                    
                    // 3. Define o nome do arquivo e força o download
                    $fileName = $record->title . '.pdf';
                    return response()->streamDownload(
                        fn() => print($pdf->output()),
                        $fileName
                    );
                }),
        ])
        ->bulkActions([
            Tables\Actions\BulkActionGroup::make([
                Tables\Actions\DeleteBulkAction::make(),
            ]),
        ]);
}

    public static function getRelations(): array
    {
        return [
            //
        ];
    }

    public static function getPages(): array
    {
        return [
            'index' => Pages\ListBooks::route('/'),
            'create' => Pages\CreateBook::route('/create'),
            'edit' => Pages\EditBook::route('/{record}/edit'),
        ];
    }
}
