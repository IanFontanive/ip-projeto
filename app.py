from flask import Flask, render_template, request
from google import genai
from dotenv import load_dotenv
import os

load_dotenv(override=True)


app = Flask(__name__)

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

client = None
if GEMINI_API_KEY:
    try:
        client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception as e:
        print(f"ERRO DE CONFIGURAÇÃO: Falha ao inicializar o cliente Gemini: {e}")
else:
    print("ALERTA: Variável GEMINI_API_KEY não configurada.")

modelo = "gemini-2.5-flash"

perguntas_pets = [
    "Como cuidar de um cachorro filhote?",
    "Qual a melhor ração para gatos adultos?",
    "Como ensinar comandos básicos ao meu cachorro?",
    "Como adaptar um pet à casa nova?",
    "Como identificar sinais de doença em cães e gatos?",
]

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/gemini", methods=["GET", "POST"])
def gemini():
    resposta = None
    pergunta_usuario = "" 

    if request.method == "POST":
        pergunta = request.form.get("pergunta")
    
    elif request.method == "GET":
        pergunta = request.args.get("pergunta_rapida")

    if pergunta:
        pergunta_usuario = pergunta
        
        if client:
            try:
                system_prompt = "Você é um especialista em cuidados com animais de estimação. Responda a todas as perguntas de forma concisa, útil e amigável. Use listas e negrito para melhorar a leitura. Responda em Português. Forneça respostas de no mínimo 30 palavras e no máximo 120."
                
                resultado = client.models.generate_content(
                    model=modelo,
                    contents=pergunta_usuario,
                    config=genai.types.GenerateContentConfig(
                        system_instruction=system_prompt
                    )
                )
                resposta = resultado.text
                
            except Exception as e:
                resposta = f"Erro ao consultar a IA: {str(e)}. Verifique se sua chave está correta."
        else:
            resposta = "A API Gemini não está configurada. Por favor, configure sua chave no arquivo .env."

    return render_template(
        'gemini.html', 
        resposta=resposta, 
        pergunta=pergunta_usuario, 
        perguntas_pets=perguntas_pets
    )


if __name__ == '__main__':
    app.run()