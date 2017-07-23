# This file will contain instructions to manage database migrations to update database schema
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from application import application as app, db
from models import Result
# Set the environment to target migration
app.config.from_object("config.DevelopmentConfig")

# Set the migration instance which has the app and db as arguments
migrate = Migrate(app, db)
manager = Manager(app)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()