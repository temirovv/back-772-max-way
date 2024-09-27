import sqlite3


class Database:
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([f"{item} = ?" for item in parameters])
        return sql, tuple(parameters.values())
    
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


    def create_users_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS users (
            tg_id INTEGER PRIMARY KEY AUTOINCREMENT,
            first_name VARCHAR(255),
            last_name VARCHAR(255),
            phone_number VARCHAR(20),
            username VARCHAR(55)
        )'''
        self.execute(sql)

    def create_category_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS category(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255)
        )'''

        self.execute(sql)

    def create_products_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS products(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(255),
            description TEXT,
            price REAL,
            image VARCHAR(255),
            category_id INTEGER,
            FOREIGN KEY (category_id) REFERENCES category(id)
        )'''
        self.execute(sql)

    def create_vacancy_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS vacancy (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title VARCHAR(120),
            is_active BOOLEAN DEFAULT TRUE
        )'''
        self.execute(sql)

    def create_cart_table(self):
        sql = '''CREATE TABLE IF NOT EXISTS cart (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        product INTEGER,
        quantity INTEGER,
        user INTEGER,
        FOREIGN KEY (product) REFERENCES products(id)
        )'''
        self.execute(sql)

    def add_to_cart(self, product_name, quantity, user):
        sql = '''INSERT INTO cart
        (product, quantity, user)
        VALUES
        ((SELECT id FROM products WHERE name = ?), ?, ?)'''
        self.execute(sql,parameters=(product_name,quantity,user),commit=True)

    def add_product(self, name, description, price, image, category_id):
        sql = '''INSERT INTO products
                    (name, description, price, image, category_id)
                 VALUES
                    (?, ?, ?, ?, ?)'''
        self.execute(sql, parameters=(name, description, price, image, category_id), commit=True)
        

    def add_vacancy(self, title):
        sql = '''INSERT INTO vacancy (title) VALUES (?)'''
        self.execute(sql, parameters=(title,), commit=True)
        
    def add_category(self, name):
        sql = '''INSERT INTO category (name) VALUES (?)'''
        self.execute(sql, parameters=(name,), commit=True)

    def get_categories_for_admin(self):
        sql = '''SELECT id, name FROM category'''
        return self.execute(sql, fetchall=True)

    def get_products_by_category(self, name: str):
        sql = '''
        SELECT name FROM products
        WHERE category_id = (SELECT id FROM category WHERE name = ?)
        '''
        return self.execute(sql, parameters=(name,), fetchall=True)

    def get_product(self, name: str):
        sql = '''SELECT name, description, price, image FROM
        products WHERE name = ?'''

        return self.execute(sql, parameters=(name,), fetchone=True)

    def get_user_cart(self, user):
        sql = '''SELECT products.name, products.price, cart.quantity
        FROM products
        INNER JOIN cart ON products.id = cart.product
        WHERE cart.user = ?'''

        return self.execute(sql,parameters=(user,), fetchall=True)


    def clean_user_cart(self, user):
        sql = '''DELETE FROM cart WHERE user = ?'''
        self.execute(sql, parameters=(user,), commit=True)
        

def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")

baza = Database()


