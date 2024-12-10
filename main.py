from langchain.chat_models import *


class CourseSystem:
    def __init__(self):
        # 模拟课程数据
        self.courses = [
            {"id": 1, "name": "羽毛球", "type": "选修", "description": "体育相关课程"},
            {"id": 2, "name": "数学分析", "type": "必修", "description": "数学基础课程"},
            {"id": 3, "name": "Python 编程", "type": "选修", "description": "计算机编程基础"},
            {"id": 4, "name": "哲学概论", "type": "选修", "description": "人文基础课程"},
            {"id": 5, "name": "线性代数", "type": "必修", "description": "数学应用课程"},
        ]
        self.selected_courses = []
        self.user_preferences = ["体育", "计算机"]  # 模拟用户偏好

    def query_courses(self, filter_type=None):
        # 筛选课程
        if filter_type:
            filtered = [course for course in self.courses if course["type"] == filter_type]
        else:
            filtered = self.courses
        # 根据用户偏好排序
        sorted_courses = sorted(filtered, key=lambda x: any(pref in x["description"] for pref in self.user_preferences),
                                reverse=True)
        return sorted_courses

    def select_course(self, course_name):
        # 智能选课
        course = next((c for c in self.courses if c["name"] == course_name), None)
        if not course:
            similar_courses = [c["name"] for c in self.courses if
                               course_name in c["name"] or course_name in c["description"]]
            return {"status": "error", "message": f"未找到课程 '{course_name}'", "suggestions": similar_courses}
        if course in self.selected_courses:
            return {"status": "error", "message": f"课程 '{course_name}' 已被选择"}
        self.selected_courses.append(course)
        return {"status": "success", "selected": course}

    def delete_course(self, course_name):
        # 智能删除
        course = next((c for c in self.selected_courses if c["name"] == course_name), None)
        if not course:
            similar_courses = [c["name"] for c in self.selected_courses if course_name in c["name"]]
            return {"status": "error", "message": f"未找到已选课程 '{course_name}'", "suggestions": similar_courses}
        self.selected_courses.remove(course)
        return {"status": "success", "removed": course}


class LanguageDrivenCourseSystem:
    def __init__(self, model):
        self.system = CourseSystem()  # 调用之前实现的选课系统
        self.model = model  # 大语言模型实例

    def handle_query(self, user_input):
        # 使用大语言模型解析用户意图
        prompt = f"""
        你是一个智能选课助手，帮助用户完成以下需求：
        需求：{user_input}
        请根据需求生成适当的函数调用和参数。
        函数必须是 CourseSystem 类的已有方法，并返回 JSON 结果。例如：
        - 查询必修课程：调用 query_courses("必修")
        - 选择课程：调用 select_course("羽毛球")
        - 删除课程：调用 delete_course("羽毛球")
        """
        try:
            response = self.model.invoke(prompt)
            code_to_execute = response.strip()

            # 执行生成的代码
            exec(f"result = self.system.{code_to_execute}")
            return locals()['result']
        except Exception as e:
            return {"status": "error", "message": f"执行失败：{str(e)}"}


if __name__ == "__main__":
    # 初始化语言模型
    model = ChatOpenAI(model="Qwen2.5-14B", server_url="http://10.58.0.2:8000/v1", api_key="None")

    # 初始化系统
    ld_system = LanguageDrivenCourseSystem(model)

    # 用户自然语言交互
    while True:
        user_input = input("请输入您的需求（例如：查询所有选修课）：")
        if user_input.lower() in ["退出", "exit"]:
            break
        result = ld_system.handle_query(user_input)
        print("系统响应：", result)
