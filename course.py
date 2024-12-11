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
        sorted_courses = sorted(
            filtered, key=lambda x: any(pref in x["description"] for pref in self.user_preferences), reverse=True
        )
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
