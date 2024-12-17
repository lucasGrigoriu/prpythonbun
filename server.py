from flask import Flask, request, render_template, redirect, url_for
from room_handlers import home, handle_redirects, handle_actions, handle_add_room, handle_delete_room, handle_edit_room
from accomodation_handlers import handle_add_accomodation, handle_delete_accomodation, handle_edit_accomodation
from client_handlers import handle_client, handle_add_client_accomodation

app = Flask(__name__)

# Serve the HTML form
app.add_url_rule('/', 'home', home, methods=['GET', 'POST'])
app.add_url_rule('/action_handler', 'handle_redirects', handle_redirects, methods=['POST'])
app.add_url_rule('/actions/<string:action>', 'handle_actions', handle_actions, methods=['GET'])
app.add_url_rule('/actions/<string:action>', 'handle_actions', handle_actions, methods=['GET'])

app.add_url_rule('/add_room', 'handle_add_room', handle_add_room, methods=['POST'])
app.add_url_rule('/delete_room', 'handle_delete_room', handle_delete_room, methods=['POST'])
app.add_url_rule('/edit_room', 'handle_edit_room', handle_edit_room, methods=['POST'])

app.add_url_rule('/add_accomodation', 'handle_add_accomodation', handle_add_accomodation, methods=['POST'])
app.add_url_rule('/delete_accomodation', 'handle_delete_accomodation', handle_delete_accomodation, methods=['POST'])
app.add_url_rule('/edit_accomodation', 'handle_edit_accomodation', handle_edit_accomodation, methods=['POST'])

app.add_url_rule('/client', 'handle_client', handle_client, methods=['GET'])
app.add_url_rule('/add_client_accomodation', 'handle_add_client_accomodation', handle_add_client_accomodation, methods=['POST'])


if __name__ == '__main__':
    app.run(debug=True)
