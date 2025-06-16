import os
from dotenv import load_dotenv
from sqlalchemy.engine.url import make_url

load_dotenv()
url = os.environ.get("SUPABASE_DATABASE_URL")
print("Loaded URL:", repr(url))
try:
    parsed = make_url(url)
    print("SQLAlchemy parsed URL:", parsed)
except Exception as e:
    print("Error:", e)