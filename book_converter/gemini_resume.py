import google.generativeai as genai
import os
from dotenv import load_dotenv
import time
import book_pdf
import pdf_make
import pdf_compress

def configurar_e_listar():
    """
    Configura a API e imprime uma lista de modelos disponíveis
    que podem gerar conteúdo.
    """
    try:
        # Carrega a chave de API do arquivo .env
        # load_dotenv()
        # api_key = os.getenv("GOOGLE_API_KEY")
        api_key = "AIzaSyCOEPtwL45MvzmV8oC71802450038gNmUixAczSzNttU"

        
        if not api_key:
            print("Erro: Chave de API não encontrada no arquivo .env.")
            print("Verifique se o arquivo .env está na mesma pasta.")
            return

        genai.configure(api_key=api_key)
        print("API configurada. Buscando lista de modelos...\n")
        
        # Itera e lista todos os modelos disponíveis
        modelos_encontrados = 0
        for m in genai.list_models():
            # Queremos modelos que suportem o método 'generateContent'
            # (que é o que usamos no script principal)
            if 'generateContent' in m.supported_generation_methods:
                print(f"--- Modelo Encontrado ---")
                print(f"Nome do Modelo: {m.name}")
                print(f"  - Descrição: {m.description}")
                print(f"  - Métodos suportados: {m.supported_generation_methods}\n")
                modelos_encontrados += 1
        
        if modelos_encontrados == 0:
            print("Nenhum modelo com 'generateContent' foi encontrado para esta API Key.")
            return

        print("-----------------------------------------------------------------")
        print("Busca concluída.")
        print("\nInstruções:")
        print("1. Procure na lista acima por um modelo multimodal (como 'gemini-1.5-pro' ou 'gemini-pro-vision').")
        print("2. Copie o 'Nome do Modelo' exato (ex: 'models/gemini-1.5-pro-latest').")
        print("3. Cole esse nome no seu script 'processar_pdf.py' na linha 'model = ...'.")
        print("-----------------------------------------------------------------")


    except Exception as e:
        print(f"Ocorreu um erro ao tentar listar os modelos: {e}")

def configurar_gemini():
    """
    Carrega a chave de API do arquivo .env e configura o cliente Gemini.
    """
    # Carrega as variáveis de ambiente do arquivo .env
    # load_dotenv()
    
    # api_key = os.getenv("GOOGLE_API_KEY")
    api_key = "AIzaSyCOEPtwL45MvzmV8oC71802450038gNmUixAczSzNttU"
    if not api_key:
        raise ValueError("Chave de API não encontrada. Verifique seu arquivo .env")
        
    genai.configure(api_key=api_key)
    print("API do Gemini configurada com sucesso.")

def processar_pdf(nome_arquivo_pdf):
    """
    Envia o PDF para o Gemini, pede a descrição e o resumo, 
    e retorna o texto gerado.
    """
    print(f"Iniciando o upload do arquivo: {nome_arquivo_pdf}...")
    
    # 1. Faz o upload do arquivo PDF.
    # Usamos o Gemini 1.5 Pro, que aceita arquivos diretamente.
    # O upload pode demorar alguns segundos dependendo do tamanho.
    try:
        pdf_file = genai.upload_file(path=nome_arquivo_pdf,
                                     display_name="Documento Escaneado")
        
        # Espera o processamento do arquivo (opcional, mas bom)
        while pdf_file.state.name == "PROCESSING":
            print("Processando o arquivo no servidor...")
            time.sleep(5)
            pdf_file = genai.get_file(pdf_file.name)

        if pdf_file.state.name == "FAILED":
            raise ValueError("Falha ao processar o arquivo no servidor.")

        print(f"Upload concluído! Nome do arquivo no servidor: {pdf_file.name}")

        # 2. Configura o modelo (Gemini 1.5 Pro)
        model = genai.GenerativeModel(model_name="models/gemini-pro-latest")

        # 3. Cria o prompt
        # Instruímos o modelo a "ler" o arquivo (pois é escaneado)
        # e a formatar a saída exatamente como queremos.
        prompt_instrucoes = f"""
        Analise o documento PDF que foi enviado (é um documento escaneado 
        escrito à mão). O nome do arquivo é {pdf_file.display_name}.
        
        Com base no conteúdo deste documento, por favor:
        
        1.  Gere uma descrição detalhada do conteúdo em exatamente 20 linhas.
        2.  Gere um resumo conciso do conteúdo em exatamente 5 linhas.
        
        Formate a sua resposta da seguinte maneira:

        DESCRIÇÃO:
        [Aqui vão as 20 linhas da descrição]

        ---
        
        RESUMO:
        [Aqui vão as 5 linhas do resumo]
        """

        # 4. Envia o prompt E o arquivo para o modelo
        print("Enviando o prompt para o Gemini...")
        response = model.generate_content([prompt_instrucoes, pdf_file])
        
        print("Resposta recebida!")
        return response.text

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        return None
    
    finally:
        # 5. (Importante) Deleta o arquivo do servidor após o uso
        if 'pdf_file' in locals() and pdf_file:
            print(f"Limpando o arquivo {pdf_file.name} do servidor...")
            genai.delete_file(pdf_file.name)
            print("Limpeza concluída.")


def salvar_texto(conteudo, nome_arquivo_saida):
    """
    Salva o conteúdo de texto em um arquivo .txt
    """
    try:
        with open(nome_arquivo_saida, "w", encoding="utf-8") as f:
            f.write(conteudo)
        print(f"Texto salvo com sucesso em: {nome_arquivo_saida}")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")

# --- Ponto de entrada principal do programa ---
if __name__ == "__main__":
    
        
    print("=== Conversor de Imagens para PDF ===")
    pasta_imagens = book_pdf.selecionar_pasta()
    nome_arquivo_pdf = book_pdf.informar_nome_arquivo()

    print(f"Pasta selecionada: {pasta_imagens}")
    print(f"Nome do arquivo PDF de saída: {nome_arquivo_pdf}")

    pdf_make.criar_pdf_de_imagens(pasta_imagens, nome_arquivo_pdf)
    pdf_compress.comprimir_pdf(nome_arquivo_pdf, f"comprimido_{nome_arquivo_pdf}", nivel_qualidade=1)
    book_pdf.remover_arquivo_se_existir(nome_arquivo_pdf)
    
    # --- CONFIGURAÇÃO ---
    NOME_DO_SEU_PDF = f"comprimido_{nome_arquivo_pdf}"  # <-- Coloque o nome do seu PDF aqui
    ARQUIVO_DE_SAIDA = f"resumo_{nome_arquivo_pdf}.txt"
    # --------------------
    # configurar_e_listar()
    try:
        configurar_gemini()
        
        # Verifica se o PDF existe antes de continuar
        if not os.path.exists(NOME_DO_SEU_PDF):
            print(f"Erro: O arquivo '{NOME_DO_SEU_PDF}' não foi encontrado.")
            print("Por favor, coloque o seu PDF na mesma pasta do script.")
        else:
            texto_gerado = processar_pdf(NOME_DO_SEU_PDF)
            
            if texto_gerado:
                salvar_texto(texto_gerado, ARQUIVO_DE_SAIDA)

    except ValueError as ve:
        print(f"Erro de configuração: {ve}")
    except Exception as e:
        print(f"Ocorreu um erro inesperado no programa: {e}")