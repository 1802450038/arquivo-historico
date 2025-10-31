<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Arquivo Histórico de Uruguaiana</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;700&family=Lora:wght@400;500;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Poppins', sans-serif;
        }
        .font-lora {
            font-family: 'Lora', serif;
        }
    </style>
</head>
<body class="bg-stone-100 text-stone-800 flex flex-col min-h-screen">

    <!-- Cabeçalho -->
    <header class="bg-white shadow-md">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-24">
                <!-- Logo e Título -->
                <div class="flex items-center space-x-4">
                    <!-- NOTA: Imagem do logo ajustada. -->
                    <img src="{{asset("assets/logo.png")}}" class="h-12 w-auto" alt="logo">
                    <h1 class="text-2xl sm:text-3xl font-bold font-lora text-stone-700 hidden sm:block">Arquivo Histórico</h1>
                </div>

                <!-- Barra de Pesquisa -->
                <div class="w-full max-w-lg">
                    <div class="relative">
                        <span class="absolute inset-y-0 left-0 flex items-center pl-3">
                            <svg class="h-5 w-5 text-gray-400" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor">
                                <path fill-rule="evenodd" d="M9 3.5a5.5 5.5 0 100 11 5.5 5.5 0 000-11zM2 9a7 7 0 1112.452 4.391l3.328 3.329a.75.75 0 11-1.06 1.06l-3.329-3.328A7 7 0 012 9z" clip-rule="evenodd" />
                            </svg>
                        </span>
                        <input
                            type="text"
                            placeholder="Pesquisar documentos..."
                            class="w-full pl-10 pr-4 py-2 border rounded-full text-stone-700 border-stone-300 focus:outline-none focus:ring-2 focus:ring-amber-800 focus:border-transparent"
                        >
                    </div>
                </div>
            </div>
             <h1 class="text-2xl text-center sm:text-3xl font-bold font-lora text-stone-700 sm:hidden pb-4">Arquivo Histórico</h1>
        </div>
    </header>

    <!-- Conteúdo Principal - Grid de Documentos -->
    <main class="container mx-auto px-4 sm:px-6 lg:px-8 py-12 flex-grow">
        <h2 class="text-2xl font-lora font-bold mb-8 text-stone-700">Documentos em Destaque</h2>

        <div class="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 lg:grid-cols-4 xl:grid-cols-5 gap-8">
            

            @foreach ($posts as $post)
                  <div class="bg-white rounded-lg shadow-lg overflow-hidden transform hover:-translate-y-1 transition-transform duration-300 flex flex-col">
                <div class="w-full h-60 flex items-center justify-center p-4 bg-[#a1887f]">
                    <h4 class="font-lora text-center text-white" style="font-size: 1.3rem">{{$post->title}}</h4>
                </div>
                <div class="p-4 flex flex-col flex-grow">
                    <p class="text-sm  text-lg mb-2 text-stone-800 truncate">{{$post->post_legend}}</p>
                     <div class="mt-auto pt-4">
                        <a href={{route('show', $post->id)}} class="block w-full text-center bg-transparent border border-stone-600 text-stone-600 px-4 py-2 rounded-md text-sm font-medium hover:bg-stone-600 hover:text-white transition-colors">Visualizar</a>
                    </div>
                </div>
            </div>
            @endforeach
        </div>
    </main>

    <!-- Rodapé -->
    <footer class="bg-stone-800 text-white">
        <div class="container mx-auto px-4 sm:px-6 lg:px-8 py-6 text-center">
            <p>&copy; 2024 Prefeitura Municipal de Uruguaiana. Todos os direitos reservados.</p>
            <p class="text-sm text-stone-400 mt-1">Desenvolvido pelo Setor de Tecnologia da Informação.</p>
        </div>
    </footer>

</body>
</html>
