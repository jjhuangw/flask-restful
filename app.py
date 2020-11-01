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
from flask import Flask, request, jsonify, Response
from flask_sqlalchemy import SQLAlchemy

from dataclasses import field
from marshmallow_dataclass import dataclass
from flasgger import Swagger
from flask_mail import Mail, Message
from threading import Thread
import logging
import configparser
import traceback

app = Flask(__name__)
db = SQLAlchemy(app)
log = logging.getLogger("demo")

config = configparser.RawConfigParser()
config.read('ConfigFile.properties')
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "API",
    "description": "demo",
    "specs": [
        {
            "version": "1.0.0",
            "title": "Event API",
            "description": "include event management and sign up functions",
            "endpoint": 'spec',
            "route": '/spec',
            "rule_filter": lambda rule: True
        }
    ]
}
Swagger(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///event.db'
db.init_app(app)

mail_settings = {
    "MAIL_SERVER": config.get('Email', 'mail.server'),
    "MAIL_PORT": config.get('Email', 'mail.port'),
    "MAIL_USE_TLS": True,
    "MAIL_USE_SSL": False,
    "MAIL_USERNAME": config.get('Email', 'mail.username'),
    "MAIL_PASSWORD": config.get('Email', 'mail.password')
}

app.config.update(mail_settings)
mail = Mail(app)


@app.route('/events', methods=['GET'])
@swag_from('api-doc/event/query.yml')
def query_event():
    events = Event.query.all()
    return jsonify(events), 200


@app.route('/events', methods=['POST'])
@swag_from('api-doc/event/create.yml')
def create_event():
    event = Event.Schema().loads(json.dumps(request.json))
    event.id = None
    db.session.add(event)
    db.session.commit()
    return Response(status=201)


@app.route('/events/<event_id>', methods=['PATCH'])
@swag_from('api-doc/event/update.yml')
def update_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return Response(status=404)
    revised = Event.Schema().loads(json.dumps(request.json))
    event.name = revised.name
    event.location = revised.location
    event.start_time = revised.start_time
    event.end_time = revised.end_time
    db.session.commit()
    return Response(status=204)


@app.route('/events/<event_id>', methods=['DELETE'])
@swag_from('api-doc/event/delete.yml')
def remove_event(event_id):
    event = Event.query.filter_by(id=event_id).first()
    if event is None:
        return Response(status=404)
    db.session.delete(event)
    db.session.commit()
    return Response(status=204)


@app.route('/register', methods=['POST'])
@swag_from('api-doc/register/create.yml')
def post():
    participant = Participant.Schema().loads(json.dumps(request.json))
    event = Event.query.filter_by(id=participant.event_id).first()
    if event is None:
        return Response(status=404)

    record = Participant.query.filter_by(email=participant.email).filter_by(event_id=participant.event_id).first()
    if record:
        return {"msg": "duplicated record"}, 403

    try:
        db.session.add(participant)
        msg = Message(config.get('Email', 'mail.title'),
                      sender=config.get('Email', 'mail.sender'),
                      recipients=[participant.email])
        msg.body = "You have been successfully registered " + event.name
        thr = Thread(target=send_async_email, args=[msg])
        thr.start()
    except Exception:
        log.error("Exception: %s" % traceback.format_exc())
        db.session.rollback()
    db.session.commit()
    return Response(status=201)


def send_async_email(msg):
    with app.app_context():
        mail.send(msg)


@app.route('/register', methods=['DELETE'])
@swag_from('api-doc/register/delete.yml')
def delete():
    participant = Participant.Schema().loads(json.dumps(request.json))
    record = Participant.query.filter_by(email=participant.email).filter_by(event_id=participant.event_id).first()
    if record is None:
        return Response(status=404)
    db.session.delete(record)
    db.session.commit()
    return Response(status=204)


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    log.error("Exception: %s" % traceback.format_exc())
    return jsonify(error=str(e)), code


@dataclass
class Event(db.Model):
    __tablename__ = "EVENT"
    id: int
    name: str
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
    __tablename__ = "PARTICIPANT"
    email: str = field(metadata={"required": True})
    event_id: int = field(metadata={"required": True})

    email = db.Column(db.Text, primary_key=True)
    event_id = db.Column(db.Integer, primary_key=True)


if __name__ == '__main__':
    app.run(debug=True)
