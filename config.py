import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

WTF_CSRF_ENABLED = True

SQLALCHEMY_DATABASE_URI = "postgresql:///markusaurala"
SQLALCHEMY_TRACK_MODIFICATIONS = False
DATABASE_INIT_SCRIPT = "init_db.sql"
DATABASE_POPULATE_SCRIPT = "populate_db.sql"
