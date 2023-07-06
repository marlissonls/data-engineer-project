import psycopg2
from os import getenv
from dotenv import load_dotenv

load_dotenv()

conn = psycopg2.connect(host = getenv("DB_HOST"), 
                        port = getenv("DB_PORT"), 
                        dbname = getenv("DB_DATABASE"), 
                        user = getenv("DB_USER"), 
                        password = getenv("DB_PASSWORD"))
cursor = conn.cursor()