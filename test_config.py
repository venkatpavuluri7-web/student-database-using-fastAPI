from database import Settings
settings=Settings()

print("Host:", settings.db_host)
print("Port:", settings.db_port)
print("User:", settings.db_user)
print("Database:", settings.db_name)