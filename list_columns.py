from sqlalchemy import create_engine
import pandas as pd

engine = create_engine('sqlite:///nz_vehicles.db')
columns = pd.read_sql("PRAGMA table_info(vehicles);", engine)['name'].to_list()
print(columns)