from repositories.QuestionRepository import QuestionRepository
from repositories.CorrectionRepository import CorrectionRepository

from services.QuestionService import QuestionService
from services.CorrectionService import CorrectionService

from retriever import Retriever
from evaluator import Evaluator

question_repository = QuestionRepository()
correction_repository = CorrectionRepository()

retriever = Retriever()
evaluator = Evaluator()

question_service = QuestionService(question_repository)

correction_service = CorrectionService(
    question_repository,
    correction_repository,
    retriever,
    evaluator
)