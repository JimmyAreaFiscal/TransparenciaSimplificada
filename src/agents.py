from prompts import MAIN_SYSTEM_PROMPT

from langchain.agents.middleware import dynamic_prompt, ModelRequest
from vector_store import retriever 
from langchain.agents import create_agent
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langgraph.checkpoint.memory import InMemorySaver
from langchain_core.messages import HumanMessage  

load_dotenv()

model = ChatOpenAI(model="gpt-4o-mini")
saver = InMemorySaver()


@dynamic_prompt
def prompt_with_context(request: ModelRequest) -> str:
    """Inject context into state messages."""
    last_query = request.state["messages"][-1].text
    retrieved_docs = retriever.invoke(last_query)

    docs_content = "\n\n".join(doc.page_content for doc in retrieved_docs)

    system_message = MAIN_SYSTEM_PROMPT.format(context=docs_content, question=last_query)

    return system_message

agent = create_agent(model, tools=[], middleware=[prompt_with_context], checkpointer=saver)


if __name__ == "__main__":
    print('\n-----------------------------------\n')
    print('Testando o agente...')
    print('\n-----------------------------------\n')

    while True:
        query = input("Digite a pergunta: ")
        if query.lower() == "sair":
            break
        result = agent.invoke(
            {"messages": [HumanMessage(content=query)]},
            {"configurable": {"thread_id": "1"}},  
        )
        print(result['messages'][-1].content)

