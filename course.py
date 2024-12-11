class CourseSystem:
    def __init__(self):
        # 模拟课程数据库，初始课程数据
        self.courses = [
            {"id": 1, "name": "羽毛球", "type": "选修", "description": "体育相关课程"},
            {"id": 2, "name": "数学分析", "type": "必修", "description": "数学基础课程"},
            {"id": 3, "name": "Python 编程", "type": "选修", "description": "计算机编程基础"},
            {"id": 4, "name": "哲学概论", "type": "选修", "description": "人文基础课程"},
            {"id": 5, "name": "线性代数", "type": "必修", "description": "数学应用课程"},
        ]
        self.next_id = 6  # 用于生成新的课程 ID

    def list_courses(self):
        """列出所有课程"""
        return self.courses

    def add_course(self, name, course_type, description):
        """添加新课程"""
        new_course = {
            "id": self.next_id,
            "name": name,
            "type": course_type,
            "description": description,
        }
        self.courses.append(new_course)
        self.next_id += 1
        return new_course

    def update_course(self, course_id, name=None, course_type=None, description=None):
        """更新课程信息"""
        for course in self.courses:
            if course["id"] == course_id:
                if name is not None:
                    course["name"] = name
                if course_type is not None:
                    course["type"] = course_type
                if description is not None:
                    course["description"] = description
                return course
        return {"error": f"未找到课程 ID 为 {course_id} 的课程"}

    def delete_course(self, course_id):
        """删除课程"""
        for course in self.courses:
            if course["id"] == course_id:
                self.courses.remove(course)
                return {"status": "success", "removed": course}
        return {"error": f"未找到课程 ID 为 {course_id} 的课程"}

    def delete_course_by_name(self, course_name):
        """删除课程"""
        for course in self.courses:
            if course["name"] == course_name:
                self.courses.remove(course)
                return {"status": "success", "removed": course}
        return {"error": f"未找到课程名称为 {course_name} 的课程"}


# 测试示例
if __name__ == "__main__":
    system = CourseSystem()

    # 列出所有课程
    print("所有课程:", system.list_courses())

    # 添加新课程
    new_course = system.add_course("人工智能", "选修", "计算机高级课程")
    print("添加课程:", new_course)

    # 更新课程
    updated_course = system.update_course(3, name="Python 高级编程", description="深入学习 Python 的课程")
    print("更新课程:", updated_course)

    # 删除课程
    deleted_course = system.delete_course(2)
    print("删除课程:", deleted_course)

    # 再次列出所有课程
    print("更新后的课程列表:", system.list_courses())
