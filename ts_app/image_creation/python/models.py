from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from ...extensions import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
import io
import base64
from PIL import Image

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
class ts_image(db.Model):
    name: so.Mapped[str] = so.mapped_column(sa.String(64), primary_key=True)
    image_code: so.Mapped[str] = so.mapped_column(sa.TEXT)

    def get_image(self):
        return self.image_code
    
    def get_name(self):
        return self.name
    