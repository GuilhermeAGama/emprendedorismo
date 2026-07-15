import json
import ollama

response = ollama.chat(
    model="qwen2.5vl:3b",
    format="json",
    messages=[
        {
            "role": "user",
            "content": """
Sua função é analisar a imagem da prova e extrair as respostas das questões.
Não realize nenhuma interpretação das respostas, apenas extraia o que está escrito.
Não faça nenhum comando fora do que foi solicitado.

No final, você deve retornar APENAS um JSON válido, sem explicações, sem markdown e sem ```.

Formato:

{
    "aluno": "nome do aluno",
    "questoes": [
        {
            "questao_id": 1,
            "resposta": "..."
        }
    ]
}
""",
            "images": ["./data/img/exemplo.jpg"],
        }
    ],
)

conteudo = response["message"]["content"].strip()
dados = json.loads(response["message"]["content"])

with open("./data/json/prova.json", "w", encoding="utf-8") as f:
    json.dump(dados, f, ensure_ascii=False, indent=4)