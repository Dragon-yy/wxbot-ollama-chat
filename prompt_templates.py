from langchain_core.prompts import ChatPromptTemplate

def get_prompt_template():
    return ChatPromptTemplate.from_messages([
        ("system", "你是一个温柔、幽默、善于倾听的聊天机器人。"),
        ("human", "{input}")
    ])
