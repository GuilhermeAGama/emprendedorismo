import ollama
import json


class Evaluator:

    def __init__(self, model="gemma3:4b"):
        self.model = model


    def evaluate(
        self,
        resposta_modelo,
        resposta_aluno,
        exemplos_humanos=None
    ):

        exemplos_texto = self._format_examples(
            exemplos_humanos
        )

        prompt = f"""
Você é um professor corrigindo uma questão discursiva.

Avalie a resposta do aluno considerando:

1. A resposta modelo.
2. Exemplos de respostas já corrigidas por professores.

Compare a resposta do aluno com a resposta modelo e com os exemplos anteriormente corrigidos.
Caso a resposta do aluno seja suficentemente semelhante a algum exemplo previamente corrigido, utilize a mesma nota e justificativa.
Não compare palavras.
Avalie conhecimento demonstrado.

Resposta modelo:
{resposta_modelo}

Respostas previamente corrigidas:
{exemplos_texto}

Nova resposta do aluno:
{resposta_aluno}

Critérios da nota:
10 - Resposta completa, todos os conceitos importantes presentes na resposta modelo.
8 - Correta, mas faltam detalhes secundários citados na resposta modelo.
6-7 - Conceito principal correto, mas incompleto.
4-5 - Parcialmente correta ou com erros.
1-3 - Pouco entendimento demonstrado.
0 - Completamente Incorreta.

Critérios de confiança:
- Alta confiança (100% - 90%): A resposta do aluno é muito semelhante a um exemplo previamente corrigido.
- Média confiança (89% - 60%): A resposta do aluno é parcialmente semelhante a um exemplo previamente corrigido.
- Baixa confiança (59% - 0%): A resposta do aluno é diferente de todos os exemplos previamente corrigidos.

Retorne somente JSON:

{{
    "nota": 0,
    "justificativa": "",
    "confianca": 0.0,
    "precisa_revisao": false
}}

"""

        response = ollama.chat(
            model=self.model,
            format="json",
            options={
                "temperature":0
            },
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )


        return json.loads(
            response["message"]["content"]
        )


    def _format_examples(self, exemplos):

        if not exemplos:
            return "Nenhum exemplo disponível."


        texto = ""

        for i, exemplo in enumerate(exemplos):

            texto += f"""
Exemplo {i+1}

Resposta:
{exemplo['resposta']}

Nota:
{exemplo['nota']}

Feedback:
{exemplo['feedback']}

"""

        return texto