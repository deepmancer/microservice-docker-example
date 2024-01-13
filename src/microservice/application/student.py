from ..domain import student as student_handler
from ..config.student_schema import StudentSchema
from .validator import Validator


def add_student(name, age, education_level):
    try:
        Validator.validate_name(name)
        Validator.validate_age(age)
        Validator.validate_education_level(education_level)
        age = int(age)
        student_data = student_handler.add_student(name, age, education_level)
        return StudentSchema(student_data)
    except ValueError as e:
        return f"Validation error: {e}"
    except Exception as e:
        return f"Error adding student: {e}"


def modify_student(student_id, name, age, education_level):
    try:
        Validator.validate_name(name)
        Validator.validate_age(age)
        Validator.validate_education_level(education_level)
        student_data = student_handler.modify_student(student_id, name, age, education_level)
        return StudentSchema(student_data)
    except ValueError as e:
        return f"Validation error: {e}"
    except Exception as e:
        return f"Error modifying student: {e}"


def delete_student(student_id):
    try:
        student_data = student_handler.delete_student(student_id)
        return StudentSchema(student_data)
    except Exception as e:
        return f"Error deleting student: {e}"


def get_student_information(student_id):
    try:
        return StudentSchema(student_handler.get_student_information(student_id))
    except Exception as e:
        return f"Error retrieving student information: {e}"


def get_all_students_information():
    try:
        return [StudentSchema(s) for s in student_handler.get_all_students_information()]
    except Exception as e:
        return f"Error retrieving all students' information: {e}"
