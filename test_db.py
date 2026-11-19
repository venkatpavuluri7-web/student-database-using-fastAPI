from database import engine
from database import setting
try:
    with engine.connect() as connection:
        print("connection successful")
except Exception as e:
    print("connection failed")
    print(e)
print("host",setting.db_host)