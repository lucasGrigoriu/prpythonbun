from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection
from datetime import datetime
import random

def handle_add_accomodation():
    
    name=request.form.get('name')
    room_id = request.form.get('room_id')
    date_start = request.form.get('start-date')
    date_end = request.form.get('end-date')

 

    conn = get_db_connection()
    cursor = conn.cursor()
    id=random.randint(1, 2000)

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
            return redirect(url_for('handle_actions', action="manage_accomodations"))
    cursor.execute('SELECT COUNT(*) FROM accomodations WHERE id = ?', (id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="manage_accomodations"))
    # No conflicts; proceed with insertion
    cursor.execute('''
        INSERT INTO accomodations (id, room_id, date_start, date_end, name)
        VALUES (?, ?, ?, ?, ?)
    ''', (id, room_id, date_start, date_end, name))

    conn.commit()
    conn.close()
    return redirect(url_for('handle_actions', action="manage_accomodations"))





    
def handle_delete_accomodation():
    id = request.form.get('id')

    # Validate input
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the first room with the given ID
    cursor.execute('DELETE FROM accomodations WHERE id = ? ', (id,))
    conn.commit()

    # Check if any rows were affected
    

    conn.close()
    
    return redirect(url_for('handle_actions', action="manage_accomodations"))
    
def handle_edit_accomodation():
    room_id = request.form.get('room_id')
    beds = request.form.get('beds')
    ppn = request.form.get('ppn')
    rating = request.form.get('rating')
    no_ratings = request.form.get('no_ratings')
    conn = get_db_connection()
    cursor = conn.cursor()

    # Update the room's details
    cursor.execute('''
        UPDATE rooms
        SET beds = ?, ppn = ?, rating = ?, no_ratings = ?
        WHERE id = ?
    ''', (int(beds), float(ppn), float(rating), int(no_ratings), int(room_id)))
    conn.commit()

    # Check if any rows were updated
    if cursor.rowcount == 0:
        conn.close()
        return f"No room found with ID {room_id}.", 404

    conn.close()
    return redirect(url_for('manage_rooms'))