from ..config.database import table_config, pg_config
from . import database
from . import student

_student_handler = database.StudentPGHandler(table_config, pg_config)
student_da = student.StudentDA(_student_handler)
