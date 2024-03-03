import os
from dotenv import load_dotenv

import psycopg2

if (not load_dotenv()):
    raise DOTENV_NOTFOUND

conn = psycopg2.connect(database=os.getenv('DATANAME'),
                        host=os.getenv('HOST'),
                        user=os.getenv('DB_USER'),
                        password=os.getenv('DB_PASSWORD'),
                        port=os.getenv('PORT'))
