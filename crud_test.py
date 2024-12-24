import streamlit as st
import pandas as pd

# CRUD operation class
class CRUDClass:
    def __init__(self, mydb):
        self.db = mydb

    def create_table(self):
        table_name = st.text_input("Enter the Table Name")
        column_definitions = st.text_area(
            "Enter Column definition (e.g., Customer_id VARCHAR(255) PRIMARY KEY, name VARCHAR(50), email VARCHAR(100), phone VARCHAR(20), location VARCHAR(500))"
        )
        if st.button("Create Table"):
            if not table_name or not column_definitions:
                st.error("Enter the Details")
                return
            
            query = f"CREATE TABLE {table_name} ({column_definitions});"
            try:
                self.db.execute_query(query)
                st.success(f"Table {table_name} created successfully")
            except Exception as e:
                st.error(f"Error: {str(e)}")

    def read_table(self):
        
        table_name = st.selectbox("Select a table", self.db.fetch_table())
        if table_name:
            query = f"SELECT * FROM {table_name}"
            try:
                data = pd.read_sql(query, self.db.connection)
                st.dataframe(data)
            except Exception as e:
                st.error(f"Error: {str(e)}")

    

    def insert_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_table())
        if table_name:
            columns = self.db.fetch_column(table_name)
            column_values = {}

            for column in columns:
                value = st.text_input(f"Enter value for {column}")

           
                if value == "":
                    column_values[column] = None 
                else:
                    column_values[column] = value

        
            if st.button("Insert Tabla"):
                missing_columns = [col for col, val in column_values.items() if val is None]
                if missing_columns:
                    st.error(f"Please fill all required fields: {', '.join(missing_columns)}")
                    return
                try:
                    self.db.insert_data(table_name, column_values) 
                    st.success(f"Data inserted successfully into {table_name}.")
                except Exception as e:
                    st.error(f"Error inserting data: {e}")


    def update_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_table())
        if table_name:
            columns = self.db.fetch_column(table_name)
            column_to_update = st.selectbox("Select the column to update", columns)
            new_value = st.text_input(f"Enter the new value for {column_to_update}")
            condition_column = st.selectbox("Select the condition column", columns)
            condition_value = st.text_input(f"Enter the condition value for {condition_column}")

            if st.button("Update Table"):
                if not new_value or not condition_value:
                    st.error("Please check the values you provided.")
                    return
                
                query = f"UPDATE {table_name} SET {column_to_update} = %s WHERE {condition_column} = %s"
                try:
                    self.db.execute_query(query, (new_value, condition_value))
                    st.success(f"Updated {column_to_update} in {table_name} where {condition_column} = {condition_value}")
                except Exception as e:
                    st.error(f"Error updating table: {e}")

    def delete_from_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_table())
        if table_name:
            delete_action = st.selectbox("Select the option", ["Drop the table", "Delete Row"])
            if delete_action == "Delete Row":
                condition_column = st.selectbox("Select the condition column", self.db.fetch_column(table_name))
                condition_value = st.text_input(f"Enter the condition value for {condition_column}")
                if condition_value:
                    query = f"DELETE FROM {table_name} WHERE {condition_column} = %s"
                    try:
                        self.db.execute_query(query, (condition_value,))
                        st.success("Rows deleted successfully.")
                    except Exception as e:
                        st.error(f"Error deleting rows: {e}")
            elif delete_action == "Drop the table":
                if st.checkbox(f"Confirm drop table {table_name}"):
                    query = f"DROP TABLE {table_name}"
                    try:
                        self.db.execute_query(query)
                        st.success("Table dropped successfully.")
                    except Exception as e:
                        st.error(f"Error dropping table: {e}")

    def alter_table(self):
        table_name = st.selectbox("Select a table", self.db.fetch_table())
        if table_name:
            columns = self.db.fetch_column(table_name)
            operation = st.selectbox("Select the Operation",["DROP COLUMN","MODIFY COLUMN","ADD"])
           
            if operation == "MODIFY COLUMN":
                column_to_update = st.selectbox("Select the column to alter", columns)
                column_values = st.text_input("Enter the Decepration (eg. VARCHAR(255))")
                query = f"ALTER TABLE {table_name} {column_to_update} {operation} {column_values} "
           
            elif operation == "ADD":
                column_values = st.text_input("Enter the Column Name and Decepration( eg. VARCHAR(255) )")
                query = f"ALTER TABLE {table_name} {operation} {column_values} "
            
            elif operation == "DROP COLUMN":
                column_to_update = st.selectbox("Select the column to alter", columns)
                st.status("Please press Alter Table Button to DROP COLUMN") 
                query = f"ALTER TABLE {table_name} {column_to_update} {operation}"
                

            if st.button("Alter Table"):
                try:
                    self.db.alter_table(table_name, query)
                    st.success(f"Column {operation} successfully to {table_name}.")
                except Exception as e:
                    st.error(f"Error altering table: {e}")
