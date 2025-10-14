<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8"/>
    <title>{{ $book->title }}</title>
    <style>
        /* Define as margens da página */
        @page {
            margin: 25px;
        }

        body {
            font-family: sans-serif;
        }

        h1 {
            text-align: center;
            margin-bottom: 40px;
        }

        /* Container para cada imagem */
        .image-container {
            /* ESSA É A REGRA MAIS IMPORTANTE: */
            /* Tenta evitar que a imagem seja dividida entre duas páginas */
            page-break-inside: avoid;
            
            /* Garante que o container ocupe 100% da largura disponível */
            width: 100%;
            
            /* Adiciona um espaço abaixo de cada imagem */
            margin-bottom: 25px; 
        }

        /* Estilo da imagem em si */
        .image-container img {
            /* Garante que a imagem nunca ultrapasse a largura do container (e da página) */
            max-width: 100%;
            
            /* Mantém a proporção da imagem */
            height: auto;
        }

        /* Classe para forçar a quebra de página, se necessário no futuro */
        .page-break {
            page-break-after: always;
        }
    </style>
</head>
<body>
    <h1>{{ $book->title }}</h1>

    @foreach ($images as $image)
        <div class="image-container">
            <img src="{{ $image->getPath() }}" alt="">
        </div>
    @endforeach
</body>
</html>