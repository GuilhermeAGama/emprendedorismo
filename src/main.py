from retriever import Retriever
from evaluator import Evaluator


questao = {
    "id": 1,
    "modelo":
    """
    Herança permite que uma classe reutilize
    atributos e métodos de outra classe.
    """
}


resposta_aluno = """
Uma classe filha recebe atributos da classe pai.
"""


retriever = Retriever()
evaluator = Evaluator()


exemplos = retriever.search(
    questao["id"],
    resposta_aluno
)


avaliacao = evaluator.evaluate(
    questao["modelo"],
    resposta_aluno,
    exemplos
)


print(avaliacao)