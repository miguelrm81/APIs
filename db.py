import sqlite3
import pandas as pd
import os

os.chdir(os.path.dirname(__file__))
df = pd.read_csv(os.path.join('data', 'Advertising.csv'))
conn = sqlite3.connect(os.path.join('data', 'db.db'))
df.to_sql('advertising', conn, index=False)
conn.close()