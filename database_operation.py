import pymysql


class Databaseclass:
    def __init__(self,host,user,password,database):
        self.connection = pymysql.connect(
            host = host,
            user = user,
            password = password,
            database = database
        )
        self.cursor = self.connection.cursor()
        
    def fetch_table(self):
        self.cursor.execute("SHOW TABLES")
        return [table[0]for table in self.cursor.fetchall()]
    
    def fetch_column(self, table_name):
        self.cursor.execute(f"DESCRIBE {table_name}")
        return [row[0] for row in self.cursor.fetchall()]
    
    def execute_query(self,query,parmas=None):
        try:
            cursor = self.connection.cursor()
            if parmas:
                cursor.execute(query,parmas)
            else:
                cursor.execute(query)
            self.connection.commit()
            cursor.close()
        except Exception as e:
            raise e
    

    def fetch_data(self,query):
        try:
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print(f"error fetching data: {e}")
            return None
    
    def insert_data(self, table, data):
        
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['%s'] * len(data))
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
    
        try:
            self.cursor.execute(query, tuple(data.values()))
            self.connection.commit()
            self.cursor.close()
        except pymysql.MySQLError as e:
            self.connection.rollback()
    
    def alter_table(self, table, alter_query):
      
        queryy = f"ALTER TABLE {table} {alter_query}"
        
        try:
            self.cursor.execute(alter_query)
            self.connection.commit()
            self.cursor.close()
            # print(f"Table {table} altered successfully.")
        except pymysql.MySQLError as e:
            # print(f"Error altering table {table}: {e}")
            self.connection.rollback()