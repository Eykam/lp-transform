from flask_login import UserMixin
from datetime import datetime
from . import db, login_manager


# TODO: implement
@login_manager.user_loader
def load_user(user_id):
    return User.objects(username = user_id).first()

# TODO: implement fields
class User(db.Document, UserMixin):
    username = db.StringField(unique=True, required=True, min=1, max=40)
    email = db.StringField(unique=True, required=True)
    password = db.StringField(required=True)
    profile_pic = db.ImageField()

    # Returns unique string identifying our object
    def get_id(self):
        # TODO: implement
        return self.username


# TODO: implement fields
class Review(db.Document):
    commenter = db.ReferenceField(User, required=True)
    content = db.StringField(required=True, min=5, max=500)
    date = db.StringField(required=True)
    imdb_id = db.StringField(required=True, min=9, max=9)
    movie_title = db.StringField(required=True, min=1, max=100)
    image = db.StringField()
    #Uncomment when other fields are ready for review pictures