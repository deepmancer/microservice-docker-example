class StudentSchema:
    def __init__(self, student_tuple):
        self.id, self.name, self.age, self.student_id, self.education_level = student_tuple

    def __repr__(self):
        return f"<Student id={self.id}, name={self.name}, age={self.age}, student_id={self.student_id}, education_level={self.education_level}>"

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "student_id": self.student_id,
            "education_level": self.education_level
        }
