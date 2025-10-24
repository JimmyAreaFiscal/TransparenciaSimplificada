# app.py (renomeie frontend.py para app.py)
import gradio as gr
import sys
import os

# Adicione o diretório src ao path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from agents import agent
from langchain_core.messages import HumanMessage

def chat(message, history):
    """Processa a mensagem do usuário e retorna a resposta do agente."""
    try:
        result = agent.invoke(
            {"messages": [HumanMessage(content=message)]},
            {"configurable": {"thread_id": "1"}},
        )
        response = result['messages'][-1].content
        return response
    except Exception as e:
        return f"Erro ao processar a mensagem: {str(e)}"

# Interface Gradio
with gr.Blocks(title="Chatbot - Balanço Geral do Estado do RS") as demo:
    gr.Markdown(
        """
        # Chatbot - Balanço Geral do Estado do Rio Grande do Sul
        
        Faça perguntas sobre o Balanço Geral do Estado do Rio Grande do Sul (exercício 2024).
        """
    )
    
    chatbot = gr.Chatbot(
        label="Conversa",
        height=500,
        show_copy_button=True
    )
    
    msg = gr.Textbox(
        label="Digite sua pergunta",
        placeholder="Ex: O que é o Balanço Geral?",
        lines=2
    )
    
    submit_btn = gr.Button("Enviar", variant="primary")
    clear = gr.Button("Limpar")
    
    def respond(message, chat_history):
        bot_message = chat(message, chat_history)
        chat_history.append((message, bot_message))
        return "", chat_history
    
    msg.submit(respond, [msg, chatbot], [msg, chatbot])
    submit_btn.click(respond, [msg, chatbot], [msg, chatbot])
    clear.click(lambda: None, None, chatbot, queue=False)

if __name__ == "__main__":
    demo.launch()