from flask import Flask, request, render_template
from sqlalchemy import create_engine
import pandas as pd
import os

app = Flask(__name__)

# Use environment variable for DB (for Vercel/Supabase)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///nz_vehicles.db')
engine = create_engine(DATABASE_URL)

# Get total fleet once at startup (dynamic)
try:
    total_fleet_df = pd.read_sql("SELECT COUNT(*) FROM vehicles", engine)
    total_fleet = total_fleet_df.iloc[0, 0]
    print(f"Total fleet loaded: {total_fleet:,}")
except Exception as e:
    total_fleet = 0
    print(f"DB error at startup: {e} - Running without data")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form['query'].upper()
        if not query:
            return render_template('results.html', query=query, total=0, by_gen={}, rarity='N/A', error="Please enter a search term")

        # Simple parsing
        parts = query.split()
        make = parts[0] if parts else ''
        model = ' '.join(parts[1:]) if len(parts) > 1 else ''

        sql = "SELECT * FROM vehicles WHERE make LIKE ? AND model LIKE ?"
        params = (f'%{make}%', f'%{model}%')

        try:
            results = pd.read_sql(sql, engine, params=params)
            total = len(results)
            by_gen = results['generation'].value_counts().to_dict() if 'generation' in results.columns else {}
            rarity = total_fleet // total if total > 0 else 'N/A'
            return render_template('results.html', query=query, total=total, by_gen=by_gen, rarity=rarity)
        except Exception as e:
            return render_template('results.html', query=query, total=0, by_gen={}, rarity='N/A', error=f"Search error: {str(e)}")
    return home()

if __name__ == '__main__':
    app.run(debug=True)