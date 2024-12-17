from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
import random

def handle_client():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms')  # Fetch all rooms
    
    rooms = cursor.fetchall()
    cursor.execute('SELECT * FROM accomodations')
    accomodations=cursor.fetchall()
    conn.close()
    return render_template('client.html', rooms=rooms,accomodations=accomodations)

def handle_add_client_accomodation():
    
    id=random.randint(1, 2000)
    name=request.form.get('name')
    room_id = request.form.get('room_id')
    date_start = request.form.get('start-date')
    date_end = request.form.get('end-date')

 

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM accomodations WHERE id = ?', (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="client-overview"))
    #CHECK IF ACCOMODATION POSSIBLE

    cursor.execute('SELECT * FROM accomodations WHERE room_id = ?', (room_id,))
    rows = cursor.fetchall()

    # Convert rows to a list of dictionaries
    accommodations = [
        {
            "id": row["id"],
            "room_id": row["room_id"],
            "date_start": row["date_start"],
            "date_end": row["date_end"],
            "name": row["name"]
        }
        for row in rows
    ]

    for accommodation in accommodations:
        # Check if the new date range overlaps with an existing accommodation
        if not (
            (date_start < accommodation["date_start"] and date_end < accommodation["date_start"]) or
            (date_start > accommodation["date_end"] and date_end > accommodation["date_end"])
        ):
            conn.close()
            return redirect(url_for('handle_actions', action="client-overview"))
    
    cursor.execute('SELECT COUNT(*) FROM accomodations WHERE id = ?', (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="client-overview"))
    # No conflicts; proceed with insertion
    cursor.execute('''
        INSERT INTO accomodations (id, room_id, date_start, date_end, name)
        VALUES (?, ?, ?, ?, ?)
    ''', (id, room_id, date_start, date_end, name))

    conn.commit()
    conn.close()
    return redirect(url_for('handle_actions', action="client-overview"))
