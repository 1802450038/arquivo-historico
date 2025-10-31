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

