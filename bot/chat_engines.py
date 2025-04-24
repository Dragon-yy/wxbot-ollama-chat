import os
import requests
from langchain_ollama import OllamaLLM
from langchain_openai import ChatOpenAI
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.runnables import RunnableLambda
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain.llms.base import LLM
from langchain_community.llms.utils import enforce_stop_tokens
from bot.prompt_templates import get_prompt_template


# ✅ 自定义 LLM：SiliconFlow
class SiliconFlow(LLM):
    def __init__(self):
        super().__init__()

    @property
    def _llm_type(self) -> str:
        return "siliconflow"

    def siliconflow_completions(self, model: str, prompt: str) -> str:
        API_KEY = os.getenv("CUSTOM_API_KEY", "<Your Key>")
        print(API_KEY)
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "authorization": f"Bearer {API_KEY}"
        }

        response = requests.post("https://api.siliconflow.cn/v1/chat/completions", json=payload, headers=headers)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]

    # 这里的model是silconflow上对接的模型可以自己设置
    def _call(self, prompt: str, stop: list = None, model: str = "deepseek-ai/DeepSeek-R1-Distill-Qwen-32B") -> str:
        response = self.siliconflow_completions(model=model, prompt=prompt)
        if stop is not None:
            response = enforce_stop_tokens(response, stop)
        return response


# ✅ 模型选择器
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
    elif model_name == "siliconflow":
        return SiliconFlow()
    else:
        raise ValueError(f"❌ 不支持的模型名称：{model_name}")


# ✅ 构建对话链（支持上下文）
def build_chain(model_name="ollama"):
    llm = get_llm(model_name)
    prompt = get_prompt_template()

    def chain_fn(inputs):
        return {"output": llm.invoke(prompt.invoke(inputs))}

    base_chain = RunnableLambda(chain_fn)

    def get_memory(session_id: str):
        return ChatMessageHistory()

    return RunnableWithMessageHistory(
        base_chain,
        get_memory,
        input_messages_key="input",
        history_messages_key="history"
    )
