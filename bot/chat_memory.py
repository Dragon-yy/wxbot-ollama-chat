from langchain_ollama import OllamaLLM
from langchain.memory import ConversationBufferMemory
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_community.chat_message_histories import ChatMessageHistory
from bot.prompt_templates import get_prompt_template


def get_conversation_chain():
    llm = OllamaLLM(model="deepseek-r1:14b")
    prompt = get_prompt_template()
    chain = prompt | llm

    # memory handler
    def get_memory(session_id: str):
        return ChatMessageHistory()

    return RunnableWithMessageHistory(
        chain,
        get_memory,
        input_messages_key="input",    # 必须和 prompt 输入变量一致
        history_messages_key="history" # 系统自动注入上下文
    )
