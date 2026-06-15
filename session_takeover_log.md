# Session Takeover Log — Yixiang Wang

## 使用说明（给接手的 Claude）

这是 Yixiang 的项目进度文档。每次 session 结束时，Yixiang 会让 Claude 生成一份更新版的 session takeover，把新的进度、踩过的坑、当前代码状态、下一步全部追加进来。

**接手时请做的事：**
1. 通读本文档，了解项目背景和当前状态
2. 从"下一步"部分开始继续
3. 遵守教学风格（micro-step、Java 对比、每步解释 why）
4. session 结束时生成新版 takeover，追加到本文档最后

---


---

## Session 1 — June 13, 2025

### 学生背景
- 姓名：Yixiang Wang (rew006@ucsd.edu, 8186992028)
- 学校：UC San Diego，Math-CS 专业
- 身份：转学生，大三才开始接触 CS，2027 年 6 月本科毕业
- GPA：3.6
- 计划：本科毕业后读 Master（DS 或 Finance 方向），不打算读 MSCS
- 目标：2027 年暑假找到 SDE / AI Engineer 相关实习

### 已修课程
| 课程 | 内容 |
|------|------|
| CSE 11 | Java 入门，OOP 基础 |
| CSE 12 | 数据结构（链表、树、哈希表） |
| CSE 29 | C 语言系统编程 |
| CSE 101 | 算法设计与分析（感觉很难） |
| MATH 170A | 数值线代（SVD、特征值、最小二乘） |
| MATH 103A | 近世代数 I（群论） |
| ECE 176 | Deep Learning（CNN/GAN/Transformer） |
| COGS 108 | 数据科学实践（Python，参与度低） |

### 本次完成
- 分析求职方向：确定 AI Engineer / DS 方向，不做纯 SDE
- 确定暑假项目：Socratic Math Tutor
- 环境配置：VSCode + conda `ece176` + DeepSeek API + python-dotenv
- 实现多轮对话核心代码（messages 列表管理对话历史）
- 理解 `.env` 文件管理 API key

### 已理解概念
- pip、conda 环境
- Python list vs Java ArrayList，dict vs Java HashMap
- `input()`、f-string、`os.environ.get()`、`load_dotenv()`
- messages 列表为什么要存整个历史（AI 每次读全部对话）
- Python 缩进 = Java 大括号

### 踩过的坑
- homebrew python 和 conda python 环境冲突
- `export` 关掉终端就消失，需用 `.env` 文件
- Mac Finder 不能创建 `.` 开头的文件，需用终端 `mv`
- `load_dotenv(API_KEY)` 错误，应为 `load_dotenv("API_KEY.env")`
- 代码缩进错误导致 API 调用在 while 循环外面

### 当前代码状态
多轮对话可以跑通，但还没有 system prompt。

### 下一步
1. 加入 system prompt，从文件读取
2. 实现 Socratic tutor 风格
3. 处理图片输入

---

## Session 2 — June 14, 2025

### 本次完成

#### System Prompt 接入
- 新建 `instruction_prompt.txt`，用 `with open()` 读取
- 修复 bug：`"system_prompt"` 加引号是字符串，去掉才是变量
- Socratic 风格已生效，AI 开始分步讲解，每步确认理解

#### 教学风格确认（默认模式，所有 session 必须遵守）
- 每次只做一个 micro-step，停，确认，再继续
- 矩阵乘法拆成 dot product 逐元素算
- determinant 永远 Laplace expansion，解释为什么选那行/列
- 每步解释"为什么"，不只说操作
- 完成模块后做套路总结
- Python 概念必须给 Java 对比例子
- 禁止用"it follows that"、"therefore"、"hence"跳步骤

#### GitHub Repo 建立
- 地址：https://github.com/RWyx/Math-Tutor
- `.gitignore` 屏蔽：`API_KEY.env`、`.history/`、`session_summary.md`
- 注意：`.history/` 里有 API key 历史记录，危险，必须屏蔽
- 命令：`git rm -r --cached . -f` 强制清除已 staged 文件

#### 项目设计完善
确定完整项目方向：用历年 final exam / HW 建 RAG 题库，出对标真实考试难度的新题，再用 Socratic 方式讲解，SQL 记录错题。

### 已理解概念
- `with open()` 读文件（对应 Java try-with-resources）
- RAG vs 上下文管理的区别
- LangChain 是什么（类比 Spring Framework）
- SQLite vs PostgreSQL vs MongoDB 的区别和适用场景
- 题库版权问题：官网公开材料合法，推荐 UCSD 官网 + MIT OCW

### 踩过的坑
- `messages.append{"role": ...}` 错误，append 后要用 `()`
- `"system_prompt"` 加引号变字符串
- `.history/` 文件夹包含 API key 历史，差点上传到 GitHub

### 当前代码状态

```python
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv("API_KEY.env")

with open("instruction_prompt.txt", "r") as f:
    system_prompt = f.read()

client = OpenAI(
    api_key=os.environ.get("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com"
)

messages = [
    {"role": "system", "content": system_prompt}
]

print("What's your problem")

while True:
    user_input = input("Student: ")
    if user_input == "quit":
        break
    messages.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=messages
    )
    ai_reply = response.choices[0].message.content
    messages.append({"role": "assistant", "content": ai_reply})
    print(f"AI：{ai_reply}\n")
```

### 下一步
1. **图片输入**：用户输入图片路径，转 base64 发给 AI
2. **收集题库材料**：UCSD 官网 + MIT OCW 找 typed PDF
3. **手动写 RAG**：读 PDF → 切割 → 向量检索 → 出新题
4. **SQL 错题本**
5. **LangChain 重构**
6. **Streamlit 界面**

### 教学风格备注
- Java 背景，Python 刚开始学
- 每次解释 Python 概念必须给 Java 对比例子
- 逐行理解代码，不要一次给太多
- 遇到报错直接截图发过来

---

## 附：CODEX 课程复习模板（项目灵感来源）

Yixiang 有一套用 AI 复习课程的 prompt 模板（`CODEX_Course_Review_Prompt_Template.md`），核心流程：

> 上传 lecture PDF + HW + 真实 Midterm → AI 逐页读取 → 生成结构化复习笔记 → 预测考题

**和项目的关联：**

这个模板逻辑和 Socratic Tutor 项目可以合并：

> 上传 lecture PDF + 历年 exam → RAG 从材料里出对标真实考试难度的新题 → Socratic 讲解

所以 RAG 的材料不只是 exam，还可以包括：
- Lecture slides
- HW solutions
- Practice exam solutions

**给 Claude Code 写 prompt 时也可以参考这个模板的结构**——逐步上传材料、指定输出格式、明确不允许跳步骤。

模板文件保存在 Yixiang 本地（`CODEX_Course_Review_Prompt_Template.md`），需要时直接发给新 session 参考。
