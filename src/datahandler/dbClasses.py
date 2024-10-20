import sqlite3
from datetime import datetime

DataBase = "database.db"


def merge(key_names, values, pop_key: str = None):
    value = dict(zip(key_names, values))
    if value.get(pop_key):
        value.pop(pop_key)
    return value


class UserHandler:
    def __init__(self):
        self.conn = sqlite3.connect(DataBase)
        self.create_user_table()

    def create_user_table(self):
        query = '''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            phone TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            user_type TEXT DEFAULT 'user',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
        '''
        self.conn.execute(query)
        self.conn.commit()
        print("Created: User Table Created")

    def new_user(self, name, email, phone, password, user_type='user'):
        # Check if the email or phone already exists
        check_query = '''
        SELECT * FROM users WHERE email = ? OR phone = ?
        '''
        cur = self.conn.execute(check_query, (email, phone))

        if not cur.fetchone():
            # If not, create the new user
            insert_query = '''
            INSERT INTO users (name, email, phone, password, user_type)
            VALUES (?, ?, ?, ?, ?)
            '''
            self.conn.execute(insert_query, (name, email,
                                             phone, password, user_type))
            self.conn.commit()
            print("Success: User Created Successfully.")
        else:
            print("Error: Email or Phone Already Exists.")

    def get_user(self, user_id=None, name=None, email=None, phone=None, password=None, user_type=None, query_type=' AND '):
        filters = []
        params = []

        if user_id:
            filters.append("user_id = ?")
            params.append(user_id)
        if name:
            filters.append("name = ?")
            params.append(name)
        if email:
            filters.append("email = ?")
            params.append(email)
        if phone:
            filters.append("phone = ?")
            params.append(phone)
        if password:
            filters.append("password = ?")
            params.append(password)
        if user_type:
            filters.append("user_type = ?")
            params.append(user_type)

        if not filters:
            return []

        query = f"SELECT * FROM users WHERE {query_type.join(filters) }"
        cur = self.conn.execute(query, tuple(params))
        rows = cur.fetchall()

        if not rows:
            return []

        # Fetch column names
        column_names = [description[0] for description in cur.description]

        # Return each row as a dictionary
        return [merge(column_names, row, pop_key="password") for row in rows]

    def update_user(self, user_id, name=None, email=None, phone=None, password=None, user_type=None):
        updates = []
        params = []

        if name:
            updates.append("name = ?")
            params.append(name)
        if email:
            updates.append("email = ?")
            params.append(email)
        if phone:
            updates.append("phone = ?")
            params.append(phone)
        if password:
            updates.append("password = ?")
            params.append(password)
        if user_type:
            updates.append("user_type = ?")
            params.append(user_type)

        if not updates:
            return "No parameters provided for updating user."

        query = f"UPDATE users SET {', '.join(updates)} WHERE user_id = ?"
        params.append(user_id)
        self.conn.execute(query, tuple(params))
        self.conn.commit()
        return "User updated successfully."

    def delete_user(self, user_id=None, email=None, phone=None):
        filters = []
        params = []

        if user_id:
            filters.append("user_id = ?")
            params.append(user_id)
        if email:
            filters.append("email = ?")
            params.append(email)
        if phone:
            filters.append("phone = ?")
            params.append(phone)

        if not filters:
            return "No parameters provided for deleting user."

        query = f"DELETE FROM users WHERE {' OR '.join(filters)}"
        self.conn.execute(query, tuple(params))
        self.conn.commit()
        return "User deleted successfully."

    def __del__(self):
        self.conn.close()
