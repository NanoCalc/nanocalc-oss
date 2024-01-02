from flask_sqlalchemy import SQLAlchemy
import hashlib

db = SQLAlchemy()

class Visitor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(64), index=True)
    ip_address = db.Column(db.String(64))
    user_agent = db.Column(db.String(256))
    operating_system = db.Column(db.String(100))
    country = db.Column(db.String(100))
    visit_timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, ip_address, user_agent, operating_system, country):
        self.ip_address = hashlib.sha256(ip_address.encode()).hexdigest() if ip_address else None
        self.user_agent = user_agent
        self.operating_system = operating_system
        self.country = country
        self.session_id = hashlib.sha256((ip_address + user_agent).encode()).hexdigest() if ip_address and user_agent else None
