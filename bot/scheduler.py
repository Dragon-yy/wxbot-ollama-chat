import schedule
import time
from datetime import datetime

def push_daily(wx, who="文件传输助手"):
    msg = f"📅 今日信息推送：{datetime.now().strftime('%Y-%m-%d')}\n☀️ 记得喝水、站起来走走哦！"
    wx.ChatWith(who)
    wx.SendMsg(msg)

def start_daily_schedule(wx, who="文件传输助手", push_time="08:30"):
    """
    启动每日定时推送
    :param wx: WeChat 实例
    :param who: 推送对象
    :param push_time: 推送时间，格式 HH:MM
    """
    try:
        time.strptime(push_time, "%H:%M")  # 简单时间格式校验
    except ValueError:
        raise ValueError("时间格式不正确，请使用 HH:MM（如 08:30）")

    schedule.every().day.at(push_time).do(push_daily, wx=wx, who=who)
    print(f"✅ 已设置每天 {push_time} 向「{who}」发送定时信息")

    while True:
        schedule.run_pending()
        time.sleep(10)
