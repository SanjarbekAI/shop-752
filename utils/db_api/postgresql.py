import psycopg2


class DBManager:
    def __init__(self):
        self.conn = psycopg2.connect(
            database='shop_db',
            user='bot',
            password='sanjarbek2002',
            host='localhost',
            port=5432
        )
        self.cursor = self.conn.cursor()

    def get_user(self, chat_id):
        query = f"SELECT * FROM users WHERE chat_id = {chat_id}"
        return self.cursor.execute(query).fetchone()

    def insert_user(self, data: dict):
        full_name = data['full_name']
        login = data['login']
        password = data['password']
        phone_number = data['phone_number']
        chat_id = data['chat_id']

        query = "INSERT INTO users (full_name, login, password, chat_id, phone_number) VALUES (?,?,?,?,?)"
        values = (full_name, login, password, chat_id, phone_number)

        self.cursor.execute(query, values)
        self.conn.commit()
        return True

class TableManager(DBManager):
    def create_table(self):
        query = """CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        chat_id INTEGER,
        phone_number TEXT NOT NULL,
        login TEXT NOT NULL,
        password TEXT NOT NULL,
        full_name TEXT NOT NULL
        )
        """
        # query = """CREATE TABLE IF NOT EXISTS products (
        #   id INTEGER PRIMARY KEY,
        #   chat_id INTEGER,
        #   name TEXT NOT NULL,
        #   price REAL NOT NULL,
        #   info TEXT NOT NULL,
        #   photo TEXT NOT NULL,
        #   status TEXT NOT NULL,
        #   created_at TEXT NOT NULL
        #   )
        #   """
        self.cursor.execute(query)
        self.conn.commit()


table_manager = TableManager()
table_manager.create_table()

