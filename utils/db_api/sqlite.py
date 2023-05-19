import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    def create_table_blocks(self):
        sql = """
        CREATE TABLE IF NOT EXISTS blocks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_groups(self):
        sql = """
        CREATE TABLE IF NOT EXISTS groups (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name VARCHAR(100) NOT NULL
        );
        """
        self.execute(sql, commit=True)

    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            group_type VARCHAR(100),
            block_1 VARCHAR(100),
            block_2 VARCHAR(100),
            full_name VARCHAR(100) NOT NULL,
            payment VARCHAR(100) NOT NULL
            );
"""
        self.execute(sql, commit=True)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())

    def add_user(self, group_type: str, block_1: str, block_2: str, full_name: str, payment: str):
        sql = """
        INSERT INTO users(group_type, block_1, block_2, full_name, payment) VALUES(?, ?, ?, ?, ?)
        """
        self.execute(sql, parameters=(group_type, block_1, block_2, full_name, payment), commit=True)

    def select_all_users(self):
        sql = """
        SELECT * FROM users
        """
        return self.execute(sql, fetchall=True)

    def select_user(self, **kwargs):
        # SQL_EXAMPLE = "SELECT * FROM users where id=1 AND Name='John'"
        sql = "SELECT * FROM users WHERE "
        sql, parameters = self.format_args(sql, kwargs)

        return self.execute(sql, parameters=parameters, fetchone=True)

    def count_users(self):
        return self.execute("SELECT COUNT(*) FROM users;", fetchone=True)

    def update_user_email(self, email, id):
        # SQL_EXAMPLE = "UPDATE users SET email=mail@gmail.com WHERE id=12345"

        sql = f"""
        UPDATE users SET email=? WHERE id=?
        """
        return self.execute(sql, parameters=(email, id), commit=True)

    def delete_users(self):
        self.execute("DELETE FROM users WHERE TRUE", commit=True)


    """ GROUPS TABLE """
    def prefer_groups(self):
        sql = r"""
        INSERT INTO groups (name)
        VALUES ('Abituriyent'), ('O`rta'), ('Maktab');
        """
        return self.execute(sql, commit=True)

    def get_groups(self):
        return self.execute("SELECT * FROM groups", fetchall=True)


    """ BLOCK TABLE """
    def prefer_block(self):
        sql = r"""
        INSERT INTO blocks (name)
        VALUES 
        ('Matem A'),
        ('Matem B'),
        ('Matem C'),
        ('Matem D'),
        
        ('Fizika A'),
        ('Fizika B'),
        
        ('Ona tili A'),
        ('Ona tili B'),
        
        ('Ing tili A'),
        ('Ing tili B'),
        ('Ing tili C'),
        ('Ing tili D'),
	('IELST'),
	('CEFR'),
        
        ('Rus tili A'),
        ('Rus tili B'),
        
        ('Kimyo A'), 
        ('Kimyo B'),
        
        ('Biologiya A'),
        ('Biologiya B'),
        
        ('Geografiya'),
        
        ('Tarix A'),
        ('Tarix B'),
        
        ('Fransuz tili');
        """
        self.execute(sql, commit=True)

    def get_blocks(self):
        return self.execute("SELECT * FROM blocks", fetchall=True)
def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")
