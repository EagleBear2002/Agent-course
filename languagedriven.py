import json
import logging

from course import CourseSystem

# 配置日志
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


class LanguageDrivenCourseSystem:
    def __init__(self, model):
        self.system = CourseSystem()  # 调用之前实现的选课系统
        self.model = model  # 大语言模型实例

    def handle_query(self, user_input):
        """处理用户输入的自然语言需求"""
        prompt = f"""
        你是一个智能选课助手，帮助用户完成以下需求：
        用户输入：{user_input}
        请直接分析用户意图并调用 CourseSystem 中的方法完成需求。
        返回 JSON 格式的结果。
        """
        try:
            # 调用大语言模型进行解析
            response = self.model.invoke([{"role": "user", "content": prompt}])

            # 检查模型返回内容
            if not isinstance(response, dict) or "content" not in response:
                return {"status": "error", "message": "模型响应格式不正确"}

            action_data = json.loads(response["content"])
            action = action_data.get("action")
            parameters = action_data.get("parameters", {})

            if not hasattr(self.system, action):
                return {"status": "error", "message": f"操作 '{action}' 不存在"}

            # 动态调用对应的方法
            method = getattr(self.system, action)
            result = method(**parameters)
            return result

        except Exception as e:
            logging.error(f"执行失败：{e}")
            return {"status": "error", "message": f"执行失败：{str(e)}"}
