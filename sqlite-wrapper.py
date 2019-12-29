import sqlite3 as sq

class SQLiteDatabase:

    def __init__(self, db_name):
        self.db = sq.connect(db_name)
        self.cursor = self.db.cursor()
        self.cursor.row_factory = sq.Row
    
    def close(self):
        self.db.close()
    
    def create_table(self, table_name, **kwargs):
        data_type = ""
        for key, value in kwargs:
            data_type += key + " " + " ".join(value) + ", "    
        query = f"CREATE TABLE {table_name} ({data_type.strip(' ,')})"
        self.cursor.execute(query)
        self.db.commit()
    
    def insert_data(self, table_name, *contents, **kwargs):
        """
        TODO: Fix This
        Do not use both 'contents' and 'kwargs'. Choose one.
        """
        length = len(contents) if contents else len(kwargs)
        if kwargs:
            data_type = "(" + ", ".join(kwargs.keys()) + ")"
        elif contents:
            contents = [str(i) for i in contents]
            data_type = ""
        values_placeholders = ("?, "*length).strip(", ")
        query = f"INSERT INTO {table_name}{data_type} VALUES ({values_placeholders})"
        # print(query, "\n", kwargs.values())
        self.cursor.execute(query, contents if contents else list(kwargs.values()))
        self.db.commit()
    
    def get_data(self, table_name, columns=[], condition=""):
        cols = ", ".join(columns).strip(", ") if columns else "*"
        query = f"SELECT {cols} from {table_name} "
        if condition:
            query += condition
        self.cursor.execute(query.strip())
        return self.cursor.fetchall()

    def update_row(self, table_name, col_name, row_id,  **kwargs):
        query = f"UPDATE {table_name} SET "
        sorted_keys = sorted(kwargs)
        sorted_keys_value = [kwargs[x] for x in sorted_keys]
        for key in sorted_keys:
            query += key + " = ?, "
        query = query.strip(", ") + f" WHERE {col_name}={row_id}"
        self.cursor.execute(query, sorted_keys_value)
        self.db.commit()
    
    def update_row_tuple(self, table_name, col_name, row_id,  tuple_row):
        query = f"UPDATE {table_name} SET "
        kwargs = dict(tuple_row)
        sorted_keys = sorted(kwargs)
        sorted_keys_value = [kwargs[x] for x in sorted_keys]
        for key in sorted_keys:
            query += key + " = ?, "
        query = query.strip(", ") + f" WHERE {col_name}={row_id}"
        self.cursor.execute(query, sorted_keys_value)
        self.db.commit()

    def delete_row(self, table_name, col_name, row_id):
        query = f"DELETE FROM {table_name} WHERE {col_name}={row_id}"
        self.cursor.execute(query)
        self.db.commit()
    