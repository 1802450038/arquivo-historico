import subprocess
import os

def comprimir_pdf(arquivo_entrada, arquivo_saida, nivel_qualidade=2):
    """
    Comprime um arquivo PDF usando o Ghostscript.

    :param arquivo_entrada: Caminho para o PDF original.
    :param arquivo_saida: Caminho para salvar o PDF comprimido.
    :param nivel_qualidade: Um número de 0 a 4 representando o nível de compressão.
                            0: screen (mais baixo, menor tamanho)
                            1: ebook (bom equilíbrio)
                            2: printer (alta qualidade)
                            3: prepress (qualidade de gráfica)
                            4: default (qualidade original)
    """
    if not os.path.exists(arquivo_entrada):
        print(f"Erro: O arquivo de entrada '{arquivo_entrada}' não foi encontrado.")
        return

    qualidades = {
        0: '/screen',
        1: '/ebook',
        2: '/printer',
        3: '/prepress',
        4: '/default'
    }

    # Comando base do Ghostscript
    comando = [
        'gs',
        '-sDEVICE=pdfwrite',
        '-dCompatibilityLevel=1.4',
        f'-dPDFSETTINGS={qualidades.get(nivel_qualidade, "/default")}',
        '-dNOPAUSE',
        '-dQUIET',
        '-dBATCH',
        f'-sOutputFile={arquivo_saida}',
        arquivo_entrada
    ]

    try:
        print(f"Comprimindo '{arquivo_entrada}' para '{arquivo_saida}'...")
        subprocess.run(comando, check=True)
        
        # Calcula a redução de tamanho
        tamanho_original = os.path.getsize(arquivo_entrada) / (1024 * 1024) # em MB
        tamanho_comprimido = os.path.getsize(arquivo_saida) / (1024 * 1024) # em MB
        reducao = (1 - tamanho_comprimido / tamanho_original) * 100

        print("\nCompressão concluída com sucesso!")
        print(f"Tamanho original: {tamanho_original:.2f} MB")
        print(f"Tamanho comprimido: {tamanho_comprimido:.2f} MB")
        print(f"Redução de: {reducao:.2f}%")

    except FileNotFoundError:
        print("Erro: Ghostscript não encontrado. Verifique se ele está instalado e no PATH do sistema.")
    except subprocess.CalledProcessError as e:
        print(f"Ocorreu um erro durante a execução do Ghostscript: {e}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")

# nome_do_pdf = "./PDFS/Termos de Juramento dos Empregados Municipais no Conselho Municipal e Intendentes do Município 1885 a 1928.pdf"


# pdf_comprimido = nome_do_pdf.split('/')[-1].split('.pdf')[0] + "_comprimido.pdf"
# 3. Escolha o nível de qualidade (leia a explicação abaixo)
#    0: Qualidade de tela (menor arquivo, ideal para web/email)
#    1: Qualidade de eBook (ótimo equilíbrio entre tamanho e qualidade)
#    2: Qualidade de Impressão (para imprimir em casa/escritório)
#    3: Qualidade de Pré-impressão (para gráficas profissionais)
#    Recomendação: comece com 1 (ebook) e veja o resultado.
# qualidade = 1


# comprimir_pdf(nome_do_pdf, pdf_comprimido, qualidade)