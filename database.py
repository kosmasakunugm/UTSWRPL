# database.py
import mysql.connector
from mysql.connector import Error
import streamlit as st

def get_db_connection():
    """Membuat koneksi ke database MySQL"""
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='fitnessmanagementsystem',
        port=3306
    )

def search_facilities(search_query, facility_type):
    # ... (kode fungsi yang diberikan)
    
def get_user_bookings(user_id):
    # ... (kode fungsi yang diberikan)

def update_profile(user_id, name, phone):
    # ... (kode fungsi yang diberikan)

# Tambahkan fungsi database lainnya di bawah ini