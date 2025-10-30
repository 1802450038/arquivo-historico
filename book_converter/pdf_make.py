import os
import re
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

def extrair_numero(nome_arquivo):
    """
    Extrai o número do nome de um arquivo usando expressões regulares.
    Retorna o número como um inteiro se encontrado, caso contrário, retorna um valor muito alto
    para garantir que arquivos sem número fiquem por último.
    """
    # Procura por um ou mais dígitos no nome do arquivo
    numeros = re.findall(r'\d+', nome_arquivo)
    if numeros:
        # Retorna o primeiro grupo de números encontrado como um inteiro
        return int(numeros[0])
    # Se nenhum número for encontrado, retorna um número grande para despriorizar
    return float('inf')

def criar_pdf_de_imagens(pasta_imagens, nome_arquivo_saida):
    """
    Cria um arquivo PDF a partir de imagens em uma pasta, ordenadas numericamente.

    :param pasta_imagens: O caminho para a pasta contendo as imagens.
    :param nome_arquivo_saida: O nome do arquivo PDF a ser gerado (ex: 'resultado.pdf').
    """
    # Lista de extensões de imagem válidas
    extensoes_validas = ['.jpg', '.jpeg', '.png']

    # Pega todos os arquivos na pasta que possuem uma extensão válida
    try:
        arquivos_imagem = [f for f in os.listdir(pasta_imagens) if os.path.splitext(f)[1].lower() in extensoes_validas]
    except FileNotFoundError:
        print(f"Erro: A pasta '{pasta_imagens}' não foi encontrada.")
        return

    if not arquivos_imagem:
        print(f"Nenhuma imagem encontrada na pasta '{pasta_imagens}'.")
        return

    # Ordena a lista de arquivos de imagem com base no número extraído do nome
    arquivos_imagem.sort(key=extrair_numero)

    # Configura o canvas do PDF com o tamanho de uma folha A4
    c = canvas.Canvas(nome_arquivo_saida, pagesize=letter)
    largura_pdf, altura_pdf = letter

    print("Iniciando a criação do PDF...")
    print(nome_arquivo_saida)
    for i, nome_imagem in enumerate(arquivos_imagem):
        caminho_completo = os.path.join(pasta_imagens, nome_imagem)
        try:
            with Image.open(caminho_completo) as img:
                # Obtém as dimensões da imagem
                largura_img, altura_img = img.size
                
                # Calcula a proporção para ajustar a imagem à página
                aspect_ratio = altura_img / float(largura_img)
                largura_desenho = largura_pdf
                altura_desenho = largura_desenho * aspect_ratio

                # Se a altura da imagem for maior que a página, ajusta pela altura
                if altura_desenho > altura_pdf:
                    altura_desenho = altura_pdf
                    largura_desenho = altura_desenho / aspect_ratio

                # Centraliza a imagem na página
                x = (largura_pdf - largura_desenho) / 2
                y = (altura_pdf - altura_desenho) / 2

                # Adiciona a imagem ao PDF
                c.drawImage(caminho_completo, x, y, width=largura_desenho, height=altura_desenho)
                
                # Adiciona uma nova página para a próxima imagem
                if i < len(arquivos_imagem) - 1:
                    c.showPage()
                
                print(f"Adicionada a página {i+1}: {nome_imagem}")

        except Exception as e:
            print(f"Não foi possível processar a imagem {nome_imagem}: {e}")

    # Salva o arquivo PDF
    c.save()
    print(f"\nPDF '{nome_arquivo_saida}' criado com sucesso com {len(arquivos_imagem)} páginas!")

# --- COMO USAR O SCRIPT ---

# 1. Coloque o caminho para a sua pasta de imagens aqui
#    Exemplo no Windows: "C:\\Users\\SeuUsuario\\Desktop\\MinhasImagens"
#    Exemplo no Linux/Mac: "/home/seu_usuario/imagens"
pasta_com_imagens = "/Users/gabrielbellagamba/Desktop/arquivo_filament/conversor_pdf_python/arquivo_files_historico/Termos de juramento"

# 2. Defina o nome que você quer para o arquivo PDF de saída
# nome_do_pdf = "Ata das Sessões da Câmara Municipal da Vila de Uruguaiana 1867 a 1871.pdf"
# nome_do_pdf = "Atas de Exames nas Escolas Municipais 1893.pdf"
# nome_do_pdf = "Atas de Exames nas Escolas Municipais 1895.pdf"
# nome_do_pdf = "Carta de Sesmaria 1823.pdf"
# nome_do_pdf = "Contrato de Professores da Instrução Pública de 1883 a 1889.pdf"
# nome_do_pdf = "Correspondências da Intendência de Uruguaiana e Junta Revolucionária 1890 a 1891.pdf"
# nome_do_pdf = "Inventário dos Objetos de Utensílios das Aulas Públicas (sexo feminino) 1876 a 1880.pdf"
# nome_do_pdf = "Juramento dos Empregados Públicos da Câmara Municipal Vila de Uruguaiana 1847 até 1885.pdf"
# nome_do_pdf = "Juramento dos Empregados Públicos Câmara Municipal - Vila de Uruguaiana 1847 a 1885.pdf"
# nome_do_pdf = "Lançamento dos Balanços e Orçamentos da Câmara Municipal a Assembleia Provincial 1853 a 1859.pdf"
# nome_do_pdf = "Folha de Pagamento dos Funcionários Municipais 1920 a 1921.pdf"
# nome_do_pdf = "Registros de Títulos e Nomeações dos Empregados Públicos de Uruguaiana 1847 a 1889.pdf"
# nome_do_pdf = "Registro dos Terrenos concedidos pela Câmara Municipal e outras autoridades 1861.pdf"
# nome_do_pdf = "Registros de Inventários 1893 a 1921.pdf"
# nome_do_pdf = "Termo de Responsabilidade e Fiança para estabelecer Casas de Jogos e Hotéis em Uruguaiana.pdf"
# nome_do_pdf = "Termos de Visita à Cadeia Pública pelo Delegado de Polícia de Uruguaiana.pdf"
# nome_do_pdf = "Termos de Arrematação, Fiança e Outros Contratos da Câmara Municipal de Uruguaiana 1855 a 1886.pdf"
# nome_do_pdf = "Termos de Audiências da Delegacia da Villa de Uruguaiana 1858 a 1877.pdf"
# nome_do_pdf = "Termos de Balanços de Verificação no Cofre da Câmara Municipal 1858 a 1870.pdf"
nome_do_pdf = "Termos de Juramento dos Empregados Municipais no Conselho Municipal e Intendentes do Município 1885 a 1928.pdf"

# 3. Executa a função
criar_pdf_de_imagens(pasta_com_imagens, nome_do_pdf)