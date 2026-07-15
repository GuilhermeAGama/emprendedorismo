import uuid
from embedding import generate_embedding
from database import collection


class Retriever:
    
    def add(
        self,
        questao_id,
        resposta,
        nota,
        feedback
    ):

        embedding = generate_embedding(resposta)

        collection.add(
            ids=[str(uuid.uuid4())],

            embeddings=[embedding],

            documents=[resposta],

            metadatas=[{
                "questao_id": questao_id,
                "nota": nota,
                "feedback": feedback
            }]
        )

    def search(
        self,
        questao_id,
        resposta_aluno,
        quantidade=3
    ):

        embedding = generate_embedding(
            resposta_aluno
        )


        resultado = collection.query(
            query_embeddings=[
                embedding
            ],

            n_results=quantidade,

            where={
                "questao_id": questao_id
            }
        )


        exemplos = []


        for i in range(
            len(resultado["documents"][0])
        ):

            exemplos.append({

                "resposta":
                resultado["documents"][0][i],

                "nota":
                resultado["metadatas"][0][i]["nota"],

                "feedback":
                resultado["metadatas"][0][i]["feedback"],

                "distancia":
                resultado["distances"][0][i],
                
                "similaridade":
                1 - resultado["distances"][0][i]
                
            })


        return exemplos