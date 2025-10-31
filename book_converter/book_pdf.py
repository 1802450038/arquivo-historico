import subprocess
import os
import re
from PIL import Image
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas



def selecionar_pasta():
    """
    Abre uma janela de diálogo para selecionar uma pasta e retorna o caminho selecionado.
    """
    try:
        from tkinter import Tk
        from tkinter.filedialog import askdirectory

        root = Tk()
        root.withdraw()  # Oculta a janela principal
        pasta_selecionada = askdirectory(title="Selecione a pasta contendo as imagens")
        root.destroy()  # Fecha a janela do Tkinter
        return pasta_selecionada
    except ImportError:
        print("Tkinter não está disponível. Certifique-se de que está instalado.")
        return None
    
def informar_nome_arquivo():
    """
    Solicita ao usuário o nome do arquivo PDF de saída.
    """
    nome_arquivo = input("Digite o nome do arquivo PDF de saída (ex: resultado.pdf): ")
    if not nome_arquivo.lower().endswith('.pdf'):
        nome_arquivo += '.pdf'
    return nome_arquivo

def remover_arquivo_se_existir(caminho_arquivo):
    """
    Remove o arquivo especificado se ele já existir.
    """
    if os.path.exists(caminho_arquivo):
        os.remove(caminho_arquivo)
        print(f"Arquivo '{caminho_arquivo}' removido com sucesso.")
    else:
        print(f"Arquivo '{caminho_arquivo}' não encontrado.")
