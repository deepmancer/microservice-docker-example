import math

from .id_generator import generate_id
from ..data_access import student_da
from ..config.education_level import allowed_education_levels


def add_student(name, age, education_level):
    try:
        if education_level not in allowed_education_levels:
            raise ValueError(f'education_level must be in {allowed_education_levels}')
        if age < 18 and education_level == "undergraduate":
            raise ValueError('Not old enough for undergraduate studies')
        if age < 22 and education_level == "graduate":
            raise ValueError('Not old enough for graduate studies')
        if age < 25 and education_level == "phd":
            raise ValueError('Not old enough for PhD studies')

        student_id = generate_id(name, age, education_level)
        student_data = student_da.insert_student(name, age, student_id, education_level)
        return student_data
    except Exception as e:
        raise Exception(f"Error in adding student: {e}")


def modify_student(student_id, name, age, education_level):
    try:
        student = student_da.get_student_by_student_id(student_id)
        if student is None:
            raise ValueError('Student not found')
        if math.fabs(allowed_education_levels.index(student[-1]) - allowed_education_levels.index(
                education_level)) > 1:
            raise ValueError('Cannot modify the education_level with skipping graduate')

        student_data = student_da.modify_student(name, age, student_id, education_level)
        return student_data

    except Exception as e:
        raise Exception(f"Error in modifying student: {e}")


def delete_student(student_id):
    try:
        student_data = student_da.delete_student(student_id)
        return student_data
    except Exception as e:
        raise Exception(f"Error in deleting student: {e}")


def get_student_information(student_id):
    try:
        return student_da.get_student_by_student_id(student_id)
    except Exception as e:
        raise Exception(f"Error in retrieving student information: {e}")


def get_all_students_information():
    try:
        return student_da.get_all_students()
    except Exception as e:
        raise Exception(f"Error in retrieving all students' information: {e}")
