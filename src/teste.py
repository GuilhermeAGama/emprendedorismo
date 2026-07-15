from pprint import pprint

from repositories.QuestionRepository import QuestionRepository
from repositories.CorrectionRepository import CorrectionRepository

from services.QuestionService import QuestionService
from services.CorrectionService import CorrectionService

from retriever import Retriever
from evaluator import Evaluator


# Repositories
question_repository = QuestionRepository()
correction_repository = CorrectionRepository()

# Componentes
retriever = Retriever()
evaluator = Evaluator(model="qwen3:8b")

# Services
question_service = QuestionService(question_repository)

correction_service = CorrectionService(
    question_repository=question_repository,
    correction_repository=correction_repository,
    retriever=retriever,
    evaluator=evaluator
)

print("\nQUESTÕES CADASTRADAS\n")

for q in question_service.list_questions():
    print(f'{q["questao_id"]} - {q["enunciado"]}')

questao_id = int(input("\nQuestão: "))
resposta = input("\nResposta do aluno:\n")

print("\n========================")
print("BUSCANDO EXEMPLOS")
print("========================")

exemplos = retriever.search(
    questao_id,
    resposta
)

pprint(exemplos)

print("\n========================")
print("AVALIANDO")
print("========================")

questao = question_service.get_question(
    questao_id
)

resultado = evaluator.evaluate(
    questao["resposta_modelo"],
    resposta,
    exemplos
)

pprint(resultado)

print("\nAceitar nota? (s/n)")
op = input("> ")

if op.lower() == "n":

    nota = float(input("Nota do professor: "))
    feedback = input("Feedback: ")

    correction_service.save_manual_correction(
        questao_id,
        resposta,
        nota,
        feedback
    )

else:

    correction_service.save_automatic_correction(
        questao_id,
        resposta,
        resultado
    )

print("\n========================")
print("BUSCA APÓS SALVAR")
print("========================")

exemplos = exemplos = [
    e
    for e in exemplos
    if e["similaridade"] >= 0.75
]

pprint(exemplos)