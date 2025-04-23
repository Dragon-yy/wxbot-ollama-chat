import click
from bot.wechat_listener import start_listening
from bot.scheduler import start_daily_schedule
from dotenv import load_dotenv

load_dotenv()  # 自动读取项目根目录下的 .env 文件


@click.group()
def cli():
    pass

@cli.command()
@click.option('--model', default='ollama', type=click.Choice(['ollama', 'chatgpt', 'deepseek',  'siliconflow']), help='选择使用的 AI 模型')
@click.option('--listen-list', default="", help='逗号分隔的监听对象，例如：妈,老婆,好友群')
def listen(model, listen_list):
    """启动微信监听机器人"""
    # 解析监听对象列表
    listen_targets = [item.strip() for item in listen_list.split(',')] if listen_list else None
    start_listening(model=model, listen_list=listen_targets)

@cli.command()
@click.option('--target', default='文件传输助手', help='每天定时推送的联系人')
@click.option('--time', 'push_time', default='08:30', help='发送时间（格式如 08:30）')
def schedule(target, push_time):
    """开启每日信息推送功能"""
    from wxauto import WeChat
    wx = WeChat()
    start_daily_schedule(wx, who=target, push_time=push_time)


if __name__ == '__main__':
    cli()
