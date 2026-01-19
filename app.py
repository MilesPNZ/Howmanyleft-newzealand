from flask import Flask, request, render_template
from sqlalchemy import create_engine
import pandas as pd

app = Flask(__name__)
engine = create_engine('sqlite:///nz_vehicles.db')  # Your DB path

# Calculate total fleet dynamically at startup
total_fleet_df = pd.read_sql("SELECT COUNT(*) FROM vehicles", engine)
total_fleet = total_fleet_df.iloc[0,0]
print(f"Calculated total fleet: {total_fleet:,}")  # Debug print

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query'].upper()
        parts = query.split()
        make = parts[0] if parts else ''
        model = ' '.join(parts[1:]) if len(parts) > 1 else ''
        
        sql = "SELECT * FROM vehicles WHERE make LIKE ? AND model LIKE ?"
        params = (f'%{make}%', f'%{model}%')
        
        results = pd.read_sql(sql, engine, params=params)
        total = len(results)
        by_gen = results['generation'].value_counts().to_dict()
        
        rarity = total_fleet // total if total > 0 else 'N/A'
        
        return render_template('results.html', query=query, total=total, by_gen=by_gen, rarity=rarity)
    return home()

if __name__ == '__main__':
    app.run(debug=True)