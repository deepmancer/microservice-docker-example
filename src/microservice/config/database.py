pg_config = {
    'database': 'postgres',
    'user': 'postgres',
    'password': '1qaz2wsx@',
    'host': 'postgres',
    'port': 5432
}

table_config = {
    "table_name": "student",
    "columns": [
        {"name": "id", "type": "SERIAL PRIMARY KEY"},
        {"name": "name", "type": "VARCHAR(100)"},
        {"name": "age", "type": "INT"},
        {"name": "student_id", "type": "VARCHAR(50) UNIQUE"},
        {"name": "education_level", "type": "VARCHAR(50)"},
    ],
}
