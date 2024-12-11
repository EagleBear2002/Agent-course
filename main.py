import os
from langchain.chat_models import *
from languagedriven import LanguageDrivenCourseSystem

if __name__ == "__main__":
    # 初始化语言模型
    os.environ["OPENAI_API_KEY"] = "None"
    os.environ["OPENAI_API_BASE"] = "http://10.58.0.2:8000/v1"
    model = ChatOpenAI(model="Qwen2.5-14B")

    # 初始化系统
    ld_system = LanguageDrivenCourseSystem(model)

    # 用户自然语言交互
    while True:
        user_input = input("请输入您的需求（例如：查询所有选修课）：")
        if user_input.lower() in ["退出", "exit"]:
            break
        result = ld_system.handle_query(user_input)
        print("系统响应：", result)
