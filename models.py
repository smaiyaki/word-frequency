from app import db


# This class will contain a model of the object we will be using in counting words
# This class allows us to use the following commands
# python manage.py db init (to initialise alembic for migrations)
# python manage.py db migrate (to perform the migration)
# python manage.py db upgrade (Migrate the changes to the actual database)
class Result(db.Model):
    __tablename__ = 'results' # Table called Result is first created

    # Creating columns in the Results table
    hashed_word = db.Column(db.String(100), primary_key=True)
    encrypted_word = db.Column(db.String(200))
    frequency = db.Column(db.Integer)
    url = db.Column(db.String(200))

    def __init__(self, hashed_word, encrypted_word,frequency, url):
        self.hashed_word = hashed_word
        self.encrypted_word = encrypted_word
        self.frequency = frequency
        self.url = url

    def __repr__(self):
        return '<hashed_word {}>'.format(self.hashed_word)