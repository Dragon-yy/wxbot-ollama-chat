from wxauto import WeChat
import time
from chat_memory import get_conversation_chain
import re
from langchain_core.messages import HumanMessage



# 初始化微信
wx = WeChat()
listen_list = ['xxx']
for i in listen_list:
    wx.AddListenChat(who=i)

# 联系人 → 对话链映射（含上下文）
conversation_chains = {}

wait = 1  # 每1秒监听一次
while True:
    msgs = wx.GetListenMessage()
    for chat in msgs:
        who = chat.who
        one_msgs = msgs.get(chat)
        for msg in one_msgs:

            sender = msg.sender
            if sender == "Self":
                continue  # 忽略自己发的

            content = msg.content
            print(f"【{sender}】：{content}")

            # 获取/初始化当前联系人的对话链
            if who not in conversation_chains:
                conversation_chains[who] = get_conversation_chain()

            chain = conversation_chains[who]

            try:
                # 如果开头有@bot关键词再予以ai响应
                if content.startswith("@bot"):
                    response = chain.invoke({"input": content.lstrip("@bot")},config={"configurable": {"session_id": sender}})
                    # 去除deepseek think的内容
                    print(response)
                    response = re.sub(r'<think>.*?</think>', '', response, flags=re.DOTALL).strip()
                    chat.SendMsg(response+" [powered by dragon-yy]")
                else:
                    continue
            except Exception as e:
                print(f"处理出错: {e}")
                chat.SendMsg("我好像有点糊涂了……稍后再试试吧~ [powered by dragon-yy]")

    time.sleep(wait)
