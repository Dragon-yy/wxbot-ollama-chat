# 🤖 微信聊天机器人 (WeChat AI Bot)

一个基于 `wxauto + LangChain + Ollama/ChatGPT/DeepSeek` 构建的微信 AI 助手，支持私聊自动回复、多轮对话上下文、模型切换、定时提醒推送等功能。

---

## ✨ 功能亮点

- 🧠 多轮对话 + 上下文记忆（按联系人隔离）
- 💬 私聊或群聊中发送 `@bot` 自动触发 AI 回复
- 🔄 多模型支持：Ollama（本地）、ChatGPT、DeepSeek
- 🕒 支持每日定时推送提醒（可设时间和联系人）
- 📁 聊天记录自动保存（按天分文件）
- 🖥️ 基于 Click 构建的命令行启动器

---

## 📦 项目结构

```
wechat-ai-bot/
├── main.py                 # CLI 启动入口
├── .env                    # 存放 API 密钥（建议忽略提交）
├── logs/                   # 聊天记录保存目录
├── bot/
│   ├── wechat_listener.py  # 监听微信消息并响应
│   ├── chat_engines.py     # AI 模型链封装
│   ├── scheduler.py        # 定时提醒逻辑
│   └── prompt_templates.py # 提示词模板（可选）
├── requirements.txt        # Python 依赖
└── README.md               # 项目说明
```

---

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 设置环境变量

创建 `.env` 文件：

```env
OPENAI_API_KEY=sk-xxxx
DEEPSEEK_API_KEY=sk-xxxx
```

### 3. 启动微信并登录

手动打开微信并登录账号，保持程序期间不要关闭。

---

## 🧠 使用方式

### 启动微信监听机器人：

监听单个联系人（默认使用 Ollama 本地模型）：

```bash
python main.py listen --listen-list 妈
```

监听多个联系人，指定模型：

```bash
python main.py listen --model chatgpt --listen-list 妈,老婆,好友群
```

> 支持模型：`ollama` | `chatgpt` | `deepseek`

---

### 设置每日定时推送

默认发送给 “文件传输助手”，时间为 08:30：

```bash
python main.py schedule
```

自定义推送对象和时间：

```bash
python main.py schedule --target 老婆 --time 21:00
```

---

## 💬 使用说明

### 如何触发 AI 回复？

你需要在对话中以 `@bot` 开头：

```
你：@bot 今天天气怎么样？
bot：杭州今天天气晴，气温 24～30℃，记得防晒哦~
```

---

## 📁 聊天记录存储

程序自动将每位联系人的聊天记录按天保存在 `logs/` 目录：

```
logs/
├── 老婆_2024-04-21.txt
├── 妈_2024-04-21.txt
```

---

## 🧠 支持模型说明

| 模型       | 来源       | 是否需联网 | 描述                      |
|------------|------------|------------|---------------------------|
| `ollama`   | 本地部署   | 否         | 需本地安装 [ollama](https://ollama.com) 并拉取模型（如 llama3） |
| `chatgpt`  | OpenAI     | 是         | 需配置 `OPENAI_API_KEY`   |
| `deepseek` | DeepSeek   | 是         | 中文表现优秀，需配置 `DEEPSEEK_API_KEY` |

---

## ⚙️ CLI 参数总览

| 命令 | 参数 | 示例 |
|------|------|------|
| `listen` | `--model` 指定模型<br> `--listen-list` 监听对象（逗号分隔） | `python main.py listen --model chatgpt --listen-list 妈,老婆` |
| `schedule` | `--target` 接收人<br>`--time` 时间（HH:MM） | `python main.py schedule --target 老婆 --time 08:30` |

---

## 🧱 依赖列表（部分）

- `wxauto`：微信窗口自动化
- `langchain` + `langchain-openai`：AI 对话管理
- `click`：构建 CLI 命令行
- `schedule`：任务调度器
- `python-dotenv`：读取 .env 配置

---

## 🛡️ 使用建议

- 仅供**个人学习用途**，避免频繁操作或群发行为，防止微信风控。
- Ollama 模型需本地安装 Ollama 并执行 `ollama run llama3` 等命令启动模型。
- 对话记录未加密存储，请注意隐私。

---

## 📌 后续计划（TODO）

- [ ] 加入关键词触发模型切换（如 @ollama / @gpt）
- [ ] 群聊中识别是否 @自己
- [ ] 对图片消息进行 OCR + 回复
- [ ] 支持多时段定时提醒（早安 + 晚安）

---

## 📬 联系我

Made with ❤️ by **dragon-yy**

欢迎提建议、star、fork 或开 issue 🚀
