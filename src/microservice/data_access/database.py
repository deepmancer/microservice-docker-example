import psycopg2
from psycopg2 import sql


class PGHandler:
    _instance = None

    def __new__(cls, db_params):
        if cls._instance is None:
            cls._instance = super(PGHandler, cls).__new__(cls)
            cls._instance.db_params = db_params
            cls._instance._setup()
        return cls._instance

    def _setup(self):
        try:
            self.conn = psycopg2.connect(**self.db_params)
            self.cur = self.conn.cursor()
            print("Database connection established.")
        except psycopg2.DatabaseError as e:
            raise Exception(f"Database connection failed: {e}")

    def down(self):
        if self.cur is not None:
            self.cur.close()
            print("Cursor closed.")
        if self.conn is not None:
            self.conn.close()
            print("Database connection closed.")


class StudentPGHandler(PGHandler):
    _instance = None

    def __new__(cls, table_config, db_params):
        if cls._instance is None:
            cls._instance = super(StudentPGHandler, cls).__new__(cls, db_params)
            cls._instance.table_config = table_config
            cls._instance.table_name = table_config['table_name']
            cls._instance._setup_table()
        return cls._instance

    def _setup_table(self):
        super()._setup()
        table_name, columns = self.table_config['table_name'], self.table_config['columns']
        column_definitions = ", ".join([f"{col['name']} {col['type']}" for col in columns])
        create_table_query = sql.SQL("CREATE TABLE IF NOT EXISTS {} ({})").format(
            sql.Identifier(table_name),
            sql.SQL(column_definitions)
        )

        try:
            self.cur.execute(create_table_query)
            self.conn.commit()
            print(f"Table '{table_name}' created or already exists.")
        except psycopg2.DatabaseError as e:
            self.conn.rollback()
            raise Exception(f"Error creating table: {e}")

    def add(self, name, age, student_id, education_level):
        query = f"INSERT INTO {self.table_name} (name, age, student_id, education_level) VALUES (%s, %s, %s, %s) RETURNING *"
        self.execute_query(query, (name, age, student_id, education_level), commit=True)
        return self.cur.fetchone()

    def modify(self, name, age, student_id, education_level):
        query = f"UPDATE {self.table_name} SET name = %s, age = %s, education_level = %s WHERE student_id = %s RETURNING *"
        self.execute_query(query, (name, age, education_level, student_id), commit=True)
        return self.cur.fetchone()

    def delete(self, student_id):
        select_query = f"SELECT * FROM {self.table_name} WHERE student_id = %s"
        self.execute_query(select_query, (student_id,))
        row = self.cur.fetchone()

        if row:
            delete_query = f"DELETE FROM {self.table_name} WHERE student_id = %s"
            self.execute_query(delete_query, (student_id,), commit=True)

        return row

    def get_by_col(self, col, val):
        query = f'SELECT * FROM {self.table_name} WHERE {col} = %s'
        self.execute_query(query, (val,))
        return self.cur.fetchone()

    def get_all(self):
        query = f'SELECT * FROM {self.table_name}'
        self.execute_query(query, ())
        return self.cur.fetchall()

    def execute_query(self, query, params=None, commit=False):
        try:
            self.cur.execute(query, params)
            if commit:
                self.conn.commit()
        except psycopg2.DatabaseError as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()
            raise Exception(f"Error executing query: {query} with the error of {e}")
