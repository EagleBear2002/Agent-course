from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.chat_models import ChatOpenAI
from course import CourseSystem


class LanguageDrivenCourseSystem:
    def __init__(self, model):
        self.model = model
        # 在构造函数中创建 CourseSystem 实例
        self.course_system = CourseSystem()

        # 定义一个处理查询的 Prompt 模板
        self.query_prompt = PromptTemplate(
            input_variables=["query"],
            template="""
            你是一个智能选课助手，用户可以通过自然语言进行选课、查询课程、删除课程等操作。
            请解析以下用户输入，并生成相应的操作指令：
            支持的操作包括：
            1. 列出所有课程
            2. 添加课程
            3. 更新课程
            4. 删除课程

            示例：
            用户输入: "我想添加一门选修课，名字是机器学习，描述是人工智能相关课程"
            输出: {{"action": "add", "name": "机器学习", "type": "选修", "description": "人工智能相关课程"}}

            用户输入: "列出所有课程"
            输出: {{"action": "list"}}

            用户输入: {query}
            请输出格式化后的 JSON，不要输出解释或其他内容。
            """
        )
        # 设置 LLMChain
        self.query_chain = LLMChain(llm=self.model, prompt=self.query_prompt)

    def handle_query(self, user_input):
        # 使用大语言模型处理用户输入
        action_json = self.query_chain.run({"query": user_input})
        print(f"生成的操作指令：{action_json}")

        # 将 JSON 转换为 Python 字典
        try:
            action = eval(action_json)
        except Exception as e:
            return {"error": "解析操作指令失败", "details": str(e)}

        # 根据操作指令调用 CourseSystem 的方法
        if action["action"] == "list":
            return self.course_system.list_courses()

        elif action["action"] == "add":
            return self.course_system.add_course(
                name=action["name"],
                course_type=action["type"],
                description=action["description"]
            )

        elif action["action"] == "update":
            return self.course_system.update_course(
                course_id=action["id"],
                name=action.get("name"),
                course_type=action.get("type"),
                description=action.get("description")
            )

        elif action["action"] == "delete":
            return self.course_system.delete_course_by_name(course_name=action["name"])

        else:
            return {"error": "未识别的操作指令"}
