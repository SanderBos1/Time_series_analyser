from typing import Optional
import sqlalchemy as sa
import sqlalchemy.orm as so
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from extensions import db, login

@login.user_loader
def load_user(id):
    """
    Load a user from the database given its ID.

    Args:
        id (int): The ID of the user to load.

    Returns:
        User: The user object if found, None otherwise.
    """
    return db.session.get(User, int(id))

class User(UserMixin, db.Model):
    """
    Represents a user in the database.

    Attributes:
        id (int): The unique identifier for the user.
        username (str): The username of the user.
        email (str): The email address of the user.
        password_hash (str): The hashed password of the user.
    """

    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True,
                                                unique=True)
    email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True,
                                             unique=True)
    password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))

    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        """
        Set the password for the user.

        Args:
            password (str): The plaintext password to set.
        """
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """
        Check if the given password matches the user's password.

        Args:
            password (str): The plaintext password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return check_password_hash(self.password_hash, password)
    
class ts_image(db.Model):
    """
    Represents an image stored in the database.

    Attributes:
        name (str): The name of the image.
        image_code (str): The image code (e.g., binary data or URL).
        user (str): The user associated with the image.
    """
    id: so.Mapped[int] = so.mapped_column(primary_key=True)
    name: so.Mapped[str] = so.mapped_column(sa.String(64))
    image_code: so.Mapped[str] = so.mapped_column(sa.TEXT)
    user: so.Mapped[str] = so.mapped_column(sa.String(64))

    def get_image(self):
        """
        Get the image code.

        Returns:
            str: The image code.
        """

        return self.image_code
    
    def get_name(self):
        """
        Get the name of the image.

        Returns:
            str: The name of the image.
        """
        return self.name
    
    def get_user(self):
        """
        Get the user associated with the image.

        Returns:
            str: The user associated with the image.
        """
        return self.user
