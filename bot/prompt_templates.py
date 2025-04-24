from langchain_core.prompts import ChatPromptTemplate

def get_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system", """你是一个聊天机器人"""),
        ("human", "{input}")
    ])
