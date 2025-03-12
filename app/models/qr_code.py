from app import db
from datetime import datetime

class QRCode(db.Model):
    __tablename__ = 'qr_codes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    content = db.Column(db.Text, nullable=False)
    qr_type = db.Column(db.String(20), default='standard')  # standard, logo, etc.
    file_path = db.Column(db.String(255), nullable=False)
    logo_path = db.Column(db.String(255), nullable=True)
    size = db.Column(db.String(20), default='200x200')
    color = db.Column(db.String(20), default='#000000')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<QRCode {self.id}>' 