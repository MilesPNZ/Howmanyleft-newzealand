import pandas as pd
from sqlalchemy import create_engine

# Connect to the DB
engine = create_engine('sqlite:///nz_vehicles.db')

# Test 1: Total vehicles in DB
total = pd.read_sql("SELECT COUNT(*) FROM vehicles", engine).iloc[0,0]
print(f"Total vehicles in DB: {total:,}")

# Test 2: Simple search for Outlander PHEVs 2003-2007
query = """
SELECT make, model, submodel, vehicle_year, generation, basic_colour, COUNT(*) as count
FROM vehicles
WHERE make = 'MITSUBISHI'
AND model LIKE '%OUTLANDER%'
AND submodel LIKE '%PHEV%'
AND vehicle_year BETWEEN 2003 AND 2007
GROUP BY generation
"""
results = pd.read_sql(query, engine)
print("\nOutlander PHEV 2003-2007 Breakdown:")
print(results.to_string(index=False))

# Test 3: Cortina example (submodels by generation)
cortina_query = """
SELECT generation, submodel, COUNT(*) as count
FROM vehicles
WHERE make = 'FORD'
AND model LIKE '%CORTINA%'
GROUP BY generation, submodel
ORDER BY generation
"""
cortina_results = pd.read_sql(cortina_query, engine)
print("\nFord Cortina Breakdown by Generation/Submodel:")
print(cortina_results.to_string(index=False))