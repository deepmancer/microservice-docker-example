class Validator:
    @staticmethod
    def validate_name(name):
        if not isinstance(name, str):
            raise ValueError("Name must be a string.")
        if not name:
            raise ValueError("Name cannot be empty.")
        if len(name) > 100:
            raise ValueError("Name cannot be more than 100 characters.")
        return True

    @staticmethod
    def validate_age(age):
        if not isinstance(age, int):
            raise ValueError("Age must be an integer.")
        if age < 0:
            raise ValueError("Age cannot be negative.")
        if age > 100:
            raise ValueError("Age seems unrealistic.")
        return True

    @staticmethod
    def validate_education_level(education_level):
        valid_education_levels = {'undergraduate', 'graduate', 'phd'}
        if not isinstance(education_level, str):
            raise ValueError("education_level must be a string.")
        if education_level not in valid_education_levels:
            raise ValueError(f"education_level must be one of {valid_education_levels}.")
        return True
