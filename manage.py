# This file will contain instructions to manage database migrations to update database schema
import os
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand


from application import application, db
from models import Result
# Set the environment to target migration
application.config.from_object("config.DevelopmentConfig")

# Set the migration instance which has the app and db as arguments
migrate = Migrate(application, db)
manager = Manager(application)

manager.add_command('db', MigrateCommand)


if __name__ == '__main__':
    manager.run()