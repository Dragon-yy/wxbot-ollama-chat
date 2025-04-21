import time
import re
from datetime import datetime
import os
from wxauto import WeChat
from bot.chat_engines import build_chain


# 联系人 → 对话链映射
conversation_chains = {}

def save_log(who, sender, user_input, reply):
    today = datetime.now().strftime("%Y-%m-%d")
    folder = "logs"
    os.makedirs(folder, exist_ok=True)
    filename = f"{folder}/{who}_{today}.txt"
    with open(filename, "a", encoding="utf-8") as f:
        f.write(f"[{sender}]：{user_input}\n")
        f.write(f"[bot]：{reply}\n\n")


def clean_response(text: str) -> str:
    # 清理 Deepseek 风格的思考信息
    return re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()

def start_listening(model="ollama", listen_list=None):
    """
    启动微信监听主逻辑
    :param model: 使用的 AI 模型（ollama/chatgpt/deepseek）
    :param listen_list: 可选的监听人名单（默认监听所有聊天窗口）
    """
    wx = WeChat()
    print("✅ 已连接微信")

    # 设置监听对象（联系人或群）
    if listen_list:
        for i in listen_list:
            wx.AddListenChat(who=i)
    else:
        print("⚠️ 未指定监听对象，将默认监听全部已打开的聊天窗口")

    wait = 1  # 每秒检查一次
    while True:
        msgs = wx.GetListenMessage()
        for chat in msgs:
            who = chat.who
            one_msgs = msgs.get(chat)
            for msg in one_msgs:
                sender = msg.sender
                # if sender == "Self":
                #     continue  # 跳过自己发的

                content = msg.content
                print(f"💬 收到 [{who} - {sender}]：{content}")

                # 判断是否触发AI（@bot）
                if not content.strip().startswith("@bot"):
                    continue

                # 初始化对话链
                if who not in conversation_chains:
                    print(f"🧠 初始化 [{who}] 的对话链，模型：{model}")
                    conversation_chains[who] = build_chain(model)

                # 去除 @bot 指令后进行处理
                user_input = content.lstrip("@bot").strip()
                try:
                    response = conversation_chains[who].invoke({
                        "input": user_input
                    }, config={"configurable": {"session_id": sender}})
                    response = response['output']
                    final_reply = clean_response(response)
                    chat.SendMsg(final_reply + "\n\n✨ Powered by Dragon-YY ✨")
                    save_log(who, sender, user_input, response)

                except Exception as e:
                    print(f"❌ AI 处理出错：{e}")
                    chat.SendMsg("AI 暂时迷路了，等等再问我吧~ \n\n✨ Powered by Dragon-YY ✨")

        time.sleep(wait)
