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
use Barryvdh\DomPDF\Facade\Pdf;
use Filament\Forms\Components\FileUpload;
use Filament\Forms\Components\Tabs;
use Illuminate\Database\Eloquent\Builder;
use Illuminate\Database\Eloquent\SoftDeletingScope;
use Illuminate\Support\Facades\Storage;
// CORRETO
use Filament\SpatieMediaLibrary\Forms\Components\SpatieMediaLibraryFileUpload;
use Filament\Forms\Components\TextInput; // Importar
use Filament\Infolists\Components\SpatieMediaLibraryImageEntry;
use Illuminate\Support\Str;
use Filament\Forms\Get;

class BookResource extends Resource
{
    protected static ?string $model = Book::class;

    protected static ?string $slug = 'Livros';

    protected static ?string $title = 'Livros';


    protected static ?string $navigationIcon = 'heroicon-o-book-open';

    protected static ?string $navigationLabel = 'Livros';

    public static function form(Form $form): Form
    {
        return $form
            ->schema([
                TextInput::make('title')
                    ->label('Titulo')
                    ->required()
                    ->maxLength(255)
                    ->columnSpanFull(),

                Tabs::make('Método de envio do arquivo ')
                    ->tabs([
                        Tabs\Tab::make('Upload de Imagens')->schema([
                            ComponentsSpatieMediaLibraryFileUpload::make('images')
                                ->label('Imagens do Livro')
                                ->collection('images') // Mesmo nome da coleção definida no Model
                                ->multiple()          // Permitir múltiplos uploads
                                ->reorderable()         // ✨ HABILITAR A REORDENAÇÃO! ✨
                                ->image()               // Garantir que apenas imagens sejam aceitas
                                ->imageEditor()         // (Opcional) Adicionar um editor básico
                                ->panelLayout('grid')
                                ->maxSize(5120)
                                ->maxFiles(200)
                                ->columnSpanFull(),

                        ]),
                        Tabs\Tab::make('Enviar PDF Pronto')
                            ->schema([
                                FileUpload::make('book_pdf_file')
                                    ->label('') // O rótulo da aba já é suficiente
                                    ->disk('public')
                                    ->directory('pdfs')
                                    ->visibility('public')
                                    ->downloadable()
                                    ->openable()
                                    ->acceptedFileTypes(['application/pdf']) // Garante que só PDFs sejam aceitos
                                    ->getUploadedFileNameForStorageUsing(fn(Get $get) => Str::slug($get('title')) . '.pdf')
                                    ->uploadingMessage('Enviando arquivo PDF...')
                                    ->columnSpanFull(),
                            ]),

                    ])->columnSpanFull(),



                FileUpload::make('book_pdf_file')
                    ->label('PDF Gerado')
                    ->downloadable()
                    ->openable()
                    ->columnSpanFull()
                    ->visible(fn($record) => $record !== null),


            ]);
    }

    public static function table(Table $table): Table
    {
        return $table
            ->columns([
                Tables\Columns\TextColumn::make('title')->searchable()
                    ->label('Titulo'),
                Tables\Columns\TextColumn::make('created_at')->since(),
                Tables\Columns\TextColumn::make('created_at')->dateTime()->sortable()
                    ->label('Criado em')->toggleable(isToggledHiddenByDefault: true),
                Tables\Columns\TextColumn::make('updated_at')->dateTime()->sortable()
                    ->label('Atualizado em')->toggleable(isToggledHiddenByDefault: true),
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
                        // 1. Pega as imagens da coleção 'images'
                        $images = $record->getMedia('images')->reverse();
                        if ($images->isEmpty()) {
                            // Opcional: notificar o usuário que não há imagens
                            return;
                        }

                        // 2. Garante que o diretório exista
                        Storage::disk('public')->makeDirectory('pdfs');

                        // 3. Define o nome e o caminho do arquivo
                        $fileName = \Illuminate\Support\Str::slug($record->title) . '.pdf';
                        $filePath = 'pdfs/' . $fileName;

                        // 4. Carrega a view e gera o PDF
                        $pdf = Pdf::loadView('pdf.book', [
                            'book' => $record,
                            'images' => $images
                        ]);

                        // 5. Salva o PDF no disco 'public'
                        Storage::disk('public')->put($filePath, $pdf->output());

                        // 6. Atualiza o campo no livro
                        $record->update([
                            'book_pdf_file' => $filePath
                        ]);
                    })
                    ->successNotificationTitle('PDF gerado e salvo com sucesso!'),
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
