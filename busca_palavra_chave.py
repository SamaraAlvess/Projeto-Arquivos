import fitz 
import re 
import os 
import json 

palavras_chave = [
    "criação do comitê", "criação do grupo de trabalho", "criação da comissão", "criação do núcleo técnico",
    
    "instituição do comitê", "instituição do grupo de trabalho", "instituição da comissão", "instituição do núcleo técnico",
    "instituição de comitê", "instituição de grupo de trabalho", "instituição de comissão", "instituição de núcleo técnico",
    "instituição dos comitês", "instituição dos grupos de trabalho", "instituição das comissões", "instituição dos núcleos técnicos",

    "composição do comitê", "composição do grupo de trabalho", "composição da comissão", "composição do núcleo técnico",
    "aprovação do comitê", "aprovação do grupo de trabalho", "aprovação da comissão", "aprovação do núcleo técnico",
    "instauração do comitê", "instauração do grupo de trabalho", "instauração da comissão", "instauração do núcleo técnico",
    "instalação do comitê", "instalação do grupo de trabalho", "instalação da comissão", "instalação do núcleo técnico",
    "implantação do comitê", "implantação do grupo de trabalho", "implantação da comissão", "implantação do núcleo técnico",
    "instituiu o comitê", "instituiu o grupo de trabalho", "instituiu a comissão", "instituiu o núcleo técnico",

    "conclusão do comitê", "conclusão do grupo de trabalho", "conclusão da comissão", "conclusão do núcleo técnico",
    "encerramento do comitê", "encerramento do grupo de trabalho", "encerramento da comissão", "encerramento do núcleo técnico",


]

pastas_pdfs = "./boletins/2025"

resultados = []

def cortar_frases(texto, max_frases=10):
    frases = re.split(r'(?<=[.!?])\s+', texto)
    return ' '.join(frases[:max_frases])

def extrair_trechos(texto, palavras):
    encontrados = []
    for palavra in palavras:

        padrao = re.compile(rf".{{0,4000}}{re.escape(palavra)}.{{0,6000}}", re.IGNORECASE)
        matches = padrao.findall(texto) 

        for trecho in matches:
            trecho_completo = trecho.strip()
            trecho_final = cortar_frases(trecho_completo, max_frases=10)

            encontrados.append({
                "palavra_chave": palavra,
                "trecho": trecho_final
            })
        
    return encontrados 

for nome_arquivo in os.listdir(pastas_pdfs):

    if nome_arquivo.endswith(".pdf"):
        caminho_pdf = os.path.join(pastas_pdfs, nome_arquivo)
        doc = fitz.open(caminho_pdf)
        texto = ""

        
        for pagina in doc:
            texto += pagina.get_text()
        trechos = extrair_trechos(texto, palavras_chave)

        if trechos:
            for item in trechos:
                resultados.append({
                    "arquivo": nome_arquivo,
                    "palavra_chave": item["palavra_chave"],
                    "trecho": item["trecho"]
                })
        else: 
            resultados.append({
                "arquivo": nome_arquivo,
                "palavra_chave": "Nenhuma encontrada",
                "trecho": "Nenhum trecho com as palavras-chaves foi encontrado nesse arquivo"
            })
        
        doc.close()

with open ("boletins_2025.json", "w", encoding="utf-8") as f:
    json.dump(resultados, f, indent=2, ensure_ascii=False)

for item in resultados:
    print(f"\nArquivo: {item['arquivo']}")
    print(f"Palavra chave: {item['palavra_chave']}")
    print(f"Trecho: {item['trecho']}\n")
    print('----'*50)

   
