import os
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_message_histories import ChatMessageHistory
from prompt_templates import get_prompt_template


def get_llm(model_name="ollama"):
    if model_name == "ollama":
        return OllamaLLM(model="deepseek-r1:8b")
    elif model_name == "chatgpt":
        return ChatOpenAI(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            model="gpt-3.5-turbo",
            temperature=0.7
        )
    elif model_name == "deepseek":
        return ChatOpenAI(
            openai_api_key=os.getenv("DEEPSEEK_API_KEY"),
            base_url="https://api.deepseek.com/v1",
            model="deepseek-chat",
            temperature=0.7
        )
    else:
        raise ValueError("❌ 不支持的模型名称")


def build_chain(model_name="ollama"):
    llm = get_llm(model_name)
    prompt = get_prompt_template()

    # 包装为 PromptChain（你也可以自定义更复杂的 chain）
    def chain_fn(inputs):
        response = llm.invoke(prompt.format(**inputs))
        return {"output": response}

    base_chain = RunnableLambda(chain_fn)

    # session_id 映射到记忆（你也可以换成 RedisChatMessageHistory）
    def get_memory(session_id: str):
        return ChatMessageHistory()

    # 构建上下文对话链
    return RunnableWithMessageHistory(
        base_chain,
        get_memory,
        input_messages_key="input",
        history_messages_key="history"
    )
