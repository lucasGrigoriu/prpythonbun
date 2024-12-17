from flask import Flask, request, render_template, redirect, url_for
import sqlite3

def get_db_connection():
    conn = sqlite3.connect('mydatabase.db')
    conn.row_factory = sqlite3.Row  # Allows accessing rows as dictionaries
    return conn