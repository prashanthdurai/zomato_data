from database_operation import Databaseclass
from crud_test import CRUDClass
import pandas as pd
import streamlit as st
# import mysql.connector  

#st.write("hello")

mydb=Databaseclass(
    host="localhost",
    user="root",
    password="Prasanth@23",
    database="zomato_database",
    #auth_plugin='mysql_native_password'
    )

#my_cursor=mydb.cursor()
crud_ops = CRUDClass(mydb)

st.title("Zomato Data Analysis")

menu = st.sidebar.radio("Zomato Data Analysis",["Data Entery Operation","Analysis Operation"])

if menu == "Data Entery Operation":

    st.sidebar.title("Zomato Data Entry")
    Data_operation = st.sidebar.selectbox("Select the Operation Data Entery",["Select the operation","Create","Read","Update","Delete","Insert","Alter"])
    
    if Data_operation == "Select the operation":
        st.image("C:/Users/Prashanth/Desktop/AIML_CLASS_GUVI/guvi_2.0/project/Zomato_Data_Insights/zomatoimagebag.jpg")
    elif Data_operation == "Create":
        crud_ops.create_table()
    elif Data_operation == "Read":
        crud_ops.read_table()
    elif Data_operation == "Update":
        crud_ops.update_table()
    elif Data_operation == "Insert":
        crud_ops.insert_table()
    elif Data_operation == "Delete":
        crud_ops.delete_from_table()
    elif Data_operation == "Alter":
        crud_ops.alter_table()


if menu == "Analysis Operation":
    
    MY_CURSOR = mydb.connection.cursor()
    sql_qures = [
        "SELECT DATE(order_date) AS order_date, HOUR(order_date) AS order_time, COUNT(*) AS order_id FROM orders GROUP BY order_date, order_time ORDER BY order_time DESC;",
        "SELECT order_id, HOUR(order_date) AS order_time, delivery_time, status FROM orders WHERE status = 'cancelled' and delivery_time > 45 ORDER BY delivery_time DESC;",
    ]
    qurey_title = [
        "Select the Analysis FaQ",
        "Most order plased in a days",
        "Order Canseled because of long delivery time",
        "Delete","Insert","prasanth"
    ]
    query_operation = st.selectbox("Select the Analysis FaQ",qurey_title)

    if query_operation == "Select the Analysis FaQ":
        #MY_CURSOR.execute()
        st.image("C:/Users/Prashanth/Desktop/AIML_CLASS_GUVI/guvi_2.0/project/Zomato_Data_Insights/zomatoimage.jpg")
    
    elif query_operation == "Most order plased in a days":
        MY_CURSOR.execute(sql_qures[0])
        data = MY_CURSOR.fetchall()
        #df = pd.read_sql(sql_qures[0],mydb)
        st.dataframe(data)
    
    elif query_operation == "Order Canseled because of long delivery time":
        MY_CURSOR.execute(sql_qures[1])
        data = MY_CURSOR.fetchall()
        #df = pd.read_sql(sql_qures[0],mydb)
        st.dataframe(data)