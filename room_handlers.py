from flask import Flask, request, render_template, redirect, url_for
import sqlite3
from utils import get_db_connection

def home():
    return render_template('index.html')

def handle_redirects():
    # Get 'action' value from the form
    action = request.form.get('action')
    # Redirect to the 'actions' route with 'action' as a URL parameter
    return redirect(url_for("handle_actions", action=action))

def handle_actions(action):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM rooms')  # Fetch all rooms
    
    rooms = cursor.fetchall()
    cursor.execute('SELECT * FROM accomodations')
    accomodations=cursor.fetchall()
    conn.close()
    return render_template(f'{action}.html', rooms=rooms,accomodations=accomodations)

def handle_add_room():
    room_id = request.form.get('id')
    beds = request.form.get('beds')
    ppn = request.form.get('ppn')
    rating = 0  # Default rating
    no_ratings = 0

    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the room_id already exists
    cursor.execute('SELECT COUNT(*) FROM rooms WHERE id = ?', (room_id,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return redirect(url_for('handle_actions', action="manage_rooms"))

    # Insert the new room
    cursor.execute('''
        INSERT INTO rooms (id, beds, ppn, rating, no_ratings)
        VALUES (?, ?, ?, ?, ?)
    ''', (int(room_id), int(beds), int(ppn), rating, no_ratings))
    conn.commit()
    conn.close()
    return redirect(url_for('handle_actions', action="manage_rooms"))

def handle_delete_room():
    room_id = request.form.get('id')

    # Validate input
    conn = get_db_connection()
    cursor = conn.cursor()

    # Delete the first room with the given ID
    cursor.execute('DELETE FROM rooms WHERE id = ? ', (room_id,))
    conn.commit()

    # Check if any rows were affected
    

    conn.close()
    
    return redirect(url_for('handle_actions', action="manage_rooms"))
    
def handle_edit_room():
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