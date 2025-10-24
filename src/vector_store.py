# Importação do modelo de embeddings
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from langchain_chroma import Chroma

load_dotenv()

embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

vector_store = Chroma(
    collection_name="balanco_geral",
    embedding_function=embeddings,
    persist_directory="src/vectorStore", 
)

retriever = vector_store.as_retriever(
    search_type="mmr", search_kwargs={"k": 1, "fetch_k": 5}
)



if __name__ == "__main__":
    print('\n-----------------------------------\n')
    print('Testando a vector store...')
    print('\n-----------------------------------\n')
    results = retriever.invoke(
    "- V. Empresas Públicas e Sociedades de Economia Mista: contempla as demonstra -ções financeiras previstas na Lei Federal 6.404, de 15 de dezembro de 1976, tais como o balanço patrimonial, a demonstração dos lucros ou prejuízos acumulados, a demonstração do resultado do exercício, a demonstração dos fluxos de caixa, e,  se  companhia aberta, a demonstração do valor adicionado. São acompanhadas de notas explicativas, do relatório da administração, do parecer dos conselhos fiscal e de administração, e, conforme o caso, do relatório do comitê de auditoria e dos auditores independentes.",
    )
    for res in results:
        print(f"* {res.page_content} [{res.metadata}]")

