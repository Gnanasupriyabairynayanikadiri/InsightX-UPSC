from sqlalchemy import create_engine
from urllib.parse import quote_plus

SERVER = r"LAPTOP-SMITHA\SQLEXPRESS"
DATABASE = "upsc_current_affairs"

params = quote_plus(
    f"DRIVER={{ODBC Driver 17 for SQL Server}};"
    f"SERVER={SERVER};"
    f"DATABASE={DATABASE};"
    f"Trusted_Connection=yes;"
)

engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")