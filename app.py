'''
Requirements
• The tool should be submitted with a pre-defined events in the data store. Events should have
the following fields identified:
    • An event will have a name
    • An event will have a location
    • An event will have a start and end time
    • An event will have a unique identifier
• The tool should accept an email address as a unique identification for a user (when signing
up for an event).
• The tool should allow the user to
    • List all events
    • Sign up for an event
    • Remove email address from event
• When signing up for an event the tool should email a pre-defined email address with a
notification.
• All properties (i.e. the pre-defined email address) should be easy to change before
deployment.
• All event times will be in the same timezone.
• An event can span multiple days.
'''
import json

from flasgger.utils import swag_from
from marshmallow_dataclass import dataclass
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

from dataclasses import field
from flasgger import Swagger

app = Flask(__name__)
swag = Swagger(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db = SQLAlchemy(app)


@dataclass
class Event(db.Model):
    id: int
    name: int
    location: str
    start_time: str
    end_time: str

    id = db.Column(db.Integer, primary_key=True, auto_increment=True)
    name = db.Column(db.Text)
    location = db.Column(db.Text)
    start_time = db.Column(db.Text)
    end_time = db.Column(db.Text)


@dataclass
class Participant(db.Model):
    email: str = field(metadata={"required": True})
    event_id: int = field(metadata={"required": True})

    email = db.Column(db.Text, primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True)


@app.route('/events', methods=['GET'])
@swag_from('api-doc/event/query.yml')
def query_event():
    events = Event.query.all()
    return jsonify(events), 200


@app.route('/events', methods=['POST'])
def create_event():
    event = Event.Schema().loads(json.dumps(request.json))
    db.session.add(event)
    db.session.commit()
    return Response(status=201)


@app.route('/events/<event_id>', methods=['DELETE'])
def remove_event(event_id):
    Event.query.filter_by(event_id=event_id).delete()
    db.session.commit()
    return Response(status=204)


@app.route('/register', methods=['POST'])
@swag_from('api-doc/register/create.yml')
def post():
    participant = Participant.Schema().loads(json.dumps(request.json))
    db.session.add(participant)
    db.session.commit()
    return Response(status=201)


@app.route('/register', methods=['DELETE'])
@swag_from('api-doc/register/delete.yml')
def delete():
    participant = Participant.Schema().loads(json.dumps(request.json))
    Participant.query.filter_by(email=participant.email).filter_by(event_id=participant.event_id).delete()
    db.session.commit()
    return Response(status=204)


if __name__ == '__main__':
    app.run(debug=True)
