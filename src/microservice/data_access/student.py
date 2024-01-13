class StudentDA:
    def __init__(self, student_pg_handler):
        self.pg_handler = student_pg_handler

    def insert_student(self, name, age, student_id, education_level):
        response = self.pg_handler.add(name, age, student_id, education_level)
        return response

    def modify_student(self, name, age, student_id, education_level):
        response = self.pg_handler.modify(name, age, student_id, education_level)
        return response

    def delete_student(self, student_id):
        response = self.pg_handler.delete(student_id)
        return response

    def get_all_students(self):
        students = self.pg_handler.get_all()
        return students

    def get_student_by_student_id(self, student_id):
        student = self.pg_handler.get_by_col('student_id', student_id)
        return student
