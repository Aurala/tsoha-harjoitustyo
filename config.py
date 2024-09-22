import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")

DATABASE_FILE = "ostoskeskus.db"
DATABASE_INIT_SCRIPT = "init_db.sql"
DATABASE_POPULATE_SCRIPT = "populate_db.sql"
