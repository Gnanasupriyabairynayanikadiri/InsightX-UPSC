from db import engine

with engine.connect() as conn:
    print("✅ SQL Server Connected")